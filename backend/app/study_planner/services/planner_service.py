"""
Study Planner Service
Core scheduling engine for generating study plans

This service implements the study plan generation algorithm with:
- Difficulty-based chapter prioritization
- Automatic revision days insertion
- Mock test scheduling
- Hour validation and optimization
"""
from datetime import date, timedelta
from typing import List, Tuple
import math

from app.study_planner.config.chapters import (
    get_chapters_by_ids,
    get_total_study_hours,
    get_difficulty_weight,
    Difficulty,
    Chapter
)
from app.study_planner.schemas.study_plan import (
    GeneratedStudyPlan,
    DayPlan,
    ChapterAllocation,
    PlanValidationResult
)
from app.models.study_plan import ActivityType


class StudyPlannerService:
    """
    Study planner service for generating optimized study schedules
    
    Algorithm Steps:
    1. Calculate days remaining until exam
    2. Calculate total available study hours
    3. Calculate total required study hours
    4. Validate if plan is feasible
    5. Sort chapters by difficulty (Hard → Medium → Easy)
    6. Distribute study sessions based on difficulty weights
    7. Insert revision days every 4 study days
    8. Insert mock tests every 7 days
    9. Generate final day-by-day plan
    """
    
    # Configuration constants
    REVISION_INTERVAL = 4  # Insert revision after every 4 study days
    MOCK_TEST_INTERVAL = 7  # Insert mock test after every 7 days
    MIN_DAILY_HOURS = 1.0
    MAX_DAILY_HOURS = 12.0
    
    def __init__(self):
        """Initialize the planner service"""
        pass
    
    def generate_study_plan(
        self,
        exam_date: date,
        daily_study_hours: float,
        selected_chapter_ids: List[int]
    ) -> GeneratedStudyPlan:
        """
        Generate a complete study plan
        
        Args:
            exam_date: Target exam date
            daily_study_hours: Hours available per day
            selected_chapter_ids: List of chapter IDs to include
        
        Returns:
            GeneratedStudyPlan with day-by-day schedule
        
        Raises:
            ValueError: If validation fails
        """
        # Step 1: Validate inputs
        validation = self._validate_inputs(exam_date, daily_study_hours, selected_chapter_ids)
        if not validation.is_valid:
            raise ValueError(f"Validation failed: {', '.join(validation.errors)}")
        
        # Step 2: Calculate time metrics
        start_date = date.today()
        days_remaining = (exam_date - start_date).days
        
        # Get chapter information
        chapters = get_chapters_by_ids(selected_chapter_ids)
        if not chapters:
            raise ValueError("No valid chapters found for the given IDs")
        
        total_required_hours = sum(ch.estimated_study_hours for ch in chapters)
        
        # Step 3: Calculate available hours (accounting for revision and mock test days)
        estimated_non_study_days = self._estimate_non_study_days(days_remaining)
        effective_study_days = days_remaining - estimated_non_study_days
        total_available_hours = effective_study_days * daily_study_hours
        
        # Step 4: Check feasibility
        warnings = []
        if total_required_hours > total_available_hours:
            warnings.append(
                f"Insufficient time: Need {total_required_hours:.1f} hours but only "
                f"{total_available_hours:.1f} hours available. Consider increasing daily hours "
                f"or reducing chapters."
            )
        
        # Step 5: Sort chapters by difficulty (Hard first)
        sorted_chapters = self._sort_chapters_by_difficulty(chapters)
        
        # Step 6: Calculate session distribution
        chapter_allocations = self._calculate_chapter_allocations(
            sorted_chapters,
            daily_study_hours,
            effective_study_days
        )
        
        # Step 7: Generate day-by-day plan
        days = self._generate_day_plan(
            start_date,
            exam_date,
            daily_study_hours,
            chapter_allocations
        )
        
        # Calculate actual totals
        total_study_hours = sum(day.allocated_hours for day in days if day.activity_type == ActivityType.STUDY)
        
        return GeneratedStudyPlan(
            exam_date=exam_date,
            daily_study_hours=daily_study_hours,
            start_date=start_date,
            total_days=len(days),
            total_available_hours=total_available_hours,
            total_required_hours=total_required_hours,
            days=days,
            chapter_allocations=chapter_allocations,
            warnings=warnings
        )
    
    def _validate_inputs(
        self,
        exam_date: date,
        daily_study_hours: float,
        selected_chapter_ids: List[int]
    ) -> PlanValidationResult:
        """Validate input parameters"""
        errors = []
        warnings = []
        
        # Validate exam date
        if exam_date <= date.today():
            errors.append("Exam date must be in the future")
        
        days_until_exam = (exam_date - date.today()).days
        if days_until_exam < 7:
            warnings.append(f"Only {days_until_exam} days until exam - very tight schedule")
        
        # Validate daily hours
        if not (self.MIN_DAILY_HOURS <= daily_study_hours <= self.MAX_DAILY_HOURS):
            errors.append(f"Daily study hours must be between {self.MIN_DAILY_HOURS} and {self.MAX_DAILY_HOURS}")
        
        # Validate chapters
        if not selected_chapter_ids:
            errors.append("At least one chapter must be selected")
        
        if len(selected_chapter_ids) != len(set(selected_chapter_ids)):
            errors.append("Duplicate chapter IDs found")
        
        # Validate chapter IDs exist
        chapters = get_chapters_by_ids(selected_chapter_ids)
        if len(chapters) != len(selected_chapter_ids):
            errors.append("One or more invalid chapter IDs")
        
        return PlanValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def _estimate_non_study_days(self, total_days: int) -> int:
        """Estimate number of revision and mock test days"""
        if total_days < 7:
            return 0
        
        # Rough estimate: 1 revision day per REVISION_INTERVAL + 1 mock test per MOCK_TEST_INTERVAL
        revision_days = total_days // (self.REVISION_INTERVAL + 1)
        mock_test_days = total_days // self.MOCK_TEST_INTERVAL
        
        return min(revision_days + mock_test_days, total_days // 2)  # Cap at 50% of days
    
    def _sort_chapters_by_difficulty(self, chapters: List[Chapter]) -> List[Chapter]:
        """
        Sort chapters by difficulty: Hard → Medium → Easy
        Hard chapters should be studied first when memory is fresh
        """
        difficulty_order = {
            Difficulty.HARD: 0,
            Difficulty.MEDIUM: 1,
            Difficulty.EASY: 2
        }
        
        return sorted(chapters, key=lambda ch: (difficulty_order[ch.difficulty], ch.chapter_name))
    
    def _calculate_chapter_allocations(
        self,
        chapters: List[Chapter],
        daily_study_hours: float,
        effective_study_days: int
    ) -> List[ChapterAllocation]:
        """
        Calculate how many sessions each chapter gets based on difficulty
        
        Hard chapters get more sessions (difficulty weight = 1.5)
        Medium chapters get baseline sessions (difficulty weight = 1.0)
        Easy chapters get fewer sessions (difficulty weight = 0.7)
        """
        allocations = []
        
        # Calculate total weighted hours
        total_weighted_hours = sum(
            ch.estimated_study_hours * get_difficulty_weight(ch.difficulty)
            for ch in chapters
        )
        
        for chapter in chapters:
            # Base sessions from estimated hours
            base_sessions = math.ceil(chapter.estimated_study_hours / daily_study_hours)
            
            # Apply difficulty weight
            difficulty_weight = get_difficulty_weight(chapter.difficulty)
            weighted_sessions = max(1, round(base_sessions * difficulty_weight))
            
            # Calculate hours per session
            hours_per_session = min(chapter.estimated_study_hours / weighted_sessions, daily_study_hours)
            
            allocations.append(ChapterAllocation(
                chapter_id=chapter.chapter_id,
                chapter_name=chapter.chapter_name,
                category=chapter.category,
                difficulty=chapter.difficulty.value,
                estimated_hours=chapter.estimated_study_hours,
                allocated_sessions=weighted_sessions,
                hours_per_session=round(hours_per_session, 2)
            ))
        
        return allocations
    
    def _generate_day_plan(
        self,
        start_date: date,
        exam_date: date,
        daily_study_hours: float,
        chapter_allocations: List[ChapterAllocation]
    ) -> List[DayPlan]:
        """
        Generate day-by-day study plan with:
        - Study sessions
        - Revision days (every 4 study days)
        - Mock tests (every 7 days)
        """
        days = []
        current_date = start_date
        day_number = 1
        study_day_counter = 0
        total_day_counter = 0
        
        # Create a session queue for each chapter
        session_queue = []
        for allocation in chapter_allocations:
            for _ in range(allocation.allocated_sessions):
                session_queue.append({
                    'chapter_id': allocation.chapter_id,
                    'chapter_name': allocation.chapter_name,
                    'hours': allocation.hours_per_session
                })
        
        # Generate days until exam or sessions exhausted
        session_index = 0
        
        while current_date < exam_date and (session_index < len(session_queue) or study_day_counter > 0):
            total_day_counter += 1
            
            # Check for mock test day (every 7 days)
            if total_day_counter % self.MOCK_TEST_INTERVAL == 0 and total_day_counter > 0:
                days.append(DayPlan(
                    day_number=day_number,
                    study_date=current_date,
                    activity_type=ActivityType.MOCK_TEST,
                    chapter_id=None,
                    chapter_name=None,
                    allocated_hours=daily_study_hours
                ))
                day_number += 1
                current_date += timedelta(days=1)
                continue
            
            # Check for revision day (every 4 study days)
            if study_day_counter > 0 and study_day_counter % self.REVISION_INTERVAL == 0:
                days.append(DayPlan(
                    day_number=day_number,
                    study_date=current_date,
                    activity_type=ActivityType.REVISION,
                    chapter_id=None,
                    chapter_name=None,
                    allocated_hours=daily_study_hours
                ))
                day_number += 1
                current_date += timedelta(days=1)
                continue
            
            # Regular study day
            if session_index < len(session_queue):
                session = session_queue[session_index]
                days.append(DayPlan(
                    day_number=day_number,
                    study_date=current_date,
                    activity_type=ActivityType.STUDY,
                    chapter_id=session['chapter_id'],
                    chapter_name=session['chapter_name'],
                    allocated_hours=session['hours']
                ))
                session_index += 1
                study_day_counter += 1
                day_number += 1
                current_date += timedelta(days=1)
            else:
                # No more sessions, break
                break
        
        return days
    
    def get_plan_summary(self, plan: GeneratedStudyPlan) -> dict:
        """Generate a summary of the study plan"""
        study_days = sum(1 for day in plan.days if day.activity_type == ActivityType.STUDY)
        revision_days = sum(1 for day in plan.days if day.activity_type == ActivityType.REVISION)
        mock_test_days = sum(1 for day in plan.days if day.activity_type == ActivityType.MOCK_TEST)
        
        total_study_hours = sum(
            day.allocated_hours for day in plan.days if day.activity_type == ActivityType.STUDY
        )
        
        return {
            'total_days': plan.total_days,
            'total_study_hours': round(total_study_hours, 2),
            'study_days': study_days,
            'revision_days': revision_days,
            'mock_test_days': mock_test_days,
            'chapters_covered': len(plan.chapter_allocations)
        }


# Singleton instance
planner_service = StudyPlannerService()
