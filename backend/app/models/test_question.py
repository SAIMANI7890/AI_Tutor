"""
TestQuestion Model
Represents a single question within a test
"""
import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SQLEnum, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from app.models.enums import QuestionType


class TestQuestion(Base):
    """
    Test Question model
    
    Stores individual questions generated for a test.
    Each question belongs to one test.
    
    Question types:
    - MCQ: question_text + options_json (array) + correct_answer (option index/letter)
    - FILL_BLANKS: question_text with _____ + correct_answer (the missing word/phrase)
    - SHORT_ANSWER: question_text + model_answer (reference answer for evaluation)
    - LONG_ANSWER: question_text + model_answer (reference answer for evaluation)
    
    Future extensibility (Phase 5 - Evaluation):
    - marks field can be added for per-question marks allocation
    - difficulty field can be added for adaptive testing
    - bloom_taxonomy field can be added for skill assessment
    """
    __tablename__ = "test_questions"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign keys
    test_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("tests.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    
    # Question metadata
    question_number = Column(Integer, nullable=False)  # Order in the test (1, 2, 3...)
    question_type = Column(SQLEnum(QuestionType), nullable=False)
    
    # Question content
    question_text = Column(Text, nullable=False)  # The actual question
    options_json = Column(JSON, nullable=True)  # For MCQ: ["Option A", "Option B", ...]
    correct_answer = Column(Text, nullable=False)  # Correct answer or model answer
    model_answer = Column(Text, nullable=True)  # Detailed model answer for subjective questions
    
    # Source information (from RAG)
    source_document = Column(String(255), nullable=True)  # PDF filename
    source_page = Column(Integer, nullable=True)  # Page number in PDF
    category = Column(String(255), nullable=False, index=True)  # History, Geography, etc.
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    test = relationship("Test", back_populates="questions")
    student_answers = relationship(
        "StudentTestAnswer",
        back_populates="question",
        cascade="all, delete-orphan"
    )
    evaluations = relationship(
        "Evaluation",
        back_populates="test_question_obj"
    )
    
    def __repr__(self):
        return f"<TestQuestion {self.id} - Q{self.question_number} ({self.question_type})>"
