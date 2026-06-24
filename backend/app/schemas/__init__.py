"""
Schemas package
Pydantic schemas for request/response validation
"""
from app.schemas.user import UserRegister, UserLogin, UserResponse, UserUpdate, TokenResponse
from app.schemas.test import TestCreate, TestUpdate, TestRead, TestSummary
from app.schemas.question import (
    TestQuestionCreate,
    TestQuestionUpdate,
    TestQuestionRead,
    TestQuestionForStudent
)
from app.schemas.answer import (
    StudentAnswerCreate,
    StudentAnswerUpdate,
    StudentAnswerRead,
    StudentAnswerWithQuestion
)
from app.schemas.evaluation import (
    EvaluationCreate,
    EvaluationUpdate,
    EvaluationResponse,
    EvaluationSummary,
    ChapterPerformance,
    UserPerformanceStats,
    EvaluateAnswerRequest,
    EvaluateAnswerResponse,
    BatchEvaluateRequest,
    BatchEvaluateResponse
)

__all__ = [
    # User schemas
    "UserRegister",
    "UserLogin",
    "UserResponse",
    "UserUpdate",
    "TokenResponse",
    # Test schemas
    "TestCreate",
    "TestUpdate",
    "TestRead",
    "TestSummary",
    # Question schemas
    "TestQuestionCreate",
    "TestQuestionUpdate",
    "TestQuestionRead",
    "TestQuestionForStudent",
    # Answer schemas
    "StudentAnswerCreate",
    "StudentAnswerUpdate",
    "StudentAnswerRead",
    "StudentAnswerWithQuestion",
    # Evaluation schemas
    "EvaluationCreate",
    "EvaluationUpdate",
    "EvaluationResponse",
    "EvaluationSummary",
    "ChapterPerformance",
    "UserPerformanceStats",
    "EvaluateAnswerRequest",
    "EvaluateAnswerResponse",
    "BatchEvaluateRequest",
    "BatchEvaluateResponse",
]
