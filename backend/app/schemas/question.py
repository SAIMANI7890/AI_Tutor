"""
Pydantic Schemas for Test Questions
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from app.models.enums import QuestionType


# Request Schemas
class TestQuestionCreate(BaseModel):
    """Schema for creating a test question"""
    test_id: UUID = Field(..., description="Test this question belongs to")
    question_number: int = Field(..., ge=1, description="Question order in the test")
    question_type: QuestionType = Field(..., description="Type of question")
    question_text: str = Field(..., min_length=1, description="The question text")
    options_json: Optional[List[str]] = Field(None, description="Options for MCQ (array of strings)")
    correct_answer: str = Field(..., min_length=1, description="Correct answer or model answer")
    model_answer: Optional[str] = Field(None, description="Detailed model answer for evaluation")
    source_document: Optional[str] = Field(None, max_length=255, description="Source PDF filename")
    source_page: Optional[int] = Field(None, ge=1, description="Page number in source document")
    category: str = Field(..., min_length=1, max_length=255, description="Category (History, Geography, etc.)")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "test_id": "123e4567-e89b-12d3-a456-426614174000",
                "question_number": 1,
                "question_type": "MCQ",
                "question_text": "What is democracy?",
                "options_json": [
                    "A form of government where power is held by the people",
                    "A form of government ruled by a king",
                    "A form of government ruled by military",
                    "A form of government ruled by religious leaders"
                ],
                "correct_answer": "A",
                "model_answer": "Democracy is a form of government where power is held by the people...",
                "source_document": "social_politics.pdf",
                "source_page": 15,
                "category": "Politics"
            }
        }


class TestQuestionUpdate(BaseModel):
    """Schema for updating a test question"""
    question_text: Optional[str] = Field(None, min_length=1)
    options_json: Optional[List[str]] = None
    correct_answer: Optional[str] = Field(None, min_length=1)
    model_answer: Optional[str] = None
    
    class Config:
        from_attributes = True


# Response Schemas
class TestQuestionRead(BaseModel):
    """Schema for reading test question data"""
    id: UUID
    test_id: UUID
    question_number: int
    question_type: QuestionType
    question_text: str
    options_json: Optional[List[str]]
    correct_answer: str
    model_answer: Optional[str]
    source_document: Optional[str]
    source_page: Optional[int]
    category: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class TestQuestionForStudent(BaseModel):
    """
    Schema for student view (without correct answer)
    Used when serving questions to students during test
    """
    id: UUID
    question_number: int
    question_type: QuestionType
    question_text: str
    options_json: Optional[List[str]]  # For MCQ only
    category: str
    
    class Config:
        from_attributes = True
