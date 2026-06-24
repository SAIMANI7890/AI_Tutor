"""
Evaluation Model
Represents AI-generated evaluation of student answers
"""
import uuid
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Evaluation(Base):
    """
    Evaluation model
    
    Stores comprehensive AI-generated evaluations of student test answers.
    Each evaluation includes:
    - Student's answer
    - Model/ideal answer
    - Marks awarded and total marks
    - Detailed feedback
    - Identified strengths and areas for improvement
    - Chapter/topic context
    
    This model enables:
    - Historical tracking of student performance
    - Progress analytics over time
    - Personalized feedback and recommendations
    - Chapter-wise performance analysis
    
    Relationships:
    - Links to User for student identification
    - Links to Test for exam context (nullable for standalone evaluations)
    - Links to TestQuestion for question details (nullable for standalone evaluations)
    """
    __tablename__ = "evaluations"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign keys
    user_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    test_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("tests.id", ondelete="SET NULL"), 
        nullable=True, 
        index=True
    )
    question_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("test_questions.id", ondelete="SET NULL"), 
        nullable=True, 
        index=True
    )
    
    # Question and answers
    question = Column(Text, nullable=False)
    student_answer = Column(Text, nullable=False)
    model_answer = Column(Text, nullable=False)
    
    # Marks
    marks_awarded = Column(Integer, nullable=False)
    total_marks = Column(Integer, nullable=False)
    
    # Feedback and analysis
    feedback = Column(Text, nullable=False)
    strengths = Column(JSON, nullable=True)  # Array of strength points
    improvements = Column(JSON, nullable=True)  # Array of improvement suggestions
    
    # Context
    chapter_name = Column(String(255), nullable=True, index=True)
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False, 
        index=True
    )
    
    # Relationships
    # 'user' and 'test' are safe — they don't conflict with any column name.
    user = relationship("User", back_populates="evaluations")
    test = relationship("Test", back_populates="evaluations")
    # IMPORTANT: Cannot use 'question' as a relationship name because it conflicts
    # with the 'question' Text column above. TestQuestion.evaluations uses
    # back_populates="test_question_obj" to match this name.
    test_question_obj = relationship("TestQuestion", back_populates="evaluations")


    def __repr__(self):
        return f"<Evaluation {self.id} - User: {self.user_id} - Score: {self.marks_awarded}/{self.total_marks}>"
    
    @property
    def percentage(self) -> float:
        """Calculate percentage score"""
        if self.total_marks == 0:
            return 0.0
        return round((self.marks_awarded / self.total_marks) * 100, 2)
