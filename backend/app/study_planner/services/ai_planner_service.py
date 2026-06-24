"""
AI-Powered Study Planner Service
Uses Google Gemini for intelligent schedule generation with fallback to rule-based planner
"""
import json
import logging
from typing import List, Optional, Dict, Any
from datetime import date

from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings
from app.study_planner.services.planner_service import planner_service
from app.study_planner.config.chapters import get_chapters_by_ids
from app.study_planner.schemas.study_plan import GeneratedStudyPlan
from app.models.study_plan import ActivityType

logger = logging.getLogger(__name__)


class AIStudyPlanGenerator:
    """
    AI-powered study plan generator using Gemini
    
    Features:
    - Intelligent schedule generation using AI
    - JSON structure validation
    - Automatic retry on failure
    - Fallback to rule-based planner
    - Error handling and logging
    """
    
    MAX_RETRIES = 1  # Reduced retry attempts (fallback to rule-based is fast)
    GEMINI_MODEL = "gemini-2.5-flash-lite"  # Gemini 2.5 Flash Lite - fastest model
    TEMPERATURE = 0.3  # Lower temperature for more consistent output
    REQUEST_TIMEOUT = 15  # Timeout for Gemini API calls (seconds)
    
    def __init__(self):
        """Initialize the AI planner service"""
        self.gemini_llm = None
        self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Initialize Gemini LLM"""
        try:
            # Check if API key is configured
            api_key = settings.GEMINI_API_KEY
            if not api_key or api_key == "":
                logger.warning("GEMINI_API_KEY not configured - will use fallback planner")
                self.gemini_llm = None
                return
            
            self.gemini_llm = ChatGoogleGenerativeAI(
                model=self.GEMINI_MODEL,
                google_api_key=api_key,
                temperature=self.TEMPERATURE,
                timeout=self.REQUEST_TIMEOUT,  # Add timeout
                max_retries=0,  # Disable internal retries (we handle retries ourselves)
                convert_system_message_to_human=True
            )
            logger.info("Gemini LLM initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {str(e)}")
            self.gemini_llm = None
    
    def generate_study_plan(
        self,
        exam_date: date,
        daily_study_hours: float,
        selected_chapter_ids: List[int]
    ) -> GeneratedStudyPlan:
        """
        Generate study plan using AI with fallback
        
        Args:
            exam_date: Target exam date
            daily_study_hours: Hours available per day
            selected_chapter_ids: List of chapter IDs to include
        
        Returns:
            GeneratedStudyPlan with day-by-day schedule
        """
        # Attempt AI generation if Gemini is available
        if self.gemini_llm:
            for attempt in range(self.MAX_RETRIES):
                try:
                    logger.info(f"Attempting AI generation (attempt {attempt + 1}/{self.MAX_RETRIES})")
                    ai_plan = self._generate_with_ai(
                        exam_date,
                        daily_study_hours,
                        selected_chapter_ids
                    )
                    
                    if ai_plan:
                        logger.info("AI generation successful")
                        return ai_plan
                    
                    logger.warning(f"AI generation attempt {attempt + 1} failed validation")
                
                except Exception as e:
                    logger.error(f"AI generation attempt {attempt + 1} failed: {str(e)}")
                    continue
        
        # Fallback to rule-based planner
        logger.info("Falling back to rule-based planner")
        return self._generate_with_fallback(
            exam_date,
            daily_study_hours,
            selected_chapter_ids
        )
    
    def _generate_with_ai(
        self,
        exam_date: date,
        daily_study_hours: float,
        selected_chapter_ids: List[int]
    ) -> Optional[GeneratedStudyPlan]:
        """
        Generate study plan using Gemini AI
        
        Returns:
            GeneratedStudyPlan if successful, None otherwise
        """
        # Get chapter information
        chapters = get_chapters_by_ids(selected_chapter_ids)
        if not chapters:
            return None
        
        # Calculate metrics
        start_date = date.today()
        days_remaining = (exam_date - start_date).days
        
        # Create prompt
        prompt = self._create_ai_prompt(
            chapters,
            exam_date,
            start_date,
            daily_study_hours,
            days_remaining
        )
        
        # Call Gemini
        try:
            response = self.gemini_llm.invoke(prompt)
            raw_output = response.content
            
            # Parse and validate JSON
            plan_data = self._parse_and_validate_json(raw_output)
            
            if not plan_data:
                return None
            
            # Convert to GeneratedStudyPlan
            return self._convert_to_generated_plan(
                plan_data,
                exam_date,
                daily_study_hours,
                start_date,
                days_remaining,
                chapters
            )
        
        except Exception as e:
            logger.error(f"Gemini invocation failed: {str(e)}")
            return None
    
    def _create_ai_prompt(
        self,
        chapters: List[Any],
        exam_date: date,
        start_date: date,
        daily_study_hours: float,
        days_remaining: int
    ) -> str:
        """
        Create detailed prompt for Gemini
        
        The prompt must enforce:
        - Strict JSON output only
        - No markdown formatting
        - No explanations
        - Proper field structure
        """
        # Format chapter information
        chapter_list = []
        for ch in chapters:
            chapter_list.append({
                "id": ch.chapter_id,
                "name": ch.chapter_name,
                "category": ch.category,
                "difficulty": ch.difficulty.value,
                "estimated_hours": ch.estimated_study_hours
            })
        
        prompt = f"""You are an expert study planner. Generate an optimized study schedule.

**CRITICAL INSTRUCTIONS:**
1. Output ONLY a JSON array - NO markdown, NO explanations, NO additional text
2. Each day must have: day (number), type (string), task (string)
3. Valid types: "study", "revision", "mock_test"
4. Start day numbering from 1

**Input Data:**
- Exam Date: {exam_date.isoformat()}
- Start Date: {start_date.isoformat()}
- Days Available: {days_remaining}
- Daily Study Hours: {daily_study_hours}
- Chapters: {json.dumps(chapter_list, indent=2)}

**Requirements:**
1. Study harder chapters first (prioritize "Hard" difficulty)
2. Insert revision days every 4-5 study days
3. Insert mock tests every 7 days
4. For revision: task = "Revision Session"
5. For mock test: task = "Mock Test"
6. For study: task = chapter name
7. Balance workload across available days
8. Consider estimated hours for each chapter

**Expected Output Format (STRICT JSON ONLY):**
[
  {{"day": 1, "type": "study", "task": "French Revolution"}},
  {{"day": 2, "type": "study", "task": "World War I"}},
  {{"day": 3, "type": "study", "task": "Colonial Period"}},
  {{"day": 4, "type": "study", "task": "Industrial Revolution"}},
  {{"day": 5, "type": "revision", "task": "Revision Session"}},
  {{"day": 6, "type": "study", "task": "Geography Chapter 1"}},
  {{"day": 7, "type": "mock_test", "task": "Mock Test"}}
]

Generate the JSON array now (NO OTHER TEXT):"""
        
        return prompt
    
    def _parse_and_validate_json(self, raw_output: str) -> Optional[List[Dict[str, Any]]]:
        """
        Parse and validate JSON output from Gemini
        
        Args:
            raw_output: Raw response from Gemini
        
        Returns:
            Parsed and validated list of day plans, or None if invalid
        """
        try:
            # Clean the output (remove markdown if present)
            cleaned = raw_output.strip()
            
            # Remove markdown code blocks if present
            if cleaned.startswith("```"):
                lines = cleaned.split("\n")
                cleaned = "\n".join(line for line in lines if not line.startswith("```"))
                cleaned = cleaned.strip()
            
            # Remove "json" language identifier if present
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
            
            # Parse JSON
            plan_data = json.loads(cleaned)
            
            # Validate structure
            if not isinstance(plan_data, list):
                logger.error("Output is not a JSON array")
                return None
            
            if len(plan_data) == 0:
                logger.error("Output array is empty")
                return None
            
            # Validate each day
            valid_types = {"study", "revision", "mock_test"}
            
            for day in plan_data:
                # Check required fields
                if not isinstance(day, dict):
                    logger.error(f"Invalid day entry: {day}")
                    return None
                
                if "day" not in day or "type" not in day or "task" not in day:
                    logger.error(f"Missing required fields in day: {day}")
                    return None
                
                # Validate day number
                if not isinstance(day["day"], int) or day["day"] < 1:
                    logger.error(f"Invalid day number: {day['day']}")
                    return None
                
                # Validate type
                if day["type"] not in valid_types:
                    logger.error(f"Invalid activity type: {day['type']}")
                    return None
                
                # Validate task
                if not isinstance(day["task"], str) or not day["task"].strip():
                    logger.error(f"Invalid task: {day['task']}")
                    return None
            
            logger.info(f"Successfully validated {len(plan_data)} days")
            return plan_data
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {str(e)}")
            logger.error(f"Raw output: {raw_output[:500]}")  # Log first 500 chars
            return None
        except Exception as e:
            logger.error(f"Validation failed: {str(e)}")
            return None
    
    def _convert_to_generated_plan(
        self,
        plan_data: List[Dict[str, Any]],
        exam_date: date,
        daily_study_hours: float,
        start_date: date,
        days_remaining: int,
        chapters: List[Any]
    ) -> GeneratedStudyPlan:
        """
        Convert AI-generated plan data to GeneratedStudyPlan object
        
        This maps the AI output to our internal data structures
        """
        from datetime import timedelta
        from app.study_planner.schemas.study_plan import DayPlan, ChapterAllocation
        
        # Create chapter lookup
        chapter_lookup = {ch.chapter_name: ch for ch in chapters}
        
        # Convert plan data to DayPlan objects
        days = []
        current_date = start_date
        
        for day_data in plan_data:
            # Map type to ActivityType enum
            activity_type_map = {
                "study": ActivityType.STUDY,
                "revision": ActivityType.REVISION,
                "mock_test": ActivityType.MOCK_TEST
            }
            
            activity_type = activity_type_map.get(day_data["type"], ActivityType.STUDY)
            task = day_data["task"]
            
            # Find matching chapter
            chapter_id = None
            chapter_name = None
            
            if activity_type == ActivityType.STUDY:
                # Try to match task to a chapter
                matching_chapter = chapter_lookup.get(task)
                if matching_chapter:
                    chapter_id = matching_chapter.chapter_id
                    chapter_name = matching_chapter.chapter_name
                else:
                    # Use task as chapter name if no match
                    chapter_name = task
            
            day_plan = DayPlan(
                day_number=day_data["day"],
                study_date=current_date,
                activity_type=activity_type,
                chapter_id=chapter_id,
                chapter_name=chapter_name,
                allocated_hours=daily_study_hours
            )
            
            days.append(day_plan)
            current_date += timedelta(days=1)
        
        # Create chapter allocations
        chapter_allocations = []
        for chapter in chapters:
            # Count how many times this chapter appears
            study_sessions = sum(
                1 for day in days
                if day.activity_type == ActivityType.STUDY and day.chapter_name == chapter.chapter_name
            )
            
            if study_sessions > 0:
                allocation = ChapterAllocation(
                    chapter_id=chapter.chapter_id,
                    chapter_name=chapter.chapter_name,
                    category=chapter.category,
                    difficulty=chapter.difficulty.value,
                    estimated_hours=chapter.estimated_study_hours,
                    allocated_sessions=study_sessions,
                    hours_per_session=daily_study_hours
                )
                chapter_allocations.append(allocation)
        
        # Calculate totals
        total_required_hours = sum(ch.estimated_study_hours for ch in chapters)
        total_available_hours = len(days) * daily_study_hours
        
        return GeneratedStudyPlan(
            exam_date=exam_date,
            daily_study_hours=daily_study_hours,
            start_date=start_date,
            total_days=len(days),
            total_available_hours=total_available_hours,
            total_required_hours=total_required_hours,
            days=days,
            chapter_allocations=chapter_allocations,
            warnings=["Generated using AI (Gemini)"]
        )
    
    def _generate_with_fallback(
        self,
        exam_date: date,
        daily_study_hours: float,
        selected_chapter_ids: List[int]
    ) -> GeneratedStudyPlan:
        """
        Generate study plan using rule-based fallback planner
        
        This ensures the application never fails even if AI is unavailable
        """
        logger.info("Using rule-based fallback planner")
        
        plan = planner_service.generate_study_plan(
            exam_date=exam_date,
            daily_study_hours=daily_study_hours,
            selected_chapter_ids=selected_chapter_ids
        )
        
        # Add warning that fallback was used
        plan.warnings.append("Generated using rule-based planner (AI unavailable)")
        
        return plan


# Singleton instance
ai_planner_service = AIStudyPlanGenerator()
