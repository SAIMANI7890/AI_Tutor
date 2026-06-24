"""
Study Plan Schemas
Pydantic schemas for study plan requests and responses
"""
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from app.models.study_plan import ActivityType, StudyStatus


# ============================================================
# REQUEST SCHEMAS
# ============================================================

class StudyPlanCreateRequest(BaseModel):
    """Schema for creating a study plan"""
    exam_date: date = Field(..., description="Target exam date")
    daily_study_hours: float = Field(..., ge=1.0, le=12.0, description="Daily study hours (1-12)")
    selected_chapter_ids: List[int] = Field(..., min_length=1, description="List of chapter IDs to study")
    
    @field_validator('exam_date')
    @classmethod
    def validate_exam_date(cls, v: date) -> date:
        """Validate that exam date is in the future"""
        if v <= date.today():
            raise ValueError("Exam date must be in the future")
        return v
    
    @field_validator('selected_chapter_ids')
    @classmethod
    def validate_chapter_ids(cls, v: List[int]) -> List[int]:
        """Validate chapter IDs are unique"""
        if len(v) != len(set(v)):
            raise ValueError("Chapter IDs must be unique")
        return v


# ============================================================
# RESPONSE SCHEMAS
# ============================================================

class StudyPlanItemResponse(BaseModel):
    """Schema for study plan item response"""
    id: int
    study_plan_id: int
    day_number: int
    study_date: date
    activity_type: ActivityType
    chapter_id: Optional[int] = None
    chapter_name: Optional[str] = None
    allocated_hours: float
    status: StudyStatus
    created_at: datetime
    
    class Config:
        from_attributes = True


class StudyPlanResponse(BaseModel):
    """Schema for study plan response"""
    id: int
    user_id: int
    exam_date: date
    daily_study_hours: float
    created_at: datetime
    updated_at: datetime
    items: List[StudyPlanItemResponse] = []
    
    class Config:
        from_attributes = True


class StudyPlanSummary(BaseModel):
    """Schema for study plan summary"""
    total_days: int
    total_study_hours: float
    study_days: int
    revision_days: int
    mock_test_days: int
    chapters_covered: int


class StudyPlanDetailResponse(BaseModel):
    """Schema for detailed study plan with summary"""
    plan: StudyPlanResponse
    summary: StudyPlanSummary


# ============================================================
# PLANNING SCHEMAS (Internal Use)
# ============================================================

class ChapterAllocation(BaseModel):
    """Schema for chapter study allocation"""
    chapter_id: int
    chapter_name: str
    category: str
    difficulty: str
    estimated_hours: float
    allocated_sessions: int
    hours_per_session: float


class DayPlan(BaseModel):
    """Schema for a single day in the study plan"""
    day_number: int
    study_date: date
    activity_type: ActivityType
    chapter_id: Optional[int] = None
    chapter_name: Optional[str] = None
    allocated_hours: float


class GeneratedStudyPlan(BaseModel):
    """Schema for generated study plan (before database save)"""
    exam_date: date
    daily_study_hours: float
    start_date: date
    total_days: int
    total_available_hours: float
    total_required_hours: float
    days: List[DayPlan]
    chapter_allocations: List[ChapterAllocation]
    warnings: List[str] = []


# ============================================================
# VALIDATION SCHEMAS
# ============================================================

class PlanValidationResult(BaseModel):
    """Schema for plan validation result"""
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []


# ============================================================
# CHAPTER INFO SCHEMAS
# ============================================================

class ChapterInfo(BaseModel):
    """Schema for chapter information"""
    chapter_id: int
    chapter_name: str
    category: str
    difficulty: str
    estimated_study_hours: float


class ChaptersListResponse(BaseModel):
    """Schema for list of chapters"""
    chapters: List[ChapterInfo]
    total_count: int
