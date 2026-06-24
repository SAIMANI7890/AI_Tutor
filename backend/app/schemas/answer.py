"""
Pydantic Schemas for Student Test Answers
"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


# Request Schemas
class StudentAnswerCreate(BaseModel):
    """Schema for creating/saving a student answer"""
    test_id: UUID = Field(..., description="Test ID")
    question_id: UUID = Field(..., description="Question ID")
    student_answer: Optional[str] = Field(None, description="Student's answer (can be null for unanswered)")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "test_id": "123e4567-e89b-12d3-a456-426614174000",
                "question_id": "234e5678-e89b-12d3-a456-426614174001",
                "student_answer": "A"
            }
        }


class StudentAnswerUpdate(BaseModel):
    """Schema for updating a student answer"""
    student_answer: Optional[str] = Field(None, description="Updated answer")
    
    class Config:
        from_attributes = True


# Response Schemas
class StudentAnswerRead(BaseModel):
    """Schema for reading student answer data"""
    id: UUID
    test_id: UUID
    question_id: UUID
    student_answer: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StudentAnswerWithQuestion(BaseModel):
    """
    Schema for student answer with question details
    Used for displaying student's responses with questions
    """
    id: UUID
    test_id: UUID
    question_id: UUID
    student_answer: Optional[str]
    question_number: int
    question_text: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
