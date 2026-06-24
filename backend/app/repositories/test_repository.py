"""
Test Repository
Data access layer for Test operations
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.test import Test
from app.models.enums import TestStatus


class TestRepository:
    """
    Repository for Test CRUD operations
    Follows Repository pattern for clean separation of data access
    """
    
    @staticmethod
    def create(db: Session, test: Test) -> Test:
        """
        Create a new test
        
        Args:
            db: Database session
            test: Test object to create
            
        Returns:
            Created Test object
        """
        db.add(test)
        db.commit()
        db.refresh(test)
        return test
    
    @staticmethod
    def get_by_id(db: Session, test_id: UUID) -> Optional[Test]:
        """
        Get test by ID
        
        Args:
            db: Database session
            test_id: Test UUID
            
        Returns:
            Test object or None if not found
        """
        return db.query(Test).filter(Test.id == test_id).first()
    
    @staticmethod
    def get_by_user(db: Session, user_id: int) -> List[Test]:
        """
        Get all tests for a specific user
        Ordered by created_at descending (newest first)
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            List of Test objects
        """
        return db.query(Test).filter(
            Test.user_id == user_id
        ).order_by(desc(Test.created_at)).all()
    
    @staticmethod
    def get_by_user_and_status(
        db: Session, 
        user_id: int, 
        status: TestStatus
    ) -> List[Test]:
        """
        Get tests by user and status
        
        Args:
            db: Database session
            user_id: User ID
            status: Test status
            
        Returns:
            List of Test objects
        """
        return db.query(Test).filter(
            Test.user_id == user_id,
            Test.status == status
        ).order_by(desc(Test.created_at)).all()
    
    @staticmethod
    def update(db: Session, test: Test) -> Test:
        """
        Update test
        
        Args:
            db: Database session
            test: Test object with updated values
            
        Returns:
            Updated Test object
        """
        db.commit()
        db.refresh(test)
        return test
    
    @staticmethod
    def delete(db: Session, test: Test) -> bool:
        """
        Delete test (cascade deletes questions and answers)
        
        Args:
            db: Database session
            test: Test object to delete
            
        Returns:
            True if deleted successfully
        """
        db.delete(test)
        db.commit()
        return True
    
    @staticmethod
    def count_by_user(db: Session, user_id: int) -> int:
        """
        Count total tests for a user
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Number of tests
        """
        return db.query(Test).filter(Test.user_id == user_id).count()
