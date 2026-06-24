"""
Evaluation Repository
Data access layer for Evaluation operations
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.models.evaluation import Evaluation


class EvaluationRepository:
    """
    Repository for Evaluation CRUD operations
    Follows Repository pattern for clean separation of data access
    """
    
    @staticmethod
    def create(db: Session, evaluation: Evaluation) -> Evaluation:
        """
        Create a new evaluation
        
        Args:
            db: Database session
            evaluation: Evaluation object to create
            
        Returns:
            Created Evaluation object
        """
        db.add(evaluation)
        db.commit()
        db.refresh(evaluation)
        return evaluation
    
    @staticmethod
    def get_by_id(db: Session, evaluation_id: UUID) -> Optional[Evaluation]:
        """
        Get evaluation by ID
        
        Args:
            db: Database session
            evaluation_id: Evaluation UUID
            
        Returns:
            Evaluation object or None if not found
        """
        return db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    
    @staticmethod
    def get_by_user(
        db: Session, 
        user_id: int, 
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Evaluation]:
        """
        Get all evaluations for a specific user
        Ordered by created_at descending (newest first)
        
        Args:
            db: Database session
            user_id: User ID
            limit: Maximum number of results (optional)
            offset: Number of results to skip (optional)
            
        Returns:
            List of Evaluation objects
        """
        query = db.query(Evaluation).filter(
            Evaluation.user_id == user_id
        ).order_by(desc(Evaluation.created_at))
        
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
            
        return query.all()
    
    @staticmethod
    def get_by_test(db: Session, test_id: UUID) -> List[Evaluation]:
        """
        Get all evaluations for a specific test
        
        Args:
            db: Database session
            test_id: Test UUID
            
        Returns:
            List of Evaluation objects
        """
        return db.query(Evaluation).filter(
            Evaluation.test_id == test_id
        ).order_by(Evaluation.created_at).all()
    
    @staticmethod
    def get_by_test_and_question(
        db: Session,
        test_id: str, 
        question_id: str
    ) -> Optional[Evaluation]:
        """
        Get evaluation for a specific test question
        
        Args:
            db: Database session
            test_id: Test UUID (as string)
            question_id: Question UUID (as string)
            
        Returns:
            Evaluation object or None if not found
        """
        return db.query(Evaluation).filter(
            Evaluation.test_id == test_id,
            Evaluation.question_id == question_id
        ).first()
    
    @staticmethod
    def get_by_chapter(
        db: Session, 
        user_id: int, 
        chapter_name: str
    ) -> List[Evaluation]:
        """
        Get all evaluations for a specific user and chapter
        
        Args:
            db: Database session
            user_id: User ID
            chapter_name: Chapter/topic name
            
        Returns:
            List of Evaluation objects
        """
        return db.query(Evaluation).filter(
            Evaluation.user_id == user_id,
            Evaluation.chapter_name == chapter_name
        ).order_by(desc(Evaluation.created_at)).all()
    
    @staticmethod
    def get_recent_by_user(
        db: Session, 
        user_id: int, 
        limit: int = 10
    ) -> List[Evaluation]:
        """
        Get most recent evaluations for a user
        
        Args:
            db: Database session
            user_id: User ID
            limit: Number of recent evaluations to fetch
            
        Returns:
            List of Evaluation objects
        """
        return db.query(Evaluation).filter(
            Evaluation.user_id == user_id
        ).order_by(desc(Evaluation.created_at)).limit(limit).all()
    
    @staticmethod
    def get_chapter_statistics(db: Session, user_id: int, chapter_name: str) -> dict:
        """
        Get performance statistics for a specific chapter
        
        Args:
            db: Database session
            user_id: User ID
            chapter_name: Chapter/topic name
            
        Returns:
            Dictionary with chapter statistics
        """
        result = db.query(
            func.count(Evaluation.id).label('total_evaluations'),
            func.sum(Evaluation.marks_awarded).label('total_marks_obtained'),
            func.sum(Evaluation.total_marks).label('total_marks_possible'),
            func.max(Evaluation.created_at).label('latest_evaluation_date')
        ).filter(
            Evaluation.user_id == user_id,
            Evaluation.chapter_name == chapter_name
        ).first()
        
        if not result or result.total_evaluations == 0:
            return {
                'chapter_name': chapter_name,
                'total_evaluations': 0,
                'total_marks_obtained': 0,
                'total_marks_possible': 0,
                'average_percentage': 0.0,
                'latest_evaluation_date': None
            }
        
        average_percentage = 0.0
        if result.total_marks_possible and result.total_marks_possible > 0:
            average_percentage = round(
                (result.total_marks_obtained / result.total_marks_possible) * 100, 2
            )
        
        return {
            'chapter_name': chapter_name,
            'total_evaluations': result.total_evaluations,
            'total_marks_obtained': result.total_marks_obtained or 0,
            'total_marks_possible': result.total_marks_possible or 0,
            'average_percentage': average_percentage,
            'latest_evaluation_date': result.latest_evaluation_date
        }
    
    @staticmethod
    def get_user_statistics(db: Session, user_id: int) -> dict:
        """
        Get overall performance statistics for a user
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Dictionary with user statistics
        """
        result = db.query(
            func.count(Evaluation.id).label('total_evaluations'),
            func.sum(Evaluation.marks_awarded).label('total_marks_obtained'),
            func.sum(Evaluation.total_marks).label('total_marks_possible'),
            func.count(func.distinct(Evaluation.chapter_name)).label('chapters_covered')
        ).filter(
            Evaluation.user_id == user_id
        ).first()
        
        if not result or result.total_evaluations == 0:
            return {
                'user_id': user_id,
                'total_evaluations': 0,
                'total_marks_obtained': 0,
                'total_marks_possible': 0,
                'overall_percentage': 0.0,
                'chapters_covered': 0
            }
        
        overall_percentage = 0.0
        if result.total_marks_possible and result.total_marks_possible > 0:
            overall_percentage = round(
                (result.total_marks_obtained / result.total_marks_possible) * 100, 2
            )
        
        return {
            'user_id': user_id,
            'total_evaluations': result.total_evaluations,
            'total_marks_obtained': result.total_marks_obtained or 0,
            'total_marks_possible': result.total_marks_possible or 0,
            'overall_percentage': overall_percentage,
            'chapters_covered': result.chapters_covered or 0
        }
    
    @staticmethod
    def get_all_chapters_by_user(db: Session, user_id: int) -> List[str]:
        """
        Get list of all unique chapters a user has been evaluated on
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            List of chapter names
        """
        results = db.query(Evaluation.chapter_name).filter(
            Evaluation.user_id == user_id,
            Evaluation.chapter_name.isnot(None)
        ).distinct().all()
        
        return [result.chapter_name for result in results]
    
    @staticmethod
    def update(db: Session, evaluation: Evaluation) -> Evaluation:
        """
        Update evaluation
        
        Args:
            db: Database session
            evaluation: Evaluation object with updated values
            
        Returns:
            Updated Evaluation object
        """
        db.commit()
        db.refresh(evaluation)
        return evaluation
    
    @staticmethod
    def delete(db: Session, evaluation: Evaluation) -> bool:
        """
        Delete evaluation
        
        Args:
            db: Database session
            evaluation: Evaluation object to delete
            
        Returns:
            True if deleted successfully
        """
        db.delete(evaluation)
        db.commit()
        return True
    
    @staticmethod
    def count_by_user(db: Session, user_id: int) -> int:
        """
        Count total evaluations for a user
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Number of evaluations
        """
        return db.query(Evaluation).filter(Evaluation.user_id == user_id).count()
