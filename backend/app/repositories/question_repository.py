"""
TestQuestion Repository
Data access layer for TestQuestion operations
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import asc
from app.models.test_question import TestQuestion


class TestQuestionRepository:
    """
    Repository for TestQuestion CRUD operations
    Follows Repository pattern for clean separation of data access
    """
    
    @staticmethod
    def create(db: Session, question: TestQuestion) -> TestQuestion:
        """
        Create a new test question
        
        Args:
            db: Database session
            question: TestQuestion object to create
            
        Returns:
            Created TestQuestion object
        """
        db.add(question)
        db.commit()
        db.refresh(question)
        return question
    
    @staticmethod
    def create_bulk(db: Session, questions: List[TestQuestion]) -> List[TestQuestion]:
        """
        Create multiple questions in bulk (for test generation)
        More efficient than creating one by one
        
        Args:
            db: Database session
            questions: List of TestQuestion objects
            
        Returns:
            List of created TestQuestion objects
        """
        db.add_all(questions)
        db.commit()
        for question in questions:
            db.refresh(question)
        return questions
    
    @staticmethod
    def get_by_id(db: Session, question_id: UUID) -> Optional[TestQuestion]:
        """
        Get question by ID
        
        Args:
            db: Database session
            question_id: Question UUID
            
        Returns:
            TestQuestion object or None if not found
        """
        return db.query(TestQuestion).filter(
            TestQuestion.id == question_id
        ).first()
    
    @staticmethod
    def get_by_test(db: Session, test_id: UUID) -> List[TestQuestion]:
        """
        Get all questions for a specific test
        Ordered by question_number ascending
        
        Args:
            db: Database session
            test_id: Test UUID
            
        Returns:
            List of TestQuestion objects
        """
        return db.query(TestQuestion).filter(
            TestQuestion.test_id == test_id
        ).order_by(asc(TestQuestion.question_number)).all()
    
    @staticmethod
    def get_by_test_and_number(
        db: Session, 
        test_id: UUID, 
        question_number: int
    ) -> Optional[TestQuestion]:
        """
        Get specific question by test and question number
        
        Args:
            db: Database session
            test_id: Test UUID
            question_number: Question number (1, 2, 3, ...)
            
        Returns:
            TestQuestion object or None if not found
        """
        return db.query(TestQuestion).filter(
            TestQuestion.test_id == test_id,
            TestQuestion.question_number == question_number
        ).first()
    
    @staticmethod
    def update(db: Session, question: TestQuestion) -> TestQuestion:
        """
        Update question
        
        Args:
            db: Database session
            question: TestQuestion object with updated values
            
        Returns:
            Updated TestQuestion object
        """
        db.commit()
        db.refresh(question)
        return question
    
    @staticmethod
    def delete(db: Session, question: TestQuestion) -> bool:
        """
        Delete question
        
        Args:
            db: Database session
            question: TestQuestion object to delete
            
        Returns:
            True if deleted successfully
        """
        db.delete(question)
        db.commit()
        return True
    
    @staticmethod
    def count_by_test(db: Session, test_id: UUID) -> int:
        """
        Count questions in a test
        
        Args:
            db: Database session
            test_id: Test UUID
            
        Returns:
            Number of questions
        """
        return db.query(TestQuestion).filter(
            TestQuestion.test_id == test_id
        ).count()

    @staticmethod
    def delete_by_test(db: Session, test_id: UUID) -> int:
        """
        Delete all questions for a test
        Used when deleting a test
        
        Args:
            db: Database session
            test_id: Test UUID
            
        Returns:
            Number of questions deleted
        """
        count = db.query(TestQuestion).filter(
            TestQuestion.test_id == test_id
        ).delete()
        db.commit()
        return count
