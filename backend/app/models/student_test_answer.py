"""
StudentTestAnswer Model
Represents a student's answer to a test question
"""
import uuid
from sqlalchemy import Column, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class StudentTestAnswer(Base):
    """
    Student Test Answer model
    
    Stores student responses to test questions.
    One answer per question per student.
    
    Answer format:
    - MCQ: "A" or "B" or "C" or "D" (the selected option)
    - FILL_BLANKS: "the missing word or phrase"
    - SHORT_ANSWER: Student's short answer text
    - LONG_ANSWER: Student's essay/long answer text
    
    Future extensibility (Phase 5 - Evaluation):
    - marks_obtained field can be added
    - feedback field can be added (AI-generated feedback)
    - evaluation_status field can be added (PENDING, EVALUATED)
    - evaluated_at timestamp can be added
    - evaluated_by (AI/Teacher) can be added
    
    This separation allows:
    1. Students to save/update answers before submission
    2. Partial test completion
    3. Easy extension for evaluation without schema redesign
    """
    __tablename__ = "student_test_answers"
    __table_args__ = (
        # UNIQUE CONSTRAINT: One answer per question per test
        # Prevents duplicate answers and enables atomic upsert
        UniqueConstraint('test_id', 'question_id', name='uq_test_question_answer'),
    )
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign keys
    test_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("tests.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    question_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("test_questions.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    
    # Student's answer
    student_answer = Column(Text, nullable=True)  # Nullable to allow saving before answering
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )
    
    # Relationships
    test = relationship("Test", back_populates="student_answers")
    question = relationship("TestQuestion", back_populates="student_answers")
    
    def __repr__(self):
        return f"<StudentTestAnswer {self.id} - Test: {self.test_id} Q: {self.question_id}>"
