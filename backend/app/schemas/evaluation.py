"""
Pydantic Schemas for Evaluation
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field, field_validator


# Request Schemas
class EvaluationCreate(BaseModel):
    """Schema for creating a new evaluation"""
    user_id: int = Field(..., description="User ID of the student")
    test_id: Optional[str] = Field(None, description="Test ID (nullable for standalone evaluations)")
    question_id: Optional[str] = Field(None, description="Question ID (nullable for standalone evaluations)")
    question: str = Field(..., min_length=1, description="The question text")
    student_answer: str = Field(..., min_length=1, description="Student's answer text")
    model_answer: str = Field(..., min_length=1, description="Model/ideal answer text")
    marks_awarded: int = Field(..., ge=0, description="Marks awarded to the student")
    total_marks: int = Field(..., gt=0, description="Total marks for the question")
    feedback: str = Field(..., min_length=1, description="Detailed AI-generated feedback")
    strengths: Optional[List[str]] = Field(None, description="List of identified strengths")
    improvements: Optional[List[str]] = Field(None, description="List of improvement suggestions")
    chapter_name: Optional[str] = Field(None, max_length=255, description="Chapter/topic name")
    
    @field_validator('marks_awarded')
    @classmethod
    def validate_marks_awarded(cls, v, info):
        """Validate marks_awarded does not exceed total_marks"""
        # Note: total_marks is in info.data if it was validated before this field
        total_marks = info.data.get('total_marks')
        if total_marks is not None and v > total_marks:
            raise ValueError(f'marks_awarded ({v}) cannot exceed total_marks ({total_marks})')
        return v
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "test_id": "123e4567-e89b-12d3-a456-426614174000",
                "question_id": "234e5678-e89b-12d3-a456-426614174001",
                "question": "Explain the causes of World War I",
                "student_answer": "World War I was caused by the assassination of Archduke Franz Ferdinand...",
                "model_answer": "World War I resulted from a complex interplay of factors including...",
                "marks_awarded": 8,
                "total_marks": 10,
                "feedback": "Good understanding of the immediate trigger. Consider exploring underlying tensions...",
                "strengths": [
                    "Correctly identified the assassination as immediate cause",
                    "Clear and well-structured response"
                ],
                "improvements": [
                    "Could elaborate on alliance systems",
                    "Add more details about economic factors"
                ],
                "chapter_name": "World History - World War I"
            }
        }


class EvaluationUpdate(BaseModel):
    """Schema for updating an evaluation (partial updates)"""
    marks_awarded: Optional[int] = Field(None, ge=0, description="Updated marks awarded")
    feedback: Optional[str] = Field(None, min_length=1, description="Updated feedback")
    strengths: Optional[List[str]] = Field(None, description="Updated strengths")
    improvements: Optional[List[str]] = Field(None, description="Updated improvements")
    
    class Config:
        from_attributes = True


# Response Schemas
class EvaluationResponse(BaseModel):
    """Schema for reading evaluation data"""
    id: UUID
    user_id: int
    test_id: Optional[UUID]
    question_id: Optional[UUID]
    question: str
    student_answer: str
    model_answer: str
    marks_awarded: int
    total_marks: int
    feedback: str
    strengths: Optional[List[str]]
    improvements: Optional[List[str]]
    chapter_name: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class EvaluationSummary(BaseModel):
    """Schema for evaluation summary (without full text content)"""
    id: UUID
    user_id: int
    test_id: Optional[UUID]
    question_id: Optional[UUID]
    marks_awarded: int
    total_marks: int
    chapter_name: Optional[str]
    created_at: datetime
    
    @property
    def percentage(self) -> float:
        """Calculate percentage score"""
        if self.total_marks == 0:
            return 0.0
        return round((self.marks_awarded / self.total_marks) * 100, 2)
    
    class Config:
        from_attributes = True


class ChapterPerformance(BaseModel):
    """Schema for chapter-wise performance analysis"""
    chapter_name: str
    total_evaluations: int
    total_marks_obtained: int
    total_marks_possible: int
    average_percentage: float
    latest_evaluation_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserPerformanceStats(BaseModel):
    """Schema for overall user performance statistics"""
    user_id: int
    total_evaluations: int
    total_marks_obtained: int
    total_marks_possible: int
    overall_percentage: float
    chapters_covered: int
    recent_evaluations: List[EvaluationSummary]
    
    class Config:
        from_attributes = True


# API Request/Response Schemas
class EvaluateAnswerRequest(BaseModel):
    """Schema for evaluation request"""
    question: str = Field(..., min_length=1, description="The question to evaluate")
    student_answer: str = Field(..., min_length=1, description="Student's answer")
    chapter_name: Optional[str] = Field(None, max_length=255, description="Chapter/topic name")
    test_id: Optional[UUID] = Field(None, description="Test ID if part of an exam")
    question_id: Optional[UUID] = Field(None, description="Question ID if part of an exam")
    total_marks: int = Field(5, ge=1, le=100, description="Total marks for the question")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "question": "What is democracy?",
                "student_answer": "Democracy is a form of government where people elect their leaders.",
                "chapter_name": "Democracy",
                "total_marks": 5
            }
        }


class EvaluateAnswerResponse(BaseModel):
    """Schema for evaluation response with all details"""
    evaluation_id: UUID
    question: str
    student_answer: str
    model_answer: str
    marks_awarded: int
    total_marks: int
    feedback: str
    strengths: List[str]
    improvements: List[str]
    chapter_name: Optional[str]
    created_at: datetime
    percentage: Optional[float] = None
    
    @property
    def calculated_percentage(self) -> float:
        """Calculate percentage score"""
        if self.total_marks == 0:
            return 0.0
        return round((self.marks_awarded / self.total_marks) * 100, 2)
    
    class Config:
        from_attributes = True


class BatchEvaluateRequest(BaseModel):
    """Schema for batch evaluation request"""
    evaluations: List[Dict[str, Any]] = Field(
        ..., 
        min_length=1,
        description="List of evaluation requests"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "evaluations": [
                    {
                        "question": "What is democracy?",
                        "student_answer": "A form of government by the people",
                        "chapter_name": "Democracy",
                        "total_marks": 5
                    },
                    {
                        "question": "Name three features of democracy",
                        "student_answer": "Elections, freedom of speech, rule of law",
                        "chapter_name": "Democracy",
                        "total_marks": 5
                    }
                ]
            }
        }


class BatchEvaluateResponse(BaseModel):
    """Schema for batch evaluation response"""
    evaluations: List[EvaluateAnswerResponse]
    total_count: int
    successful_count: int
    failed_count: int
    errors: List[str] = []
    
    class Config:
        from_attributes = True
