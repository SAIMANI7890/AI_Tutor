"""
Study Plan Service
Business logic for study plan management
"""
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.study_plan import StudyPlan, StudyPlanItem, StudyStatus
from app.study_planner.services.ai_planner_service import ai_planner_service
from app.study_planner.schemas.study_plan import StudyPlanCreateRequest
from app.study_planner.config.chapters import validate_chapter_ids


class StudyPlanService:
    """Service for managing study plans"""
    
    @staticmethod
    def create_study_plan(
        db: Session,
        user_id: int,
        request: StudyPlanCreateRequest
    ) -> StudyPlan:
        """
        Create a new study plan for a user
        
        Args:
            db: Database session
            user_id: ID of the user creating the plan
            request: Study plan creation request
            
        Returns:
            Created StudyPlan with items
            
        Raises:
            HTTPException: If validation fails or plan cannot be created
        """
        # Validate chapter IDs
        if not validate_chapter_ids(request.selected_chapter_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more invalid chapter IDs provided"
            )
        
        # Generate study plan using AI planner service (with fallback)
        try:
            generated_plan = ai_planner_service.generate_study_plan(
                exam_date=request.exam_date,
                daily_study_hours=request.daily_study_hours,
                selected_chapter_ids=request.selected_chapter_ids
            )
        except ValueError as e:
            # Validation errors from planner service
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            # Unexpected errors
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate study plan: {str(e)}"
            )
        
        # Create StudyPlan record
        study_plan = StudyPlan(
            user_id=user_id,
            exam_date=request.exam_date,
            daily_study_hours=request.daily_study_hours
        )
        db.add(study_plan)
        db.flush()  # Get the ID without committing
        
        # Create StudyPlanItem records
        for day_plan in generated_plan.days:
            study_item = StudyPlanItem(
                study_plan_id=study_plan.id,
                day_number=day_plan.day_number,
                study_date=day_plan.study_date,
                activity_type=day_plan.activity_type,
                chapter_id=day_plan.chapter_id,
                chapter_name=day_plan.chapter_name,
                allocated_hours=day_plan.allocated_hours,
                status=StudyStatus.PENDING
            )
            db.add(study_item)
        
        db.commit()
        db.refresh(study_plan)
        
        return study_plan
    
    @staticmethod
    def get_user_study_plans(db: Session, user_id: int) -> List[StudyPlan]:
        """
        Get all study plans for a user
        
        Args:
            db: Database session
            user_id: ID of the user
            
        Returns:
            List of StudyPlan objects
        """
        return db.query(StudyPlan).filter(
            StudyPlan.user_id == user_id
        ).order_by(StudyPlan.created_at.desc()).all()
    
    @staticmethod
    def get_study_plan_by_id(
        db: Session,
        plan_id: int,
        user_id: Optional[int] = None
    ) -> Optional[StudyPlan]:
        """
        Get a study plan by ID, optionally filtered by user
        
        Args:
            db: Database session
            plan_id: ID of the study plan
            user_id: Optional user ID for ownership check
            
        Returns:
            StudyPlan object or None if not found
        """
        query = db.query(StudyPlan).filter(StudyPlan.id == plan_id)
        
        if user_id is not None:
            query = query.filter(StudyPlan.user_id == user_id)
        
        return query.first()
    
    @staticmethod
    def update_study_item_status(
        db: Session,
        plan_id: int,
        item_id: int,
        user_id: int,
        new_status: StudyStatus
    ) -> StudyPlanItem:
        """
        Update the status of a study plan item
        
        Args:
            db: Database session
            plan_id: ID of the study plan
            item_id: ID of the study plan item
            user_id: ID of the user (for ownership check)
            new_status: New status to set
            
        Returns:
            Updated StudyPlanItem
            
        Raises:
            HTTPException: If plan or item not found, or unauthorized
        """
        from datetime import datetime
        from app.core.config import settings
        import pytz
        
        # Verify plan ownership
        plan = StudyPlanService.get_study_plan_by_id(db, plan_id, user_id)
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Study plan not found"
            )
        
        # Get the study item
        study_item = db.query(StudyPlanItem).filter(
            StudyPlanItem.id == item_id,
            StudyPlanItem.study_plan_id == plan_id
        ).first()
        
        if not study_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Study plan item not found"
            )
        
        # Update status and timestamp
        study_item.status = new_status
        
        # Set completed_at timestamp when marking as completed
        if new_status == StudyStatus.COMPLETED:
            study_item.completed_at = datetime.now(pytz.UTC)
        elif new_status == StudyStatus.PENDING:
            # Clear timestamp when unmarking
            study_item.completed_at = None
        
        db.commit()
        db.refresh(study_item)
        
        return study_item
    
    @staticmethod
    def delete_study_plan(
        db: Session,
        plan_id: int,
        user_id: int
    ) -> bool:
        """
        Delete a study plan and all its items
        
        Args:
            db: Database session
            plan_id: ID of the study plan
            user_id: ID of the user (for ownership check)
            
        Returns:
            True if deleted successfully
            
        Raises:
            HTTPException: If plan not found or unauthorized
        """
        # Verify plan ownership
        plan = StudyPlanService.get_study_plan_by_id(db, plan_id, user_id)
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Study plan not found"
            )
        
        # Delete plan (cascade will handle items)
        db.delete(plan)
        db.commit()
        
        return True
    
    @staticmethod
    def calculate_completion_percentage(study_plan: StudyPlan) -> float:
        """
        Calculate completion percentage for a study plan
        
        Args:
            study_plan: StudyPlan object with loaded items
            
        Returns:
            Completion percentage (0-100)
        """
        if not study_plan.items:
            return 0.0
        
        total_items = len(study_plan.items)
        completed_items = sum(
            1 for item in study_plan.items
            if item.status == StudyStatus.COMPLETED
        )
        
        return round((completed_items / total_items) * 100, 2)
    
    @staticmethod
    def verify_plan_ownership(
        db: Session,
        plan_id: int,
        user_id: int
    ) -> StudyPlan:
        """
        Verify that a user owns a study plan
        
        Args:
            db: Database session
            plan_id: ID of the study plan
            user_id: ID of the user
            
        Returns:
            StudyPlan object
            
        Raises:
            HTTPException: If plan not found or user is not the owner
        """
        plan = StudyPlanService.get_study_plan_by_id(db, plan_id)
        
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Study plan not found"
            )
        
        if plan.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this study plan"
            )
        
        return plan
    
    @staticmethod
    def get_progress_summary(
        db: Session,
        user_id: int
    ) -> dict:
        """
        Get progress summary for user's latest study plan
        
        Args:
            db: Database session
            user_id: ID of the user
            
        Returns:
            Dictionary with progress metrics
            
        Raises:
            HTTPException: If no study plan found
        """
        # Get latest study plan
        plans = StudyPlanService.get_user_study_plans(db, user_id)
        if not plans:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No study plan found"
            )
        
        latest_plan = plans[0]  # Already sorted by created_at desc
        
        # Calculate metrics
        total_tasks = len(latest_plan.items)
        completed_tasks = sum(
            1 for item in latest_plan.items
            if item.status == StudyStatus.COMPLETED
        )
        pending_tasks = sum(
            1 for item in latest_plan.items
            if item.status == StudyStatus.PENDING
        )
        skipped_tasks = sum(
            1 for item in latest_plan.items
            if item.status == StudyStatus.SKIPPED
        )
        
        completion_percentage = StudyPlanService.calculate_completion_percentage(latest_plan)
        
        return {
            "plan_id": latest_plan.id,
            "exam_date": latest_plan.exam_date.isoformat(),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "skipped_tasks": skipped_tasks,
            "completion_percentage": completion_percentage
        }
