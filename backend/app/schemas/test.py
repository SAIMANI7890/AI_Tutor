"""
Pydantic Schemas for Test/Examination
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from app.models.enums import QuestionType, TestStatus


# Request Schemas
class TestCreate(BaseModel):
    """Schema for creating a new test"""
    subject: str = Field(..., min_length=1, max_length=255, description="Subject name (e.g., Social Studies)")
    question_type: QuestionType = Field(..., description="Type of questions in the test")
    selected_categories: List[str] = Field(..., min_length=1, description="Categories/chapters to include")
    question_count: int = Field(..., ge=1, le=10, description="Number of questions (1-10)")
    
    @field_validator('question_count')
    @classmethod
    def validate_question_count(cls, v):
        """Validate question count is positive and reasonable"""
        if v < 1:
            raise ValueError('Question count must be at least 1')
        if v > 10:
            raise ValueError('Question count cannot exceed 10')
        return v
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "subject": "Social Studies",
                "question_type": "MCQ",
                "selected_categories": ["History", "Geography"],
                "question_count": 5
            }
        }


class TestUpdate(BaseModel):
    """Schema for updating test status"""
    status: TestStatus = Field(..., description="New test status")
    started_at: Optional[datetime] = Field(None, description="When student started the test")
    completed_at: Optional[datetime] = Field(None, description="When student completed the test")
    
    class Config:
        from_attributes = True


# Response Schemas
class TestRead(BaseModel):
    """Schema for reading test data"""
    id: UUID
    user_id: int
    subject: str
    question_type: QuestionType
    selected_categories: List[str]
    question_count: int
    status: TestStatus
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class TestSummary(BaseModel):
    """Schema for test summary (without questions)"""
    id: UUID
    subject: str
    question_type: QuestionType
    question_count: int
    status: TestStatus
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True
