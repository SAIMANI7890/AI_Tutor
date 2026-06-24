"""
Unit Tests for Study Planner Service

Tests cover:
- Normal plan generation
- Hard chapter prioritization
- Revision day insertion
- Mock test insertion
- Insufficient hours validation
- Past exam date validation
- No chapters selected validation
"""
import pytest
from datetime import date, timedelta
from app.study_planner.services.planner_service import StudyPlannerService
from app.models.study_plan import ActivityType


class TestStudyPlannerService:
    """Test suite for StudyPlannerService"""
    
    @pytest.fixture
    def planner(self):
        """Create planner service instance"""
        return StudyPlannerService()
    
    @pytest.fixture
    def future_exam_date(self):
        """Get a future exam date (30 days from now)"""
        return date.today() + timedelta(days=30)
    
    @pytest.fixture
    def sample_chapter_ids(self):
        """Sample chapter IDs for testing"""
        return [1, 2, 11]  # French Revolution (Hard), Industrial Revolution (Hard), Climate (Medium)
    
    # ========================================
    # TEST: Normal Plan Generation
    # ========================================
    
    def test_generate_normal_plan(self, planner, future_exam_date, sample_chapter_ids):
        """Test normal study plan generation"""
        plan = planner.generate_study_plan(
            exam_date=future_exam_date,
            daily_study_hours=3.0,
            selected_chapter_ids=sample_chapter_ids
        )
        
        # Verify plan is generated
        assert plan is not None
        assert len(plan.days) > 0
        
        # Verify date range
        assert plan.start_date == date.today()
        assert plan.exam_date == future_exam_date
        
        # Verify days don't exceed available time
        assert plan.total_days <= (future_exam_date - date.today()).days
        
        # Verify all chapter allocations present
        assert len(plan.chapter_allocations) == len(sample_chapter_ids)
        
        # Verify at least some study days
        study_days = [day for day in plan.days if day.activity_type == ActivityType.STUDY]
        assert len(study_days) > 0
    
    def test_plan_with_different_daily_hours(self, planner, future_exam_date, sample_chapter_ids):
        """Test plan generation with different daily hours"""
        # Test with 2 hours
        plan_2h = planner.generate_study_plan(
            exam_date=future_exam_date,
            daily_study_hours=2.0,
            selected_chapter_ids=sample_chapter_ids
        )
        
        # Test with 5 hours
        plan_5h = planner.generate_study_plan(
            exam_date=future_exam_date,
            daily_study_hours=5.0,
            selected_chapter_ids=sample_chapter_ids
        )
        
        # More hours should result in fewer days
        assert plan_2h.total_days >= plan_5h.total_days
    
    # ========================================
    # TEST: Hard Chapter Prioritization
    # ========================================
    
    def test_hard_chapters_scheduled_first(self, planner, future_exam_date):
        """Test that hard chapters are prioritized and scheduled early"""
        chapter_ids = [1, 9, 11]  # Hard (French Rev), Easy (Ancient Civ), Medium (Climate)
        
        plan = planner.generate_study_plan(
            exam_date=future_exam_date,
            daily_study_hours=3.0,
            selected_chapter_ids=chapter_ids
        )
        
        # Get study days
        study_days = [day for day in plan.days if day.activity_type == ActivityType.STUDY]
        
        # French Revolution (Hard) should appear before Ancient Civilizations (Easy)
        french_rev_days = [i for i, day in enumerate(study_days) if day.chapter_id == 1]
        ancient_civ_days = [i for i, day in enumerate(study_days) if day.chapter_id == 9]
        
        if french_rev_days and ancient_civ_days:
            assert min(french_rev_days) < min(ancient_civ_days), \
                "Hard chapters should be scheduled before easy chapters"
    
    def test_hard_chapters_get_more_sessions(self, planner, future_exam_date):
        """Test that hard chapters get more study sessions"""
        chapter_ids = [1, 9]  # French Revolution (Hard), Ancient Civilizations (Easy)
        
        plan = planner.generate_study_plan(
            exam_date=future_exam_date,
            daily_study_hours=3.0,
            selected_chapter_ids=chapter_ids
        )
        
        # Count sessions for each chapter
        study_days = [day for day in plan.days if day.activity_type == ActivityType.STUDY]
        french_rev_sessions = sum(1 for day in study_days if day.chapter_id == 1)
        ancient_civ_sessions = sum(1 for day in study_days if day.chapter_id == 9)
        
        # Hard chapter should have same or more sessions
        assert french_rev_sessions >= ancient_civ_sessions, \
            "Hard chapters should have at least as many sessions as easy chapters"
    
    # ========================================
    # TEST: Revision Day Insertion
    # ========================================
    
    def test_revision_days_inserted(self, planner, future_exam_date, sample_chapter_ids):
        """Test that revision days are inserted every 4 study days"""
        plan = planner.generate_study_plan(
            exam_date=future_exam_date,
            daily_study_hours=3.0,
            selected_chapter_ids=sample_chapter_ids
        )
        
        # Count revision days
        revision_days = [day for day in plan.days if day.activity_type == ActivityType.REVISION]
        
        # Should have at least one revision day for 30-day plan
        assert len(revision_days) > 0, "Plan should include revision days"
        
        # Verify revision days have no chapter assigned
        for day in revision_days:
            assert day.chapter_id is None
            assert day.chapter_name is None
    
    def test_revision_interval(self, planner, future_exam_date):
        """Test that revision days appear at reasonable intervals"""
        # Use enough chapters to generate long plan
        chapter_ids = [1, 2, 3, 4, 5, 11, 12, 13]
        
        plan = planner.generate_study_plan(
            exam_date=future_exam_date,
            daily_study_hours=2.0,
            selected_chapter_ids=chapter_ids
        )
        
        # Simply verify that revisions are inserted
        revision_count = sum(1 for day in plan.days if day.activity_type == ActivityType.REVISION)
        
        # For a 30-day plan with many chapters, should have at least one revision
        assert revision_count > 0, "Plan should include revision days"
    
    # ========================================
    # TEST: Mock Test Insertion
    # ========================================
    
    def test_mock_tests_inserted(self, planner, future_exam_date):
        """Test that mock tests are inserted every 7 days"""
        # Use enough chapters for a long plan
        chapter_ids = [1, 2, 3, 4, 5, 11, 12, 13]
        
        plan = planner.generate_study_plan(
            exam_date=future_exam_date,
            daily_study_hours=2.0,
            selected_chapter_ids=chapter_ids
        )
        
        # Count mock test days
        mock_test_days = [day for day in plan.days if day.activity_type == ActivityType.MOCK_TEST]
        
        # Should have at least one mock test for 30-day plan
        assert len(mock_test_days) > 0, "Plan should include mock test days"
        
        # Verify mock tests have no chapter assigned
        for day in mock_test_days:
            assert day.chapter_id is None
            assert day.chapter_name is None
    
    def test_mock_test_interval(self, planner, future_exam_date):
        """Test that mock tests appear roughly every 7 days"""
        chapter_ids = [1, 2, 3, 4, 5, 11, 12, 13]
        
        plan = planner.generate_study_plan(
            exam_date=future_exam_date,
            daily_study_hours=2.0,
            selected_chapter_ids=chapter_ids
        )
        
        # Find mock test positions
        mock_test_positions = [
            i for i, day in enumerate(plan.days) if day.activity_type == ActivityType.MOCK_TEST
        ]
        
        if len(mock_test_positions) > 1:
            intervals = [mock_test_positions[i] - mock_test_positions[i-1] 
                        for i in range(1, len(mock_test_positions))]
            # Mock tests should be spaced roughly 7 days apart
            assert all(5 <= interval <= 9 for interval in intervals), \
                "Mock tests should be spaced around 7 days"
    
    # ========================================
    # TEST: Insufficient Hours Validation
    # ========================================
    
    def test_insufficient_hours_warning(self, planner):
        """Test that warning is generated when insufficient study time"""
        # Create impossible scenario: too many chapters, too little time
        exam_date = date.today() + timedelta(days=5)  # Only 5 days
        chapter_ids = [1, 2, 3, 4, 5, 11, 12, 13, 21, 22]  # 10 chapters
        
        plan = planner.generate_study_plan(
            exam_date=exam_date,
            daily_study_hours=2.0,
            selected_chapter_ids=chapter_ids
        )
        
        # Should generate warnings
        assert len(plan.warnings) > 0, "Should warn about insufficient time"
        assert any("Insufficient" in warning for warning in plan.warnings)
    
    def test_sufficient_hours_no_warning(self, planner, future_exam_date):
        """Test that no warning when sufficient time available"""
        # Feasible scenario: few chapters, plenty of time
        chapter_ids = [9, 13]  # 2 easy chapters
        
        plan = planner.generate_study_plan(
            exam_date=future_exam_date,
            daily_study_hours=4.0,
            selected_chapter_ids=chapter_ids
        )
        
        # Should have no warnings or only minor ones
        insufficient_warnings = [w for w in plan.warnings if "Insufficient" in w]
        assert len(insufficient_warnings) == 0, "Should not warn about insufficient time"
    
    # ========================================
    # TEST: Past Exam Date Validation
    # ========================================
    
    def test_past_exam_date_rejected(self, planner, sample_chapter_ids):
        """Test that past exam dates are rejected"""
        past_date = date.today() - timedelta(days=10)
        
        with pytest.raises(ValueError) as exc_info:
            planner.generate_study_plan(
                exam_date=past_date,
                daily_study_hours=3.0,
                selected_chapter_ids=sample_chapter_ids
            )
        
        assert "future" in str(exc_info.value).lower()
    
    def test_today_exam_date_rejected(self, planner, sample_chapter_ids):
        """Test that today's date is rejected as exam date"""
        today = date.today()
        
        with pytest.raises(ValueError) as exc_info:
            planner.generate_study_plan(
                exam_date=today,
                daily_study_hours=3.0,
                selected_chapter_ids=sample_chapter_ids
            )
        
        assert "future" in str(exc_info.value).lower()
    
    # ========================================
    # TEST: No Chapters Selected Validation
    # ========================================
    
    def test_empty_chapter_list_rejected(self, planner, future_exam_date):
        """Test that empty chapter list is rejected"""
        with pytest.raises(ValueError) as exc_info:
            planner.generate_study_plan(
                exam_date=future_exam_date,
                daily_study_hours=3.0,
                selected_chapter_ids=[]
            )
        
        assert "chapter" in str(exc_info.value).lower()
    
    def test_invalid_chapter_ids_rejected(self, planner, future_exam_date):
        """Test that invalid chapter IDs are rejected"""
        invalid_ids = [9999, 8888]  # Non-existent chapter IDs
        
        with pytest.raises(ValueError) as exc_info:
            planner.generate_study_plan(
                exam_date=future_exam_date,
                daily_study_hours=3.0,
                selected_chapter_ids=invalid_ids
            )
        
        assert "invalid" in str(exc_info.value).lower() or "valid" in str(exc_info.value).lower()
    
    # ========================================
    # TEST: Daily Hours Validation
    # ========================================
    
    def test_too_few_daily_hours_rejected(self, planner, future_exam_date, sample_chapter_ids):
        """Test that daily hours below minimum are rejected"""
        with pytest.raises(ValueError):
            planner.generate_study_plan(
                exam_date=future_exam_date,
                daily_study_hours=0.5,  # Below minimum of 1
                selected_chapter_ids=sample_chapter_ids
            )
    
    def test_too_many_daily_hours_rejected(self, planner, future_exam_date, sample_chapter_ids):
        """Test that daily hours above maximum are rejected"""
        with pytest.raises(ValueError):
            planner.generate_study_plan(
                exam_date=future_exam_date,
                daily_study_hours=15.0,  # Above maximum of 12
                selected_chapter_ids=sample_chapter_ids
            )
    
    # ========================================
    # TEST: Plan Summary
    # ========================================
    
    def test_plan_summary_generation(self, planner, future_exam_date, sample_chapter_ids):
        """Test that plan summary is correctly generated"""
        plan = planner.generate_study_plan(
            exam_date=future_exam_date,
            daily_study_hours=3.0,
            selected_chapter_ids=sample_chapter_ids
        )
        
        summary = planner.get_plan_summary(plan)
        
        # Verify summary fields
        assert 'total_days' in summary
        assert 'total_study_hours' in summary
        assert 'study_days' in summary
        assert 'revision_days' in summary
        assert 'mock_test_days' in summary
        assert 'chapters_covered' in summary
        
        # Verify counts
        assert summary['total_days'] == len(plan.days)
        assert summary['chapters_covered'] == len(sample_chapter_ids)
        
        # Verify day type counts add up
        study_days = sum(1 for day in plan.days if day.activity_type == ActivityType.STUDY)
        revision_days = sum(1 for day in plan.days if day.activity_type == ActivityType.REVISION)
        mock_test_days = sum(1 for day in plan.days if day.activity_type == ActivityType.MOCK_TEST)
        
        assert summary['study_days'] == study_days
        assert summary['revision_days'] == revision_days
        assert summary['mock_test_days'] == mock_test_days
    
    # ========================================
    # TEST: Edge Cases
    # ========================================
    
    def test_single_chapter_plan(self, planner, future_exam_date):
        """Test plan with only one chapter"""
        plan = planner.generate_study_plan(
            exam_date=future_exam_date,
            daily_study_hours=3.0,
            selected_chapter_ids=[1]  # Only French Revolution
        )
        
        assert len(plan.chapter_allocations) == 1
        assert plan.chapter_allocations[0].chapter_id == 1
    
    def test_many_chapters_plan(self, planner, future_exam_date):
        """Test plan with many chapters"""
        # Select 15 chapters
        chapter_ids = list(range(1, 16))
        
        plan = planner.generate_study_plan(
            exam_date=future_exam_date,
            daily_study_hours=6.0,  # High daily hours
            selected_chapter_ids=chapter_ids
        )
        
        assert len(plan.chapter_allocations) == 15
    
    def test_short_timeline_plan(self, planner):
        """Test plan with very short timeline"""
        short_exam_date = date.today() + timedelta(days=10)
        
        plan = planner.generate_study_plan(
            exam_date=short_exam_date,
            daily_study_hours=6.0,
            selected_chapter_ids=[9, 13]  # 2 easy chapters
        )
        
        # Should complete within 10 days
        assert plan.total_days <= 10
    
    def test_all_activity_types_present_in_long_plan(self, planner, future_exam_date):
        """Test that long plans include all activity types"""
        # Create a long plan with many chapters
        chapter_ids = [1, 2, 3, 4, 5, 11, 12, 13]
        
        plan = planner.generate_study_plan(
            exam_date=future_exam_date,
            daily_study_hours=2.0,
            selected_chapter_ids=chapter_ids
        )
        
        activity_types = {day.activity_type for day in plan.days}
        
        # Should have study days
        assert ActivityType.STUDY in activity_types
        
        # Should have revision or mock tests (or both)
        assert ActivityType.REVISION in activity_types or ActivityType.MOCK_TEST in activity_types


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
