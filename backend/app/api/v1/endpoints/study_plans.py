"""
Study Plans API Endpoints
RESTful API for study plan management
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.study_plan import StudyPlanItem
from app.schemas.response import APIResponse
from app.schemas.study_plan_api import (
    CreateStudyPlanRequest,
    CreateStudyPlanResponse,
    StudyPlanSummaryResponse,
    StudyPlanDetailResponse,
    StudyPlanListResponse,
    UpdateStudyItemStatusRequest,
    create_plan_summary,
    create_plan_detail
)
from app.services.study_plan_service import StudyPlanService
from app.study_planner.schemas.study_plan import StudyPlanCreateRequest

router = APIRouter()


@router.post(
    "/",
    response_model=APIResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Study Plan",
    description="Generate and save a new study plan based on exam date, daily hours, and selected chapters"
)
def create_study_plan(
    request: CreateStudyPlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new study plan for the authenticated user.
    
    This endpoint:
    1. Validates the input (exam date, daily hours, chapter IDs)
    2. Calls the planner service to generate an optimized study schedule
    3. Saves the plan and all items to the database
    4. Returns the created plan summary
    
    **Request Body:**
    - `exam_date`: Target exam date (must be in the future)
    - `daily_study_hours`: Hours available per day (1-12)
    - `selected_chapter_ids`: List of chapter IDs to include in the plan
    
    **Returns:**
    - Plan ID, total days, and item count
    
    **Raises:**
    - 400: Invalid input (past date, invalid chapters, insufficient time)
    - 401: Unauthorized (no valid token)
    - 500: Server error during plan creation
    """
    try:
        # Convert to planner service request format
        planner_request = StudyPlanCreateRequest(
            exam_date=request.exam_date,
            daily_study_hours=request.daily_study_hours,
            selected_chapter_ids=request.selected_chapter_ids
        )
        
        # Create study plan
        study_plan = StudyPlanService.create_study_plan(
            db=db,
            user_id=current_user.id,
            request=planner_request
        )
        
        # Prepare response
        response_data = CreateStudyPlanResponse(
            plan_id=study_plan.id,
            total_days=len(study_plan.items),
            items_count=len(study_plan.items),
            exam_date=study_plan.exam_date,
            daily_study_hours=study_plan.daily_study_hours
        )
        
        return APIResponse(
            success=True,
            message="Study plan generated successfully",
            data=response_data.model_dump()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create study plan: {str(e)}"
        )


@router.get(
    "/",
    response_model=APIResponse,
    summary="List Study Plans",
    description="Get all study plans for the authenticated user with completion statistics"
)
def list_study_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all study plans belonging to the authenticated user.
    
    Returns a list of study plans with:
    - Basic plan information
    - Completion percentage
    - Total and completed item counts
    
    Plans are ordered by creation date (newest first).
    
    **Returns:**
    - List of study plan summaries
    
    **Raises:**
    - 401: Unauthorized (no valid token)
    """
    try:
        # Get user's study plans
        study_plans = StudyPlanService.get_user_study_plans(db, current_user.id)
        
        # Build response with completion percentages
        plan_summaries = []
        for plan in study_plans:
            completion = StudyPlanService.calculate_completion_percentage(plan)
            summary = create_plan_summary(plan, completion)
            plan_summaries.append(summary)
        
        response_data = StudyPlanListResponse(
            plans=plan_summaries,
            total_count=len(plan_summaries)
        )
        
        return APIResponse(
            success=True,
            message="Study plans retrieved successfully",
            data=response_data.model_dump()
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve study plans: {str(e)}"
        )


@router.get(
    "/{plan_id}",
    response_model=APIResponse,
    summary="Get Study Plan Details",
    description="Get complete details of a specific study plan including all items"
)
def get_study_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get complete details of a specific study plan.
    
    This endpoint returns:
    - Full plan information
    - All study items with their status
    - Completion statistics
    
    **Path Parameters:**
    - `plan_id`: ID of the study plan to retrieve
    
    **Returns:**
    - Complete study plan with all items
    
    **Raises:**
    - 401: Unauthorized (no valid token)
    - 403: Forbidden (not the plan owner)
    - 404: Study plan not found
    """
    # Verify ownership
    study_plan = StudyPlanService.verify_plan_ownership(
        db=db,
        plan_id=plan_id,
        user_id=current_user.id
    )
    
    # Calculate completion
    completion = StudyPlanService.calculate_completion_percentage(study_plan)
    
    # Build detailed response
    plan_detail = create_plan_detail(study_plan, completion)
    
    return APIResponse(
        success=True,
        message="Study plan retrieved successfully",
        data=plan_detail.model_dump()
    )


@router.patch(
    "/{plan_id}/items/{item_id}",
    response_model=APIResponse,
    summary="Update Study Item Status",
    description="Update the status of a specific study plan item (Pending, Completed, or Skipped)"
)
def update_study_item_status(
    plan_id: int,
    item_id: int,
    request: UpdateStudyItemStatusRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the status of a study plan item.
    
    This allows students to mark study sessions as:
    - **Pending**: Not yet started
    - **Completed**: Successfully finished
    - **Skipped**: Intentionally skipped
    
    **Path Parameters:**
    - `plan_id`: ID of the study plan
    - `item_id`: ID of the study item to update
    
    **Request Body:**
    - `status`: New status (Pending, Completed, or Skipped)
    
    **Returns:**
    - Updated study item details
    
    **Raises:**
    - 400: Invalid status value
    - 401: Unauthorized (no valid token)
    - 403: Forbidden (not the plan owner)
    - 404: Plan or item not found
    """
    try:
        # Update the study item status
        updated_item = StudyPlanService.update_study_item_status(
            db=db,
            plan_id=plan_id,
            item_id=item_id,
            user_id=current_user.id,
            new_status=request.status
        )
        
        return APIResponse(
            success=True,
            message="Status updated successfully",
            data={
                "item_id": updated_item.id,
                "day_number": updated_item.day_number,
                "status": updated_item.status.value,
                "chapter_name": updated_item.chapter_name,
                "activity_type": updated_item.activity_type.value
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update status: {str(e)}"
        )


@router.delete(
    "/{plan_id}",
    response_model=APIResponse,
    summary="Delete Study Plan",
    description="Delete a study plan and all its associated items (cascade delete)"
)
def delete_study_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a study plan and all its items.
    
    This operation:
    1. Verifies plan ownership
    2. Deletes the study plan
    3. Cascade deletes all associated study items
    
    **Path Parameters:**
    - `plan_id`: ID of the study plan to delete
    
    **Returns:**
    - Success confirmation
    
    **Raises:**
    - 401: Unauthorized (no valid token)
    - 403: Forbidden (not the plan owner)
    - 404: Study plan not found
    """
    try:
        # Delete the study plan (service handles ownership check)
        StudyPlanService.delete_study_plan(
            db=db,
            plan_id=plan_id,
            user_id=current_user.id
        )
        
        return APIResponse(
            success=True,
            message="Plan deleted successfully",
            data={"plan_id": plan_id}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete study plan: {str(e)}"
        )


@router.get(
    "/{plan_id}/summary",
    response_model=APIResponse,
    summary="Get Study Plan Summary",
    description="Get quick summary statistics for a study plan"
)
def get_study_plan_summary(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get summary statistics for a study plan.
    
    Returns:
    - Completion percentage
    - Total items
    - Completed items
    - Pending items
    - Skipped items
    - Days until exam
    
    **Path Parameters:**
    - `plan_id`: ID of the study plan
    
    **Returns:**
    - Summary statistics
    
    **Raises:**
    - 401: Unauthorized (no valid token)
    - 403: Forbidden (not the plan owner)
    - 404: Study plan not found
    """
    from datetime import date
    from app.models.study_plan import StudyStatus
    
    # Verify ownership
    study_plan = StudyPlanService.verify_plan_ownership(
        db=db,
        plan_id=plan_id,
        user_id=current_user.id
    )
    
    # Calculate statistics
    total_items = len(study_plan.items)
    completed_items = sum(1 for item in study_plan.items if item.status == StudyStatus.COMPLETED)
    pending_items = sum(1 for item in study_plan.items if item.status == StudyStatus.PENDING)
    skipped_items = sum(1 for item in study_plan.items if item.status == StudyStatus.SKIPPED)
    completion = StudyPlanService.calculate_completion_percentage(study_plan)
    days_until_exam = (study_plan.exam_date - date.today()).days
    
    return APIResponse(
        success=True,
        message="Summary retrieved successfully",
        data={
            "plan_id": study_plan.id,
            "exam_date": study_plan.exam_date.isoformat(),
            "days_until_exam": days_until_exam,
            "total_items": total_items,
            "completed_items": completed_items,
            "pending_items": pending_items,
            "skipped_items": skipped_items,
            "completion_percentage": completion
        }
    )


@router.get(
    "/progress",
    response_model=APIResponse,
    summary="Get Study Progress",
    description="Get progress summary for the user's latest study plan"
)
def get_study_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get progress summary for user's latest study plan.
    
    Returns comprehensive progress metrics including:
    - Total, completed, pending, and skipped tasks
    - Completion percentage
    - Plan ID and exam date
    
    **Returns:**
    - Progress summary
    
    **Raises:**
    - 401: Unauthorized (no valid token)
    - 404: No study plan found
    """
    try:
        progress = StudyPlanService.get_progress_summary(db, current_user.id)
        
        return APIResponse(
            success=True,
            message="Progress retrieved successfully",
            data=progress
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve progress: {str(e)}"
        )


@router.patch(
    "/task/{task_id}",
    response_model=APIResponse,
    summary="Update Task Completion Status",
    description="Mark a study task as completed or incomplete"
)
def update_task_status(
    task_id: int,
    request: UpdateStudyItemStatusRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the completion status of a study task.
    
    This endpoint:
    1. Finds the task and verifies ownership
    2. Updates the task status
    3. Sets/clears the completed_at timestamp
    4. Recalculates completion percentage
    5. Returns updated progress
    
    **Path Parameters:**
    - `task_id`: ID of the study task to update
    
    **Request Body:**
    - `status`: New status (Pending, Completed, or Skipped)
    
    **Returns:**
    - Updated task status
    - New completion percentage
    
    **Raises:**
    - 400: Invalid status value
    - 401: Unauthorized (no valid token)
    - 403: Forbidden (not the task owner)
    - 404: Task not found
    """
    try:
        # Find the task and get its plan_id
        task = db.query(StudyPlanItem).filter(StudyPlanItem.id == task_id).first()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Update the task status
        updated_task = StudyPlanService.update_study_item_status(
            db=db,
            plan_id=task.study_plan_id,
            item_id=task_id,
            user_id=current_user.id,
            new_status=request.status
        )
        
        # Get updated plan to calculate new completion percentage
        plan = StudyPlanService.get_study_plan_by_id(
            db=db,
            plan_id=task.study_plan_id,
            user_id=current_user.id
        )
        
        completion_percentage = StudyPlanService.calculate_completion_percentage(plan)
        
        return APIResponse(
            success=True,
            message="Task status updated successfully",
            data={
                "task_id": updated_task.id,
                "status": updated_task.status.value,
                "completed_at": updated_task.completed_at.isoformat() if updated_task.completed_at else None,
                "completion_percentage": completion_percentage
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task status: {str(e)}"
        )

