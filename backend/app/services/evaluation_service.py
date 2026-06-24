"""
Evaluation Service
Business logic layer for evaluation operations
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.evaluation import Evaluation
from app.repositories.evaluation_repository import EvaluationRepository
from app.schemas.evaluation import (
    EvaluationCreate, 
    EvaluationResponse, 
    EvaluationSummary,
    ChapterPerformance,
    UserPerformanceStats
)


class EvaluationService:
    """
    Service layer for evaluation-related business logic
    
    Handles:
    - Evaluation creation and validation
    - Fetching user evaluations with filtering
    - Chapter-wise performance analytics
    - Overall user performance statistics
    """
    
    def __init__(self, db: Session):
        """
        Initialize service with database session
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.repository = EvaluationRepository()
    
    def create_evaluation(self, evaluation_data: EvaluationCreate) -> EvaluationResponse:
        """
        Create a new evaluation
        
        Validates:
        - Marks awarded does not exceed total marks
        - User exists (foreign key will handle this)
        - Test and question exist if provided
        
        Args:
            evaluation_data: Evaluation creation data
            
        Returns:
            Created evaluation response
            
        Raises:
            HTTPException: If validation fails
        """
        # Additional validation
        if evaluation_data.marks_awarded > evaluation_data.total_marks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Marks awarded ({evaluation_data.marks_awarded}) cannot exceed total marks ({evaluation_data.total_marks})"
            )
        
        if evaluation_data.marks_awarded < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Marks awarded cannot be negative"
            )
        
        # Create evaluation model
        evaluation = Evaluation(
            user_id=evaluation_data.user_id,
            test_id=evaluation_data.test_id,
            question_id=evaluation_data.question_id,
            question=evaluation_data.question,
            student_answer=evaluation_data.student_answer,
            model_answer=evaluation_data.model_answer,
            marks_awarded=evaluation_data.marks_awarded,
            total_marks=evaluation_data.total_marks,
            feedback=evaluation_data.feedback,
            strengths=evaluation_data.strengths,
            improvements=evaluation_data.improvements,
            chapter_name=evaluation_data.chapter_name
        )
        
        # Save to database
        created_evaluation = self.repository.create(self.db, evaluation)
        
        return EvaluationResponse.model_validate(created_evaluation)
    
    def get_evaluation_by_id(self, evaluation_id: UUID) -> EvaluationResponse:
        """
        Get evaluation by ID
        
        Args:
            evaluation_id: Evaluation UUID
            
        Returns:
            Evaluation response
            
        Raises:
            HTTPException: If evaluation not found
        """
        evaluation = self.repository.get_by_id(self.db, evaluation_id)
        
        if not evaluation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Evaluation with ID {evaluation_id} not found"
            )
        
        return EvaluationResponse.model_validate(evaluation)
    
    def get_user_evaluations(
        self, 
        user_id: int, 
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[EvaluationResponse]:
        """
        Get all evaluations for a user
        
        Args:
            user_id: User ID
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List of evaluation responses
        """
        evaluations = self.repository.get_by_user(self.db, user_id, limit, offset)
        
        return [EvaluationResponse.model_validate(eval) for eval in evaluations]
    
    def get_test_evaluations(self, test_id: UUID) -> List[EvaluationResponse]:
        """
        Get all evaluations for a specific test
        
        Args:
            test_id: Test UUID
            
        Returns:
            List of evaluation responses
        """
        evaluations = self.repository.get_by_test(self.db, test_id)
        
        return [EvaluationResponse.model_validate(eval) for eval in evaluations]
    
    def get_chapter_evaluations(
        self, 
        user_id: int, 
        chapter_name: str
    ) -> List[EvaluationResponse]:
        """
        Get all evaluations for a user in a specific chapter
        
        Args:
            user_id: User ID
            chapter_name: Chapter/topic name
            
        Returns:
            List of evaluation responses
        """
        evaluations = self.repository.get_by_chapter(self.db, user_id, chapter_name)
        
        return [EvaluationResponse.model_validate(eval) for eval in evaluations]
    
    def get_recent_evaluations(
        self, 
        user_id: int, 
        limit: int = 10
    ) -> List[EvaluationSummary]:
        """
        Get recent evaluations for a user
        
        Args:
            user_id: User ID
            limit: Number of recent evaluations
            
        Returns:
            List of evaluation summaries
        """
        evaluations = self.repository.get_recent_by_user(self.db, user_id, limit)
        
        return [EvaluationSummary.model_validate(eval) for eval in evaluations]
    
    def get_chapter_performance(
        self, 
        user_id: int, 
        chapter_name: str
    ) -> ChapterPerformance:
        """
        Get performance statistics for a specific chapter
        
        Args:
            user_id: User ID
            chapter_name: Chapter/topic name
            
        Returns:
            Chapter performance statistics
        """
        stats = self.repository.get_chapter_statistics(self.db, user_id, chapter_name)
        
        return ChapterPerformance(**stats)
    
    def get_all_chapters_performance(self, user_id: int) -> List[ChapterPerformance]:
        """
        Get performance statistics for all chapters a user has been evaluated on
        
        Args:
            user_id: User ID
            
        Returns:
            List of chapter performance statistics
        """
        chapters = self.repository.get_all_chapters_by_user(self.db, user_id)
        
        chapter_stats = []
        for chapter in chapters:
            stats = self.repository.get_chapter_statistics(self.db, user_id, chapter)
            chapter_stats.append(ChapterPerformance(**stats))
        
        return chapter_stats
    
    def get_user_performance_stats(self, user_id: int) -> UserPerformanceStats:
        """
        Get overall performance statistics for a user
        
        Args:
            user_id: User ID
            
        Returns:
            User performance statistics including recent evaluations
        """
        stats = self.repository.get_user_statistics(self.db, user_id)
        recent = self.get_recent_evaluations(user_id, limit=5)
        
        return UserPerformanceStats(
            user_id=stats['user_id'],
            total_evaluations=stats['total_evaluations'],
            total_marks_obtained=stats['total_marks_obtained'],
            total_marks_possible=stats['total_marks_possible'],
            overall_percentage=stats['overall_percentage'],
            chapters_covered=stats['chapters_covered'],
            recent_evaluations=recent
        )
    
    def delete_evaluation(self, evaluation_id: UUID, user_id: int) -> bool:
        """
        Delete an evaluation
        
        Ensures user can only delete their own evaluations
        
        Args:
            evaluation_id: Evaluation UUID
            user_id: User ID (for authorization)
            
        Returns:
            True if deleted successfully
            
        Raises:
            HTTPException: If evaluation not found or unauthorized
        """
        evaluation = self.repository.get_by_id(self.db, evaluation_id)
        
        if not evaluation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Evaluation with ID {evaluation_id} not found"
            )
        
        # Authorization check
        if evaluation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this evaluation"
            )
        
        return self.repository.delete(self.db, evaluation)
    
    def count_user_evaluations(self, user_id: int) -> int:
        """
        Count total evaluations for a user
        
        Args:
            user_id: User ID
            
        Returns:
            Number of evaluations
        """
        return self.repository.count_by_user(self.db, user_id)


def get_evaluation_service(db: Session) -> EvaluationService:
    """
    Factory function to create EvaluationService instance
    
    Args:
        db: Database session
        
    Returns:
        EvaluationService instance
    """
    return EvaluationService(db)
