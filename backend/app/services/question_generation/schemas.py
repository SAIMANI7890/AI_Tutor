"""
Schemas for Question Generation Service
Input/output data structures
"""
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from app.models.enums import QuestionType


class ExamGenerationRequest(BaseModel):
    """Request schema for generating an exam"""
    user_id: int = Field(..., description="User ID who is generating the exam")
    subject: str = Field(..., description="Subject name (e.g., Social Studies)")
    question_type: QuestionType = Field(..., description="Type of questions to generate")
    selected_categories: List[str] = Field(
        ..., 
        min_length=1,
        description="Categories to include (History, Geography, Politics, Economics)"
    )
    question_count: int = Field(..., ge=1, le=10, description="Number of questions (1-10)")
    
    @field_validator('question_count')
    @classmethod
    def validate_question_count(cls, v):
        """Validate question count"""
        if v < 1:
            raise ValueError('Question count must be at least 1')
        if v > 10:
            raise ValueError('Question count cannot exceed 10')
        return v
    
    @field_validator('selected_categories')
    @classmethod
    def validate_categories(cls, v):
        """Validate selected categories"""
        if not v:
            raise ValueError('At least one category must be selected')
        
        valid_categories = {'History', 'Geography', 'Politics', 'Economics'}
        for category in v:
            if category not in valid_categories:
                raise ValueError(f'Invalid category: {category}. Must be one of {valid_categories}')
        
        return v
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "subject": "Social Studies",
                "question_type": "MCQ",
                "selected_categories": ["History", "Geography"],
                "question_count": 5
            }
        }


class GeneratedQuestion(BaseModel):
    """Single generated question"""
    question_type: QuestionType
    question_text: str
    options: Optional[List[str]] = None  # For MCQ only
    correct_answer: str
    model_answer: Optional[str] = None  # For subjective questions
    source_document: Optional[str] = None
    source_page: Optional[int] = None
    category: str
    
    class Config:
        from_attributes = True


class ExamGenerationResponse(BaseModel):
    """Response schema for generated exam"""
    test_id: str  # UUID as string
    user_id: int
    subject: str
    question_type: QuestionType
    question_count: int
    questions: List[GeneratedQuestion]
    status: str
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "test_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": 1,
                "subject": "Social Studies",
                "question_type": "MCQ",
                "question_count": 5,
                "questions": [
                    {
                        "question_type": "MCQ",
                        "question_text": "What is democracy?",
                        "options": ["A", "B", "C", "D"],
                        "correct_answer": "A",
                        "model_answer": None,
                        "source_document": "social_politics.pdf",
                        "source_page": 15,
                        "category": "Politics"
                    }
                ],
                "status": "GENERATED"
            }
        }
