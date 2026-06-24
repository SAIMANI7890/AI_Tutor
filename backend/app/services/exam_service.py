"""
Exam Service - Phase 4C
Business logic layer for all examination operations.

Responsibilities:
- Orchestrate question generation via QuestionGeneratorService
- Enforce business rules (ownership, status transitions)
- Coordinate repositories for data access
- Aggregate data for API responses
"""
import logging
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.enums import QuestionType, TestStatus
from app.models.test import Test
from app.repositories.answer_repository import StudentAnswerRepository
from app.repositories.question_repository import TestQuestionRepository
from app.repositories.test_repository import TestRepository
from app.services.question_generation.generator import QuestionGeneratorService
from app.services.question_generation.schemas import ExamGenerationRequest

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Allowed values (single source of truth for validation)
# ---------------------------------------------------------------------------
VALID_CATEGORIES = {"History", "Geography", "Politics", "Economics"}
VALID_QUESTION_TYPES = {qt.value for qt in QuestionType}


# ---------------------------------------------------------------------------
# Lazy-initialised generator (avoids loading heavy ML models on import)
# ---------------------------------------------------------------------------
_generator: Optional[QuestionGeneratorService] = None


def _get_generator() -> QuestionGeneratorService:
    """Return (and lazily create) the singleton QuestionGeneratorService."""
    global _generator
    if _generator is None:
        _generator = QuestionGeneratorService(
            api_key=settings.GEMINI_API_KEY,
            chroma_db_path=settings.CHROMA_DB_PATH,
            use_local_embeddings=True,
        )
    return _generator


# ---------------------------------------------------------------------------
# ExamService
# ---------------------------------------------------------------------------

class ExamService:
    """
    Service layer for exam management (Phase 4C).

    All methods are static so they can be called without instantiation,
    matching the pattern used by UserService, StudyPlanService, etc.
    """

    # ------------------------------------------------------------------
    # 1. Generate exam
    # ------------------------------------------------------------------

    @staticmethod
    def generate_exam(
        db: Session,
        user_id: int,
        categories: List[str],
        question_type: str,
        question_count: int,
    ) -> dict:
        """
        Generate a new exam and persist it to the database.

        Args:
            db: Database session
            user_id: Authenticated user's ID
            categories: List of category names (History, Geography, …)
            question_type: One of MCQ | FILL_BLANKS | SHORT_ANSWER | LONG_ANSWER
            question_count: Number of questions (1-10)

        Returns:
            dict with test_id, question_count, status

        Raises:
            HTTPException 422: Invalid input
            HTTPException 500: Generation / DB failure
        """
        # --- Validate ---
        ExamService._validate_categories(categories)
        ExamService._validate_question_type(question_type)
        ExamService._validate_question_count(question_count)

        logger.info(
            "generate_exam | user=%s type=%s categories=%s count=%s",
            user_id, question_type, categories, question_count,
        )

        try:
            request = ExamGenerationRequest(
                user_id=user_id,
                subject="Social Studies",
                question_type=QuestionType(question_type),
                selected_categories=categories,
                question_count=question_count,
            )

            generator = _get_generator()
            result = generator.generate_exam(db, request)

            logger.info("generate_exam | created test_id=%s", result.test_id)

            return {
                "test_id": result.test_id,
                "question_count": result.question_count,
                "status": result.status,
            }

        except HTTPException:
            raise
        except ValueError as exc:
            logger.error("generate_exam | validation error: %s", exc)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc),
            )
        except Exception as exc:
            logger.error("generate_exam | unexpected error: %s", exc, exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Exam generation failed: {str(exc)}",
            )

    # ------------------------------------------------------------------
    # 2. Get exam detail (with questions, student-safe)
    # ------------------------------------------------------------------

    @staticmethod
    def get_exam(db: Session, test_id: UUID, user_id: int) -> dict:
        """
        Return exam metadata + questions (student-safe — no answers).

        Raises:
            HTTPException 404: Exam not found
            HTTPException 403: Not the owner
        """
        test = ExamService._get_owned_test(db, test_id, user_id)
        questions = TestQuestionRepository.get_by_test(db, test.id)

        return {
            "id": str(test.id),
            "subject": test.subject,
            "question_type": test.question_type.value,
            "selected_categories": test.selected_categories,
            "question_count": test.question_count,
            "status": test.status.value,
            "created_at": test.created_at.isoformat(),
            "started_at": test.started_at.isoformat() if test.started_at else None,
            "completed_at": test.completed_at.isoformat() if test.completed_at else None,
            "questions": [
                ExamService._serialize_question_for_student(q) for q in questions
            ],
        }

    # ------------------------------------------------------------------
    # 3. List exams for a user
    # ------------------------------------------------------------------

    @staticmethod
    def list_exams(db: Session, user_id: int) -> List[dict]:
        """
        Return all exams for the authenticated user (summary, no questions).

        Returns:
            List of exam summary dicts
        """
        tests = TestRepository.get_by_user(db, user_id)
        return [
            {
                "id": str(t.id),
                "subject": t.subject,
                "question_type": t.question_type.value,
                "selected_categories": t.selected_categories,
                "question_count": t.question_count,
                "status": t.status.value,
                "created_at": t.created_at.isoformat(),
                "started_at": t.started_at.isoformat() if t.started_at else None,
                "completed_at": t.completed_at.isoformat() if t.completed_at else None,
            }
            for t in tests
        ]

    # ------------------------------------------------------------------
    # 4. Get questions for an exam (student-safe)
    # ------------------------------------------------------------------

    @staticmethod
    def get_questions(db: Session, test_id: UUID, user_id: int) -> List[dict]:
        """
        Return only the questions of an exam.
        Does NOT include correct_answer or model_answer.

        Raises:
            HTTPException 404 / 403: See _get_owned_test
        """
        test = ExamService._get_owned_test(db, test_id, user_id)
        # Transition to IN_PROGRESS on first question fetch (if not already)
        if test.status == TestStatus.GENERATED:
            test.status = TestStatus.IN_PROGRESS
            test.started_at = datetime.now(timezone.utc)
            TestRepository.update(db, test)
            logger.info("get_questions | test %s → IN_PROGRESS", test_id)

        questions = TestQuestionRepository.get_by_test(db, test.id)
        return [ExamService._serialize_question_for_student(q) for q in questions]

    # ------------------------------------------------------------------
    # 5. Save (upsert) a student answer
    # ------------------------------------------------------------------

    @staticmethod
    def save_answer(
        db: Session,
        test_id: UUID,
        user_id: int,
        question_id: UUID,
        student_answer: str,
    ) -> dict:
        """
        Upsert a student answer. Supports autosave (create or update).

        Raises:
            HTTPException 404: Exam or question not found
            HTTPException 403: Not the owner
            HTTPException 400: Exam already submitted
        """
        test = ExamService._get_owned_test(db, test_id, user_id)

        if test.status == TestStatus.SUBMITTED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot save answers to a submitted exam.",
            )
        if test.status == TestStatus.EVALUATED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot save answers to an evaluated exam.",
            )

        # Verify question belongs to this test
        question = TestQuestionRepository.get_by_id(db, question_id)
        if question is None or question.test_id != test.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found in this exam.",
            )

        # Transition to IN_PROGRESS if still GENERATED
        if test.status == TestStatus.GENERATED:
            test.status = TestStatus.IN_PROGRESS
            test.started_at = datetime.now(timezone.utc)
            TestRepository.update(db, test)

        answer = StudentAnswerRepository.upsert(
            db, test_id=test.id, question_id=question.id,
            student_answer=student_answer,
        )

        logger.info(
            "save_answer | test=%s question=%s user=%s answer_id=%s",
            test_id, question_id, user_id, answer.id,
        )
        return {"answer_id": str(answer.id), "question_id": str(answer.question_id)}

    # ------------------------------------------------------------------
    # 6. Get saved answers
    # ------------------------------------------------------------------

    @staticmethod
    def get_answers(db: Session, test_id: UUID, user_id: int) -> List[dict]:
        """
        Return all saved answers for an exam.
        Used for page-refresh recovery.

        Raises:
            HTTPException 404 / 403: See _get_owned_test
        """
        ExamService._get_owned_test(db, test_id, user_id)
        answers = StudentAnswerRepository.get_by_test(db, test_id)
        return [
            {
                "answer_id": str(a.id),
                "question_id": str(a.question_id),
                "student_answer": a.student_answer,
                "updated_at": a.updated_at.isoformat(),
            }
            for a in answers
        ]

    # ------------------------------------------------------------------
    # 7. Submit exam
    # ------------------------------------------------------------------

    @staticmethod
    def submit_exam(db: Session, test_id: UUID, user_id: int) -> dict:
        """
        Submit the exam. Sets status to SUBMITTED and records completed_at.

        Raises:
            HTTPException 404 / 403: See _get_owned_test
            HTTPException 400: Already submitted / evaluated
        """
        test = ExamService._get_owned_test(db, test_id, user_id)

        if test.status == TestStatus.SUBMITTED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Exam has already been submitted.",
            )
        if test.status == TestStatus.EVALUATED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Exam has already been evaluated.",
            )

        answered_count = StudentAnswerRepository.count_answered(db, test.id)

        test.status = TestStatus.SUBMITTED
        test.completed_at = datetime.now(timezone.utc)
        if test.started_at is None:
            test.started_at = test.completed_at  # edge case: submit without answering
        TestRepository.update(db, test)

        logger.info(
            "submit_exam | test=%s user=%s answered=%s/%s",
            test_id, user_id, answered_count, test.question_count,
        )

        return {
            "test_id": str(test.id),
            "status": test.status.value,
            "completed_at": test.completed_at.isoformat(),
            "questions_answered": answered_count,
            "total_questions": test.question_count,
        }

    # ------------------------------------------------------------------
    # 8. Exam history
    # ------------------------------------------------------------------

    @staticmethod
    def get_history(db: Session, user_id: int) -> List[dict]:
        """
        Return exam history for the authenticated user.
        Same as list_exams but semantically named for the history endpoint.
        """
        return ExamService.list_exams(db, user_id)

    # ------------------------------------------------------------------
    # 9. Delete exam
    # ------------------------------------------------------------------

    @staticmethod
    def delete_exam(db: Session, test_id: UUID, user_id: int) -> dict:
        """
        Delete an exam and all associated data (questions and answers).

        Args:
            db: Database session
            test_id: UUID of the exam to delete
            user_id: Authenticated user's ID

        Returns:
            dict with success message

        Raises:
            HTTPException 404: Exam not found
            HTTPException 403: Not the owner
        """
        # Verify ownership
        test = ExamService._get_owned_test(db, test_id, user_id)

        logger.info(
            "delete_exam | user=%s test_id=%s status=%s",
            user_id, test_id, test.status
        )

        # Delete answers first (foreign key constraint)
        StudentAnswerRepository.delete_by_test(db, test.id)
        
        # Delete questions
        TestQuestionRepository.delete_by_test(db, test.id)
        
        # Delete test
        TestRepository.delete(db, test)

        logger.info("delete_exam | successfully deleted test %s", test_id)

        return {
            "test_id": str(test_id),
            "message": "Exam deleted successfully"
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _get_owned_test(db: Session, test_id: UUID, user_id: int) -> Test:
        """
        Fetch test and verify ownership.

        Raises:
            HTTPException 404: Not found
            HTTPException 403: Not owner
        """
        test = TestRepository.get_by_id(db, test_id)
        if test is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exam not found.",
            )
        if test.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this exam.",
            )
        return test

    @staticmethod
    def _serialize_question_for_student(q) -> dict:
        """
        Serialize a TestQuestion for student consumption.
        NEVER includes correct_answer or model_answer.
        """
        data: dict = {
            "id": str(q.id),
            "question_number": q.question_number,
            "question_type": q.question_type.value,
            "question_text": q.question_text,
            "category": q.category,
        }
        # Include options only for MCQ
        if q.question_type == QuestionType.MCQ and q.options_json:
            data["options"] = q.options_json
        return data

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_categories(categories: List[str]) -> None:
        if not categories:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="At least one category must be selected.",
            )
        invalid = [c for c in categories if c not in VALID_CATEGORIES]
        if invalid:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid categories: {invalid}. Valid: {sorted(VALID_CATEGORIES)}",
            )

    @staticmethod
    def _validate_question_type(question_type: str) -> None:
        if question_type not in VALID_QUESTION_TYPES:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid question type: '{question_type}'. "
                       f"Valid types: {sorted(VALID_QUESTION_TYPES)}",
            )

    @staticmethod
    def _validate_question_count(count: int) -> None:
        if not (1 <= count <= 10):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="question_count must be between 1 and 10.",
            )
