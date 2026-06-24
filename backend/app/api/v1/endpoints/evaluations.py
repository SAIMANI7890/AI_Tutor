"""
Evaluation API Endpoints
Handles AI-powered answer evaluation
"""
import os
import logging
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.core.config import settings
from app.schemas.response import APIResponse
from app.schemas.evaluation import (
    EvaluateAnswerRequest,
    EvaluateAnswerResponse,
    EvaluationResponse,
    EvaluationSummary,
    ChapterPerformance,
    UserPerformanceStats
)
from app.services.ai_evaluation_service import AIEvaluationService
from app.services.evaluation_orchestration_service import (
    EvaluationOrchestrationService,
    create_orchestration_service
)
from app.services.evaluation_service import EvaluationService

logger = logging.getLogger(__name__)

router = APIRouter()

# Singleton AI evaluation service
_ai_evaluation_service = None


def get_ai_evaluation_service() -> AIEvaluationService:
    """Get or create AI evaluation service instance"""
    global _ai_evaluation_service
    
    if _ai_evaluation_service is None:
        # Get configuration
        api_key = os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY
        if not api_key or api_key.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="GEMINI_API_KEY not configured. Please set the API key in your environment variables or .env file."
            )
        
        chroma_db_path = os.getenv("CHROMA_DB_PATH", "./chroma_db")
        top_k = int(os.getenv("TOP_K_RESULTS", "5"))
        
        try:
            _ai_evaluation_service = AIEvaluationService(
                api_key=api_key,
                chroma_db_path=chroma_db_path,
                top_k=top_k,
                temperature=0.3,  # Lower temperature for consistent evaluation
                use_local_embeddings=True
            )
            logger.info("AI evaluation service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AI evaluation service: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to initialize AI evaluation service. Please ensure the knowledge base has been ingested."
            )
    
    return _ai_evaluation_service


@router.post("/evaluate", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def evaluate_answer(
    request: EvaluateAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ai_service: AIEvaluationService = Depends(get_ai_evaluation_service)
):
    """
    Evaluate a student's answer using AI
    
    Workflow:
    1. Retrieve relevant textbook content using RAG
    2. Generate model answer from textbook
    3. Evaluate student answer
    4. Store evaluation in database
    5. Return complete evaluation
    
    Args:
        request: Evaluation request with question and answer
        current_user: Authenticated user
        db: Database session
        ai_service: AI evaluation service
        
    Returns:
        API response with evaluation results
    """
    try:
        logger.info(f"User {current_user.id} requested evaluation for question: {request.question[:50]}...")
        
        # Create orchestration service
        orchestration_service = create_orchestration_service(ai_service, db)
        
        # Execute evaluation workflow
        evaluation_response = orchestration_service.evaluate_and_store(
            question=request.question,
            student_answer=request.student_answer,
            user_id=current_user.id,
            chapter_name=request.chapter_name,
            test_id=str(request.test_id) if request.test_id else None,
            question_id=str(request.question_id) if request.question_id else None,
            total_marks=request.total_marks
        )
        
        # Convert to API response format
        api_response_data = EvaluateAnswerResponse(
            evaluation_id=evaluation_response.id,
            question=evaluation_response.question,
            student_answer=evaluation_response.student_answer,
            model_answer=evaluation_response.model_answer,
            marks_awarded=evaluation_response.marks_awarded,
            total_marks=evaluation_response.total_marks,
            feedback=evaluation_response.feedback,
            strengths=evaluation_response.strengths or [],
            improvements=evaluation_response.improvements or [],
            chapter_name=evaluation_response.chapter_name,
            created_at=evaluation_response.created_at,
            percentage=round((evaluation_response.marks_awarded / evaluation_response.total_marks) * 100, 2)
        )
        
        logger.info(
            f"Evaluation completed: {api_response_data.marks_awarded}/{api_response_data.total_marks} marks"
        )
        
        return APIResponse(
            success=True,
            message="Answer evaluated successfully",
            data=api_response_data.model_dump()
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error in evaluation endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Evaluation failed: {str(e)}"
        )


@router.get("/submitted-tests", response_model=APIResponse)
async def get_submitted_tests_for_evaluation(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all submitted tests with long-answer questions for evaluation
    
    Returns tests that:
    - Have status SUBMITTED
    - Contain LONG_ANSWER type questions
    - Have student answers submitted
    - Belong to current user
    
    Args:
        current_user: Authenticated user
        db: Database session
        
    Returns:
        API response with list of submitted tests and their long answers
    """
    try:
        from app.repositories.test_repository import TestRepository
        from app.repositories.question_repository import TestQuestionRepository
        from app.repositories.answer_repository import StudentAnswerRepository
        from app.repositories.evaluation_repository import EvaluationRepository
        from app.models.enums import TestStatus, QuestionType
        
        logger.info(f"Fetching submitted tests with long answers for user {current_user.id}")
        
        # Get all submitted tests for this user
        try:
            submitted_tests = TestRepository.get_by_user_and_status(
                db, 
                user_id=current_user.id,
                status=TestStatus.SUBMITTED
            )
            logger.info(f"Found {len(submitted_tests)} submitted tests")
        except Exception as e:
            logger.error(f"Error fetching submitted tests: {e}", exc_info=True)
            raise
        
        result_tests = []
        
        for test in submitted_tests:
            try:
                # Get all long answer questions for this test
                all_questions = TestQuestionRepository.get_by_test(db, test.id)
                long_answer_questions = [q for q in all_questions if q.question_type == QuestionType.LONG_ANSWER]
                
                if not long_answer_questions:
                    logger.debug(f"Test {test.id} has no long answer questions, skipping")
                    continue  # Skip tests with no long answer questions
                
                # Get student answers for long answer questions
                all_answers = StudentAnswerRepository.get_by_test(db, test.id)
                answer_map = {str(ans.question_id): ans for ans in all_answers}
                
                long_answers_data = []
                
                for question in long_answer_questions:
                    answer = answer_map.get(str(question.id))
                    
                    if not answer or not answer.student_answer or answer.student_answer.strip() == "":
                        logger.debug(f"Question {question.id} not answered, skipping")
                        continue  # Skip unanswered questions
                    
                    # Check if this question has already been evaluated
                    existing_evaluation = EvaluationRepository.get_by_test_and_question(
                        db,
                        test_id=str(test.id),
                        question_id=str(question.id)
                    )
                    
                    long_answers_data.append({
                        "question_id": str(question.id),
                        "question_number": question.question_number,
                        "question_summary": question.question_text[:120],
                        "student_answer": answer.student_answer,
                        "evaluation_id": str(existing_evaluation.id) if existing_evaluation else None,
                        "marks_awarded": existing_evaluation.marks_awarded if existing_evaluation else None
                    })
                
                if long_answers_data:  # Only include tests that have answered long answer questions
                    categories_str = ', '.join(test.selected_categories) if test.selected_categories else 'General'
                    result_tests.append({
                        "test_id": str(test.id),
                        "test_name": f"{categories_str} Exam",
                        "created_at": test.created_at.isoformat(),
                        "completed_at": test.completed_at.isoformat() if test.completed_at else None,
                        "category": categories_str,
                        "long_answers": long_answers_data
                    })
                    logger.debug(f"Added test {test.id} with {len(long_answers_data)} long answers")
                    
            except Exception as e:
                logger.error(f"Error processing test {test.id}: {e}", exc_info=True)
                continue  # Skip this test and continue with others
        
        logger.info(f"Found {len(result_tests)} submitted tests with long answers")
        
        return APIResponse(
            success=True,
            message=f"Retrieved {len(result_tests)} submitted tests",
            data={
                "tests": result_tests,
                "count": len(result_tests)
            }
        )
        
    except Exception as e:
        logger.error(f"Error fetching submitted tests: {e}", exc_info=True)
        # Return empty list instead of error for better UX
        return APIResponse(
            success=True,
            message="No submitted tests available or error occurred",
            data={
                "tests": [],
                "count": 0
            }
        )


@router.get("", response_model=APIResponse)
async def get_user_evaluations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Maximum number of evaluations"),
    offset: Optional[int] = Query(None, ge=0, description="Number of evaluations to skip")
):
    """
    Get all evaluations for current user
    
    Args:
        current_user: Authenticated user
        db: Database session
        limit: Maximum number of results
        offset: Number to skip (for pagination)
        
    Returns:
        API response with list of evaluations
    """
    try:
        logger.info(f"Fetching evaluations for user {current_user.id}")
        
        service = EvaluationService(db)
        evaluations = service.get_user_evaluations(
            user_id=current_user.id,
            limit=limit,
            offset=offset
        )
        
        logger.info(f"Retrieved {len(evaluations)} evaluations")
        
        return APIResponse(
            success=True,
            message=f"Retrieved {len(evaluations)} evaluations",
            data={
                "evaluations": [eval.model_dump() for eval in evaluations],
                "count": len(evaluations)
            }
        )
        
    except Exception as e:
        logger.error(f"Error fetching evaluations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve evaluations: {str(e)}"
        )


@router.get("/{evaluation_id}", response_model=APIResponse)
async def get_evaluation(
    evaluation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific evaluation by ID
    
    Args:
        evaluation_id: Evaluation UUID
        current_user: Authenticated user
        db: Database session
        
    Returns:
        API response with evaluation details
    """
    try:
        logger.info(f"Fetching evaluation {evaluation_id} for user {current_user.id}")
        
        service = EvaluationService(db)
        evaluation = service.get_evaluation_by_id(evaluation_id)
        
        # Authorization check: user can only access their own evaluations
        if evaluation.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this evaluation"
            )
        
        return APIResponse(
            success=True,
            message="Evaluation retrieved successfully",
            data=evaluation.model_dump()
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching evaluation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve evaluation: {str(e)}"
        )


@router.get("/chapter/{chapter_name}", response_model=APIResponse)
async def get_chapter_evaluations(
    chapter_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all evaluations for a specific chapter
    
    Args:
        chapter_name: Chapter/topic name
        current_user: Authenticated user
        db: Database session
        
    Returns:
        API response with chapter evaluations
    """
    try:
        logger.info(f"Fetching evaluations for chapter '{chapter_name}' for user {current_user.id}")
        
        service = EvaluationService(db)
        evaluations = service.get_chapter_evaluations(
            user_id=current_user.id,
            chapter_name=chapter_name
        )
        
        logger.info(f"Retrieved {len(evaluations)} evaluations for chapter '{chapter_name}'")
        
        return APIResponse(
            success=True,
            message=f"Retrieved {len(evaluations)} evaluations for chapter '{chapter_name}'",
            data={
                "chapter_name": chapter_name,
                "evaluations": [eval.model_dump() for eval in evaluations],
                "count": len(evaluations)
            }
        )
        
    except Exception as e:
        logger.error(f"Error fetching chapter evaluations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve chapter evaluations: {str(e)}"
        )


@router.get("/stats/performance", response_model=APIResponse)
async def get_user_performance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get overall performance statistics for current user
    
    Args:
        current_user: Authenticated user
        db: Database session
        
    Returns:
        API response with performance statistics
    """
    try:
        logger.info(f"Fetching performance stats for user {current_user.id}")
        
        service = EvaluationService(db)
        stats = service.get_user_performance_stats(current_user.id)
        
        return APIResponse(
            success=True,
            message="Performance statistics retrieved successfully",
            data=stats.model_dump()
        )
        
    except Exception as e:
        logger.error(f"Error fetching performance stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve performance statistics: {str(e)}"
        )


@router.get("/stats/chapters", response_model=APIResponse)
async def get_chapters_performance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get performance statistics for all chapters
    
    Args:
        current_user: Authenticated user
        db: Database session
        
    Returns:
        API response with chapter-wise performance
    """
    try:
        logger.info(f"Fetching chapter performance for user {current_user.id}")
        
        service = EvaluationService(db)
        chapters_performance = service.get_all_chapters_performance(current_user.id)
        
        return APIResponse(
            success=True,
            message=f"Retrieved performance for {len(chapters_performance)} chapters",
            data={
                "chapters": [chap.model_dump() for chap in chapters_performance],
                "count": len(chapters_performance)
            }
        )
        
    except Exception as e:
        logger.error(f"Error fetching chapter performance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve chapter performance: {str(e)}"
        )


@router.get("/stats/chapter/{chapter_name}", response_model=APIResponse)
async def get_chapter_performance(
    chapter_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get performance statistics for a specific chapter
    
    Args:
        chapter_name: Chapter/topic name
        current_user: Authenticated user
        db: Database session
        
    Returns:
        API response with chapter performance
    """
    try:
        logger.info(f"Fetching performance for chapter '{chapter_name}' for user {current_user.id}")
        
        service = EvaluationService(db)
        chapter_perf = service.get_chapter_performance(current_user.id, chapter_name)
        
        return APIResponse(
            success=True,
            message=f"Chapter performance retrieved successfully",
            data=chapter_perf.model_dump()
        )
        
    except Exception as e:
        logger.error(f"Error fetching chapter performance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve chapter performance: {str(e)}"
        )


@router.delete("/{evaluation_id}", response_model=APIResponse)
async def delete_evaluation(
    evaluation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an evaluation
    
    Args:
        evaluation_id: Evaluation UUID
        current_user: Authenticated user
        db: Database session
        
    Returns:
        API response confirming deletion
    """
    try:
        logger.info(f"Deleting evaluation {evaluation_id} for user {current_user.id}")
        
        service = EvaluationService(db)
        success = service.delete_evaluation(evaluation_id, current_user.id)
        
        if success:
            return APIResponse(
                success=True,
                message="Evaluation deleted successfully",
                data={"evaluation_id": str(evaluation_id)}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete evaluation"
            )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting evaluation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete evaluation: {str(e)}"
        )


@router.get("/health/check", response_model=APIResponse)
def check_evaluation_health(
    ai_service: AIEvaluationService = Depends(get_ai_evaluation_service)
):
    """
    Check if evaluation service is healthy and ready
    
    Returns:
        API response with health status
    """
    try:
        # Check if vector store has data
        collection_count = ai_service.retriever.collection.count()
        
        return APIResponse(
            success=True,
            message="AI Evaluation service is ready",
            data={
                "status": "healthy",
                "chunks_loaded": collection_count,
                "model": "gemini-2.5-flash-lite",
                "service": "evaluation"
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI Evaluation service is not ready"
        )


# ===========================================================================
# HELPER FUNCTIONS — Full-test evaluation
# ===========================================================================

def _compute_performance_level(percentage: float) -> str:
    """Map percentage to human-readable performance label."""
    if percentage >= 90:
        return "Excellent"
    elif percentage >= 75:
        return "Good"
    elif percentage >= 60:
        return "Average"
    else:
        return "Needs Improvement"


def _auto_grade(student_answer: str, correct_answer: str | None, total_marks: int = 10) -> dict:
    """
    Deterministically grade MCQ / FILL_BLANKS questions.
    Returns a dict with the same keys as an AI evaluation result.
    Null-safe: handles None correct_answer gracefully.
    """
    # Guard against missing correct answer
    if not correct_answer:
        return {
            "model_answer": "Correct answer not available",
            "marks_awarded": 0,
            "total_marks": total_marks,
            "feedback": "This question could not be auto-graded because the correct answer is missing.",
            "strengths": [],
            "improvements": ["Contact your instructor if this persists"],
        }

    if not student_answer or student_answer.strip() == "" or student_answer == "No answer provided":
        return {
            "model_answer": correct_answer,
            "marks_awarded": 0,
            "total_marks": total_marks,
            "feedback": "No answer was provided for this question.",
            "strengths": [],
            "improvements": [
                "Always attempt every question — partial credit may be available",
                "Review this topic in your textbook",
            ],
        }

    s = student_answer.strip().lower()
    c = correct_answer.strip().lower()

    if s == c:
        return {
            "model_answer": correct_answer,
            "marks_awarded": total_marks,
            "total_marks": total_marks,
            "feedback": "Correct! Your answer matches the expected answer perfectly.",
            "strengths": ["Accurate recall of facts", "Correctly identified the answer"],
            "improvements": [],
        }

    # Check if the student's answer contains the correct answer (partial credit)
    if c in s or s in c:
        partial = max(1, total_marks // 2)
        return {
            "model_answer": correct_answer,
            "marks_awarded": partial,
            "total_marks": total_marks,
            "feedback": (
                f"Partially correct. The expected answer is '{correct_answer}'. "
                "Your answer contained the key idea but was not an exact match."
            ),
            "strengths": ["Recalled the general concept"],
            "improvements": [
                f"The exact answer is: {correct_answer}",
                "Practice writing precise answers",
            ],
        }

    return {
        "model_answer": correct_answer,
        "marks_awarded": 0,
        "total_marks": total_marks,
        "feedback": (
            f"Incorrect. The correct answer is '{correct_answer}'. "
            "Review this topic in your textbook."
        ),
        "strengths": [],
        "improvements": [
            f"Correct answer: {correct_answer}",
            "Revise the relevant chapter",
            "Practice similar questions",
        ],
    }


def _build_question_result(question, student_answer_text: str, eval_record) -> dict:
    """Build a unified QuestionEvaluationResult dict from DB objects."""
    qt = question.question_type.value if hasattr(question.question_type, "value") else question.question_type
    return {
        "question_id": str(question.id),
        "question_number": question.question_number,
        "question_type": qt,
        "question_text": question.question_text,
        "student_answer": student_answer_text or "",
        "correct_answer": question.correct_answer if qt in ("MCQ", "FILL_BLANKS") else None,
        "model_answer": eval_record.model_answer,
        "marks_awarded": eval_record.marks_awarded,
        "total_marks": eval_record.total_marks,
        "feedback": eval_record.feedback,
        "strengths": eval_record.strengths or [],
        "improvements": eval_record.improvements or [],
        "category": question.category,
        "is_auto_graded": qt in ("MCQ", "FILL_BLANKS"),
        "evaluation_id": str(eval_record.id),
    }


def _compute_ai_insights(question_results: list) -> dict:
    """Aggregate per-question feedback into test-level AI insights."""
    all_strengths = []
    all_improvements = []
    category_scores: dict = {}

    for r in question_results:
        all_strengths.extend(r.get("strengths") or [])
        all_improvements.extend(r.get("improvements") or [])
        cat = r.get("category", "General")
        if cat not in category_scores:
            category_scores[cat] = {"awarded": 0, "possible": 0}
        category_scores[cat]["awarded"] += r["marks_awarded"]
        category_scores[cat]["possible"] += r["total_marks"]

    weak_areas = []
    recommendations = []
    strong_areas = []

    for cat, sc in category_scores.items():
        if sc["possible"] == 0:
            continue
        pct = (sc["awarded"] / sc["possible"]) * 100
        if pct >= 75:
            strong_areas.append(f"Strong understanding of {cat} ({pct:.0f}%)")
        elif pct < 60:
            weak_areas.append(f"{cat} needs improvement ({pct:.0f}%)")
            recommendations.append(f"Revise {cat} chapter thoroughly")
        else:
            recommendations.append(f"Practice more {cat} questions to reach excellence")

    # De-duplicate
    unique_strengths = list(dict.fromkeys(all_strengths))[:4]
    unique_improvements = list(dict.fromkeys(all_improvements))[:4]

    if strong_areas:
        unique_strengths = (strong_areas + unique_strengths)[:5]

    if not recommendations:
        recommendations.append("Excellent! Keep revising regularly to maintain your performance")

    return {
        "strengths": unique_strengths[:5],
        "weak_areas": (weak_areas + unique_improvements)[:5],
        "recommendations": recommendations[:5],
    }


def _build_test_summary(test, question_results: list) -> dict:
    """Compute top-level summary fields for a test evaluation."""
    total_awarded = sum(r["marks_awarded"] for r in question_results)
    total_possible = sum(r["total_marks"] for r in question_results)
    percentage = round((total_awarded / total_possible) * 100, 1) if total_possible > 0 else 0
    status_val = test.status.value if hasattr(test.status, "value") else test.status
    qt_val = test.question_type.value if hasattr(test.question_type, "value") else test.question_type

    return {
        "test_id": str(test.id),
        "test_name": f"{', '.join(test.selected_categories)} — {qt_val.replace('_', ' ').title()} Test",
        "question_type": qt_val,
        "categories": test.selected_categories,
        "question_count": test.question_count,
        "submitted_at": test.completed_at.isoformat() if test.completed_at else test.created_at.isoformat(),
        "status": status_val,
        "total_marks_awarded": total_awarded,
        "total_marks_possible": total_possible,
        "percentage": percentage,
        "performance_level": _compute_performance_level(percentage),
        "question_results": question_results,
        "ai_insights": _compute_ai_insights(question_results),
    }


# ===========================================================================
# ENDPOINT: GET /evaluations/test/{test_id}/results
# ===========================================================================

@router.get("/test/{test_id}/results", response_model=APIResponse)
async def get_test_evaluation_results(
    test_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get all existing evaluation results for a test.

    Returns the full TestEvaluationSummary if the test has been evaluated,
    or a partial structure with evaluation_count=0 if not yet evaluated.

    Used on page load to check if evaluation already exists.
    """
    try:
        from app.repositories.test_repository import TestRepository
        from app.repositories.question_repository import TestQuestionRepository
        from app.repositories.answer_repository import StudentAnswerRepository
        from app.repositories.evaluation_repository import EvaluationRepository

        # 1. Verify test ownership
        test = TestRepository.get_by_id(db, test_id)
        if not test:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not found")
        if test.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        # 2. Get existing evaluations for this test
        existing_evals = EvaluationRepository.get_by_test(db, test_id)  # pass UUID, not str
        if not existing_evals:
            return APIResponse(
                success=True,
                message="No evaluations found for this test",
                data={"evaluated": False, "evaluation_count": 0, "test_id": str(test_id)},
            )

        # 3. Get questions and answers for joining
        questions = TestQuestionRepository.get_by_test(db, test_id)
        answers = StudentAnswerRepository.get_by_test(db, test_id)
        answer_map = {str(a.question_id): a.student_answer for a in answers}
        eval_map = {str(e.question_id): e for e in existing_evals if e.question_id}

        # 4. Build question results
        question_results = []
        for q in sorted(questions, key=lambda x: x.question_number):
            eval_rec = eval_map.get(str(q.id))
            if eval_rec:
                question_results.append(
                    _build_question_result(q, answer_map.get(str(q.id), ""), eval_rec)
                )

        summary = _build_test_summary(test, question_results)
        summary["evaluated"] = True
        summary["evaluation_count"] = len(existing_evals)

        return APIResponse(
            success=True,
            message="Evaluation results retrieved successfully",
            data=summary,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching test evaluation results: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve evaluation results: {str(e)}",
        )


# ===========================================================================
# ENDPOINT: POST /evaluations/test/{test_id}/evaluate
# ===========================================================================

@router.post("/test/{test_id}/evaluate", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def evaluate_full_test(
    test_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Evaluate ALL questions in a submitted test.

    Evaluation strategy by question type:
    - MCQ / FILL_BLANKS  → auto-graded (exact/partial string match, no AI call)
    - SHORT_ANSWER / LONG_ANSWER → AI-graded via existing RAG + Gemini pipeline

    Idempotent: already-evaluated questions are skipped.
    Updates test status to EVALUATED on completion.
    Returns full TestEvaluationSummary.
    """
    try:
        from app.repositories.test_repository import TestRepository
        from app.repositories.question_repository import TestQuestionRepository
        from app.repositories.answer_repository import StudentAnswerRepository
        from app.repositories.evaluation_repository import EvaluationRepository
        from app.schemas.evaluation import EvaluationCreate
        from app.models.enums import TestStatus, QuestionType

        logger.info(f"Full-test evaluation requested: test={test_id} user={current_user.id}")

        # ── 1. Validate test ─────────────────────────────────────────────────
        test = TestRepository.get_by_id(db, test_id)
        if not test:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not found")
        if test.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        current_status = test.status.value if hasattr(test.status, "value") else test.status
        if current_status not in ("SUBMITTED", "EVALUATED"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Test must be SUBMITTED before evaluation. Current status: {current_status}",
            )

        # ── 2. Fetch data ────────────────────────────────────────────────────
        questions = TestQuestionRepository.get_by_test(db, test_id)
        if not questions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No questions found for this test")

        answers = StudentAnswerRepository.get_by_test(db, test_id)
        answer_map = {str(a.question_id): a.student_answer for a in answers}

        existing_evals = EvaluationRepository.get_by_test(db, test_id)  # pass UUID, not str
        eval_map = {str(e.question_id): e for e in existing_evals if e.question_id}

        # ── 3. Determine if AI is needed ─────────────────────────────────────
        needs_ai = any(
            (q.question_type.value if hasattr(q.question_type, "value") else q.question_type)
            in ("SHORT_ANSWER", "LONG_ANSWER")
            for q in questions
            if str(q.id) not in eval_map
        )

        orchestration_svc = None
        if needs_ai:
            try:
                ai_svc = get_ai_evaluation_service()
                orchestration_svc = create_orchestration_service(ai_svc, db)
            except HTTPException as e:
                # If AI service is unavailable, we can still grade MCQ/FILL_BLANKS
                logger.warning(f"AI service unavailable: {e.detail}")

        # ── 4. Evaluate each question ─────────────────────────────────────────
        evaluation_service = EvaluationService(db)
        question_results = []

        for question in sorted(questions, key=lambda q: q.question_number):
            qid = str(question.id)
            qt = question.question_type.value if hasattr(question.question_type, "value") else question.question_type
            student_answer_text = answer_map.get(qid, "") or ""

            # Skip already-evaluated questions — use existing result
            if qid in eval_map:
                logger.info(f"Q{question.question_number} already evaluated, reusing")
                question_results.append(
                    _build_question_result(question, student_answer_text, eval_map[qid])
                )
                continue

            # ── Auto-grade MCQ / FILL_BLANKS ─────────────────────────────────
            if qt in ("MCQ", "FILL_BLANKS"):
                grade = _auto_grade(student_answer_text, question.correct_answer, total_marks=10)
                eval_data = EvaluationCreate(
                    user_id=current_user.id,
                    test_id=str(test_id),
                    question_id=qid,
                    question=question.question_text,
                    student_answer=student_answer_text or "No answer provided",
                    model_answer=grade["model_answer"],
                    marks_awarded=grade["marks_awarded"],
                    total_marks=grade["total_marks"],
                    feedback=grade["feedback"],
                    strengths=grade["strengths"],
                    improvements=grade["improvements"],
                    chapter_name=question.category,
                )
                eval_record = evaluation_service.create_evaluation(eval_data)
                question_results.append(
                    _build_question_result(question, student_answer_text, eval_record)
                )
                logger.info(f"Q{question.question_number} auto-graded: {grade['marks_awarded']}/10")

            # ── AI-grade SHORT_ANSWER / LONG_ANSWER ─────────────────────────────
            else:
                if orchestration_svc is None:
                    # Fallback if AI unavailable — give 0 with message
                    logger.warning(f"AI unavailable for Q{question.question_number}, using fallback")
                    eval_data = EvaluationCreate(
                        user_id=current_user.id,
                        test_id=str(test_id),
                        question_id=qid,
                        question=question.question_text,
                        student_answer=student_answer_text or "No answer provided",
                        model_answer=question.model_answer or question.correct_answer or "See textbook for the correct answer",
                        marks_awarded=0,
                        total_marks=10,
                        feedback="AI evaluation service is currently unavailable. Please try again later.",
                        strengths=[],
                        improvements=["AI evaluation pending"],
                        chapter_name=question.category,
                    )
                    eval_record = evaluation_service.create_evaluation(eval_data)
                else:
                    try:
                        eval_record = orchestration_svc.evaluate_and_store(
                            question=question.question_text,
                            student_answer=student_answer_text or "No answer provided",
                            user_id=current_user.id,
                            chapter_name=question.category,
                            test_id=str(test_id),
                            question_id=qid,
                            total_marks=10,
                        )
                        logger.info(f"Q{question.question_number} AI-graded: {eval_record.marks_awarded}/10")
                    except Exception as ai_err:
                        logger.error(f"AI evaluation failed for Q{question.question_number}: {ai_err}")
                        # Fallback evaluation record
                        eval_data = EvaluationCreate(
                            user_id=current_user.id,
                            test_id=str(test_id),
                            question_id=qid,
                            question=question.question_text,
                            student_answer=student_answer_text or "No answer provided",
                            model_answer=question.model_answer or question.correct_answer or "See textbook for the correct answer",
                            marks_awarded=0,
                            total_marks=10,
                            feedback=f"Evaluation could not be completed: {str(ai_err)[:100]}",
                            strengths=[],
                            improvements=["Please retry evaluation"],
                            chapter_name=question.category,
                        )
                        eval_record = evaluation_service.create_evaluation(eval_data)

                question_results.append(
                    _build_question_result(question, student_answer_text, eval_record)
                )

        # ── 5. Mark test as EVALUATED ─────────────────────────────────────────
        try:
            test.status = TestStatus.EVALUATED
            TestRepository.update(db, test)
            logger.info(f"Test {test_id} marked as EVALUATED")
        except Exception as upd_err:
            logger.warning(f"Could not update test status: {upd_err}")

        # ── 6. Build and return summary ───────────────────────────────────────
        # Refresh test to get latest status
        test = TestRepository.get_by_id(db, test_id)
        summary = _build_test_summary(test, question_results)
        summary["evaluated"] = True
        summary["evaluation_count"] = len(question_results)

        logger.info(
            f"Full-test evaluation complete: test={test_id} "
            f"score={summary['total_marks_awarded']}/{summary['total_marks_possible']} "
            f"({summary['percentage']}%)"
        )

        return APIResponse(
            success=True,
            message="Test evaluated successfully",
            data=summary,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Full-test evaluation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Evaluation failed: {str(e)}",
        )
