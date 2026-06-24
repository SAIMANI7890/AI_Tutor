"""
Exam API Schemas - Phase 4C
Pydantic request and response models for examination endpoints.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.models.enums import QuestionType

# ---------------------------------------------------------------------------
# Allowed values
# ---------------------------------------------------------------------------
VALID_CATEGORIES = {"History", "Geography", "Politics", "Economics"}
VALID_QUESTION_TYPES = {qt.value for qt in QuestionType}


# ===========================================================================
# REQUEST SCHEMAS
# ===========================================================================


class ExamGenerateRequest(BaseModel):
    """
    Request body for POST /exams/generate
    """

    categories: List[str] = Field(
        ...,
        min_length=1,
        description="One or more subject categories. Allowed: History, Geography, Politics, Economics",
        json_schema_extra={"example": ["History", "Politics"]},
    )
    question_type: str = Field(
        ...,
        description="Type of questions. Allowed: MCQ, FILL_BLANKS, SHORT_ANSWER, LONG_ANSWER",
        json_schema_extra={"example": "MCQ"},
    )
    question_count: int = Field(
        ...,
        ge=1,
        le=10,
        description="Number of questions (1 – 10)",
        json_schema_extra={"example": 10},
    )

    @field_validator("categories")
    @classmethod
    def validate_categories(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("At least one category must be selected.")
        invalid = [c for c in v if c not in VALID_CATEGORIES]
        if invalid:
            raise ValueError(
                f"Invalid categories: {invalid}. "
                f"Allowed: {sorted(VALID_CATEGORIES)}"
            )
        return v

    @field_validator("question_type")
    @classmethod
    def validate_question_type(cls, v: str) -> str:
        if v not in VALID_QUESTION_TYPES:
            raise ValueError(
                f"Invalid question_type: '{v}'. "
                f"Allowed: {sorted(VALID_QUESTION_TYPES)}"
            )
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "categories": ["History", "Politics"],
                "question_type": "MCQ",
                "question_count": 10,
            }
        }
    }


class SaveAnswerRequest(BaseModel):
    """
    Request body for POST /exams/{test_id}/answer
    """

    question_id: UUID = Field(
        ...,
        description="UUID of the question being answered",
    )
    student_answer: str = Field(
        ...,
        min_length=1,
        description="Student's answer text",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "question_id": "123e4567-e89b-12d3-a456-426614174001",
                "student_answer": "Option A",
            }
        }
    }


# ===========================================================================
# RESPONSE SCHEMAS
# ===========================================================================


class ExamGenerateData(BaseModel):
    """Data payload for exam generation response."""

    test_id: str
    question_count: int
    status: str


class QuestionResponse(BaseModel):
    """
    Student-safe question representation.
    correct_answer and model_answer are intentionally omitted.
    """

    id: str
    question_number: int
    question_type: str
    question_text: str
    category: str
    options: Optional[List[str]] = Field(
        default=None,
        description="MCQ options only — not present for other question types",
    )

    model_config = {"from_attributes": True}


class ExamSummaryResponse(BaseModel):
    """Compact exam representation used in list and history endpoints."""

    id: str
    subject: str
    question_type: str
    selected_categories: List[str]
    question_count: int
    status: str
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class ExamDetailResponse(BaseModel):
    """Full exam detail including questions (student-safe)."""

    id: str
    subject: str
    question_type: str
    selected_categories: List[str]
    question_count: int
    status: str
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    questions: List[QuestionResponse]


class SaveAnswerData(BaseModel):
    """Data payload returned after saving an answer."""

    answer_id: str
    question_id: str


class SavedAnswerResponse(BaseModel):
    """Single saved answer entry returned by GET /exams/{test_id}/answers."""

    answer_id: str
    question_id: str
    student_answer: Optional[str] = None
    updated_at: str


class SubmitExamData(BaseModel):
    """Data payload returned on exam submission."""

    test_id: str
    status: str
    completed_at: str
    questions_answered: int
    total_questions: int


# ===========================================================================
# STANDARD API ENVELOPE
# ===========================================================================


class APISuccess(BaseModel):
    """Standard success response envelope."""

    success: bool = True
    message: str
    data: Optional[Any] = None


class APIError(BaseModel):
    """Standard error response envelope."""

    success: bool = False
    message: str
    errors: List[str] = Field(default_factory=list)
