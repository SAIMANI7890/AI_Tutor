"""
Study Plan API Schemas
Request and response models for study plan endpoints
"""
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.study_plan import ActivityType, StudyStatus


# ============================================================
# REQUEST SCHEMAS
# ============================================================

class CreateStudyPlanRequest(BaseModel):
    """Request schema for creating a study plan"""
    exam_date: date = Field(..., description="Target exam date (must be in the future)")
    daily_study_hours: float = Field(..., ge=1.0, le=12.0, description="Daily study hours (1-12)")
    selected_chapter_ids: List[int] = Field(..., min_length=1, description="List of chapter IDs to include")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "exam_date": "2026-03-15",
                "daily_study_hours": 3.0,
                "selected_chapter_ids": [1, 2, 3, 4]
            }
        }
    }


class UpdateStudyItemStatusRequest(BaseModel):
    """Request schema for updating study item status"""
    status: StudyStatus = Field(..., description="New status for the study item")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "Completed"
            }
        }
    }


# ============================================================
# RESPONSE SCHEMAS
# ============================================================

class StudyPlanItemResponse(BaseModel):
    """Response schema for a study plan item"""
    id: int
    study_plan_id: int
    day_number: int
    study_date: date
    activity_type: ActivityType
    chapter_id: Optional[int] = None
    chapter_name: Optional[str] = None
    allocated_hours: float
    status: StudyStatus
    completed_at: Optional[datetime] = None
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }


class StudyPlanSummaryResponse(BaseModel):
    """Response schema for study plan summary (list view)"""
    id: int
    exam_date: date
    daily_study_hours: float
    created_at: datetime
    updated_at: datetime
    completion_percentage: float = Field(..., ge=0.0, le=100.0)
    total_items: int
    completed_items: int
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "exam_date": "2026-03-15",
                "daily_study_hours": 3.0,
                "created_at": "2026-02-10T10:00:00",
                "updated_at": "2026-02-10T10:00:00",
                "completion_percentage": 65.5,
                "total_items": 34,
                "completed_items": 22
            }
        }
    }


class StudyPlanDetailResponse(BaseModel):
    """Response schema for complete study plan details"""
    id: int
    user_id: int
    exam_date: date
    daily_study_hours: float
    created_at: datetime
    updated_at: datetime
    completion_percentage: float
    total_items: int
    completed_items: int
    items: List[StudyPlanItemResponse]
    
    model_config = {
        "from_attributes": True
    }


class CreateStudyPlanResponse(BaseModel):
    """Response schema for study plan creation"""
    plan_id: int
    total_days: int
    items_count: int
    exam_date: date
    daily_study_hours: float
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "plan_id": 1,
                "total_days": 28,
                "items_count": 34,
                "exam_date": "2026-03-15",
                "daily_study_hours": 3.0
            }
        }
    }


class StudyPlanListResponse(BaseModel):
    """Response schema for list of study plans"""
    plans: List[StudyPlanSummaryResponse]
    total_count: int
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "plans": [
                    {
                        "id": 1,
                        "exam_date": "2026-03-15",
                        "daily_study_hours": 3.0,
                        "created_at": "2026-02-10T10:00:00",
                        "updated_at": "2026-02-10T10:00:00",
                        "completion_percentage": 65.5,
                        "total_items": 34,
                        "completed_items": 22
                    }
                ],
                "total_count": 1
            }
        }
    }


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def create_plan_summary(plan, completion_percentage: float) -> StudyPlanSummaryResponse:
    """Create a summary response from a StudyPlan object"""
    total_items = len(plan.items) if plan.items else 0
    completed_items = sum(1 for item in plan.items if item.status == StudyStatus.COMPLETED) if plan.items else 0
    
    return StudyPlanSummaryResponse(
        id=plan.id,
        exam_date=plan.exam_date,
        daily_study_hours=plan.daily_study_hours,
        created_at=plan.created_at,
        updated_at=plan.updated_at,
        completion_percentage=completion_percentage,
        total_items=total_items,
        completed_items=completed_items
    )


def create_plan_detail(plan, completion_percentage: float) -> StudyPlanDetailResponse:
    """Create a detailed response from a StudyPlan object"""
    total_items = len(plan.items) if plan.items else 0
    completed_items = sum(1 for item in plan.items if item.status == StudyStatus.COMPLETED) if plan.items else 0
    
    items = [StudyPlanItemResponse.model_validate(item) for item in plan.items]
    
    return StudyPlanDetailResponse(
        id=plan.id,
        user_id=plan.user_id,
        exam_date=plan.exam_date,
        daily_study_hours=plan.daily_study_hours,
        created_at=plan.created_at,
        updated_at=plan.updated_at,
        completion_percentage=completion_percentage,
        total_items=total_items,
        completed_items=completed_items,
        items=items
    )
