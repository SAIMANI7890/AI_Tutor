"""
StudentTestAnswer Repository
Data access layer for StudentTestAnswer operations
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.student_test_answer import StudentTestAnswer


class StudentAnswerRepository:
    """
    Repository for StudentTestAnswer CRUD operations
    Follows Repository pattern for clean separation of data access
    """
    
    @staticmethod
    def create(db: Session, answer: StudentTestAnswer) -> StudentTestAnswer:
        """
        Create a new student answer
        
        Args:
            db: Database session
            answer: StudentTestAnswer object to create
            
        Returns:
            Created StudentTestAnswer object
        """
        db.add(answer)
        db.commit()
        db.refresh(answer)
        return answer
    
    @staticmethod
    def get_by_id(db: Session, answer_id: UUID) -> Optional[StudentTestAnswer]:
        """
        Get answer by ID
        
        Args:
            db: Database session
            answer_id: Answer UUID
            
        Returns:
            StudentTestAnswer object or None if not found
        """
        return db.query(StudentTestAnswer).filter(
            StudentTestAnswer.id == answer_id
        ).first()
    
    @staticmethod
    def get_by_test(db: Session, test_id: UUID) -> List[StudentTestAnswer]:
        """
        Get all answers for a specific test
        
        Args:
            db: Database session
            test_id: Test UUID
            
        Returns:
            List of StudentTestAnswer objects
        """
        return db.query(StudentTestAnswer).filter(
            StudentTestAnswer.test_id == test_id
        ).all()
    
    @staticmethod
    def get_by_test_and_question(
        db: Session, 
        test_id: UUID, 
        question_id: UUID
    ) -> Optional[StudentTestAnswer]:
        """
        Get answer for a specific question in a test
        Used to check if student already answered this question
        
        Args:
            db: Database session
            test_id: Test UUID
            question_id: Question UUID
            
        Returns:
            StudentTestAnswer object or None if not found
        """
        return db.query(StudentTestAnswer).filter(
            StudentTestAnswer.test_id == test_id,
            StudentTestAnswer.question_id == question_id
        ).first()
    
    @staticmethod
    def update(db: Session, answer: StudentTestAnswer) -> StudentTestAnswer:
        """
        Update student answer
        
        Args:
            db: Database session
            answer: StudentTestAnswer object with updated values
            
        Returns:
            Updated StudentTestAnswer object
        """
        db.commit()
        db.refresh(answer)
        return answer
    
    @staticmethod
    def upsert(
        db: Session, 
        test_id: UUID, 
        question_id: UUID, 
        student_answer: Optional[str]
    ) -> StudentTestAnswer:
        """
        Create or update answer (upsert operation) - ATOMIC
        Uses PostgreSQL ON CONFLICT to prevent race conditions
        
        Args:
            db: Database session
            test_id: Test UUID
            question_id: Question UUID
            student_answer: Student's answer text
            
        Returns:
            StudentTestAnswer object
        """
        from sqlalchemy.dialects.postgresql import insert
        from datetime import datetime, timezone
        
        # Prepare statement with ON CONFLICT clause
        stmt = insert(StudentTestAnswer).values(
            test_id=test_id,
            question_id=question_id,
            student_answer=student_answer,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ).on_conflict_do_update(
            # Conflict target: unique constraint on (test_id, question_id)
            index_elements=['test_id', 'question_id'],
            # Update values on conflict
            set_={
                'student_answer': student_answer,
                'updated_at': datetime.now(timezone.utc)
            }
        ).returning(StudentTestAnswer)
        
        # Execute and fetch result
        result = db.execute(stmt)
        db.commit()
        
        # Get the upserted record
        answer = result.fetchone()
        if answer:
            return answer[0]
        
        # Fallback: Query the record (should not happen)
        return StudentAnswerRepository.get_by_test_and_question(db, test_id, question_id)
    
    @staticmethod
    def delete(db: Session, answer: StudentTestAnswer) -> bool:
        """
        Delete answer
        
        Args:
            db: Database session
            answer: StudentTestAnswer object to delete
            
        Returns:
            True if deleted successfully
        """
        db.delete(answer)
        db.commit()
        return True
    
    @staticmethod
    def count_answered(db: Session, test_id: UUID) -> int:
        """
        Count how many questions student has answered in a test
        (Excludes null/empty answers)
        
        Args:
            db: Database session
            test_id: Test UUID
            
        Returns:
            Number of answered questions
        """
        return db.query(StudentTestAnswer).filter(
            StudentTestAnswer.test_id == test_id,
            StudentTestAnswer.student_answer.isnot(None),
            StudentTestAnswer.student_answer != ""
        ).count()
    
    @staticmethod
    def delete_by_test(db: Session, test_id: UUID) -> int:
        """
        Delete all answers for a test
        Used for test reset functionality
        
        Args:
            db: Database session
            test_id: Test UUID
            
        Returns:
            Number of answers deleted
        """
        count = db.query(StudentTestAnswer).filter(
            StudentTestAnswer.test_id == test_id
        ).delete()
        db.commit()
        return count
