"""
Test Model
Represents a generated examination for a student
"""
import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from app.models.enums import QuestionType, TestStatus


class Test(Base):
    """
    Test/Examination model
    
    Stores generated examinations for students.
    Supports MCQ, Fill-in-Blanks, Short Answer, and Long Answer questions.
    
    Status workflow: GENERATED → IN_PROGRESS → SUBMITTED → EVALUATED
    
    Future extensibility (Phase 5 - Evaluation):
    - Total marks can be calculated from test_questions
    - Student score will be stored in a separate evaluation table
    - Pass/fail status can be derived from score
    """
    __tablename__ = "tests"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Test metadata
    subject = Column(String(255), nullable=False)  # e.g., "Social Studies"
    question_type = Column(SQLEnum(QuestionType), nullable=False, index=True)
    selected_categories = Column(JSON, nullable=False)  # Array of category IDs or names
    question_count = Column(Integer, nullable=False)  # Number of questions in this test
    
    # Test status
    status = Column(
        SQLEnum(TestStatus), 
        nullable=False, 
        default=TestStatus.GENERATED,
        index=True
    )
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    started_at = Column(DateTime(timezone=True), nullable=True)  # When student starts
    completed_at = Column(DateTime(timezone=True), nullable=True)  # When student submits
    
    # Relationships
    user = relationship("User", back_populates="tests")
    questions = relationship(
        "TestQuestion",
        back_populates="test",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    student_answers = relationship(
        "StudentTestAnswer",
        back_populates="test",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    evaluations = relationship(
        "Evaluation",
        back_populates="test",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Test {self.id} - {self.subject} ({self.question_type}) - Status: {self.status}>"
