"""
Evaluation Orchestration Service
Orchestrates AI evaluation and database storage
"""
from typing import Dict, Any
import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.services.ai_evaluation_service import AIEvaluationService
from app.services.evaluation_service import EvaluationService
from app.schemas.evaluation import EvaluationCreate, EvaluationResponse

logger = logging.getLogger(__name__)


class EvaluationOrchestrationService:
    """
    Service that orchestrates the complete evaluation workflow:
    1. Retrieve textbook content using RAG
    2. Generate model answer
    3. Evaluate student answer
    4. Store evaluation in database
    5. Return structured response
    """
    
    def __init__(
        self,
        ai_evaluation_service: AIEvaluationService,
        db: Session
    ):
        """
        Initialize orchestration service
        
        Args:
            ai_evaluation_service: AI evaluation service instance
            db: Database session
        """
        self.ai_service = ai_evaluation_service
        self.db_service = EvaluationService(db)
    
    def evaluate_and_store(
        self,
        question: str,
        student_answer: str,
        user_id: int,
        chapter_name: str = None,
        test_id: str = None,
        question_id: str = None,
        total_marks: int = 5
    ) -> EvaluationResponse:
        """
        Complete evaluation workflow with database storage
        
        Args:
            question: The question asked
            student_answer: Student's submitted answer
            user_id: User ID of the student
            chapter_name: Optional chapter name for context
            test_id: Optional test UUID if part of an exam
            question_id: Optional question UUID if part of an exam
            total_marks: Total marks for the question
            
        Returns:
            Complete evaluation response
            
        Raises:
            HTTPException: If evaluation or storage fails
        """
        try:
            # Validate inputs
            if not question or not question.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Question cannot be empty"
                )
            
            if not student_answer or not student_answer.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Student answer cannot be empty"
                )
            
            if total_marks <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Total marks must be greater than 0"
                )
            
            logger.info(f"Starting evaluation for user {user_id}")
            
            # Step 1-3: AI Evaluation with RAG
            try:
                evaluation_result = self.ai_service.evaluate_with_rag(
                    question=question.strip(),
                    student_answer=student_answer.strip(),
                    chapter_name=chapter_name,
                    total_marks=total_marks
                )
            except ValueError as e:
                # RAG-related errors (no context found, etc.)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )
            except Exception as e:
                logger.error(f"AI evaluation failed: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"AI evaluation failed: {str(e)}"
                )
            
            # Step 4: Store in database
            try:
                evaluation_data = EvaluationCreate(
                    user_id=user_id,
                    test_id=test_id,
                    question_id=question_id,
                    question=question.strip(),
                    student_answer=student_answer.strip(),
                    model_answer=evaluation_result["model_answer"],
                    marks_awarded=evaluation_result["marks_awarded"],
                    total_marks=evaluation_result["total_marks"],
                    feedback=evaluation_result["feedback"],
                    strengths=evaluation_result.get("strengths", []),
                    improvements=evaluation_result.get("improvements", []),
                    chapter_name=chapter_name
                )
                
                evaluation_response = self.db_service.create_evaluation(evaluation_data)
                
                logger.info(
                    f"Evaluation stored: {evaluation_response.id}, "
                    f"{evaluation_response.marks_awarded}/{evaluation_response.total_marks} marks"
                )
                
                return evaluation_response
                
            except HTTPException as e:
                # Re-raise HTTP exceptions from service layer
                raise e
            except Exception as e:
                logger.error(f"Database storage failed: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to store evaluation: {str(e)}"
                )
            
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as e:
            logger.error(f"Unexpected error in evaluation workflow: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Evaluation failed: {str(e)}"
            )
    
    def batch_evaluate(
        self,
        evaluations: list[Dict[str, Any]],
        user_id: int
    ) -> list[EvaluationResponse]:
        """
        Evaluate multiple questions in batch
        
        Args:
            evaluations: List of evaluation requests
            user_id: User ID
            
        Returns:
            List of evaluation responses
        """
        results = []
        errors = []
        
        for i, eval_request in enumerate(evaluations, start=1):
            try:
                result = self.evaluate_and_store(
                    question=eval_request["question"],
                    student_answer=eval_request["student_answer"],
                    user_id=user_id,
                    chapter_name=eval_request.get("chapter_name"),
                    test_id=eval_request.get("test_id"),
                    question_id=eval_request.get("question_id"),
                    total_marks=eval_request.get("total_marks", 5)
                )
                results.append(result)
                logger.info(f"Batch evaluation {i}/{len(evaluations)} completed")
            except HTTPException as e:
                error_msg = f"Question {i}: {e.detail}"
                errors.append(error_msg)
                logger.error(error_msg)
            except Exception as e:
                error_msg = f"Question {i}: {str(e)}"
                errors.append(error_msg)
                logger.error(f"Unexpected error in batch evaluation: {e}")
        
        if errors and not results:
            # All evaluations failed
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Batch evaluation failed: {'; '.join(errors)}"
            )
        
        if errors:
            logger.warning(f"Batch evaluation completed with {len(errors)} errors: {errors}")
        
        return results


def create_orchestration_service(
    ai_evaluation_service: AIEvaluationService,
    db: Session
) -> EvaluationOrchestrationService:
    """
    Factory function to create evaluation orchestration service
    
    Args:
        ai_evaluation_service: AI evaluation service instance
        db: Database session
        
    Returns:
        EvaluationOrchestrationService instance
    """
    return EvaluationOrchestrationService(ai_evaluation_service, db)
