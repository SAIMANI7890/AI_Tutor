"""
Unit Tests for Chapter Configuration

Tests cover:
- Chapter data structure
- Helper functions
- Validation logic
- Difficulty weights
"""
import pytest
from app.study_planner.config.chapters import (
    get_all_chapters,
    get_chapter_by_id,
    get_chapters_by_ids,
    get_chapters_by_category,
    get_chapters_by_difficulty,
    get_total_study_hours,
    validate_chapter_ids,
    get_difficulty_weight,
    Difficulty,
    CHAPTERS
)


class TestChapterConfiguration:
    """Test suite for chapter configuration"""
    
    def test_all_chapters_loaded(self):
        """Test that all chapters are loaded"""
        chapters = get_all_chapters()
        assert len(chapters) > 0
        assert len(chapters) == len(CHAPTERS)
    
    def test_chapter_structure(self):
        """Test that chapters have required fields"""
        chapters = get_all_chapters()
        
        for chapter in chapters:
            assert hasattr(chapter, 'chapter_id')
            assert hasattr(chapter, 'chapter_name')
            assert hasattr(chapter, 'category')
            assert hasattr(chapter, 'difficulty')
            assert hasattr(chapter, 'estimated_study_hours')
            
            # Verify types
            assert isinstance(chapter.chapter_id, int)
            assert isinstance(chapter.chapter_name, str)
            assert isinstance(chapter.category, str)
            assert isinstance(chapter.difficulty, Difficulty)
            assert isinstance(chapter.estimated_study_hours, float)
            
            # Verify values
            assert chapter.chapter_id > 0
            assert len(chapter.chapter_name) > 0
            assert chapter.estimated_study_hours > 0
    
    def test_chapter_ids_unique(self):
        """Test that all chapter IDs are unique"""
        chapters = get_all_chapters()
        chapter_ids = [ch.chapter_id for ch in chapters]
        
        assert len(chapter_ids) == len(set(chapter_ids)), "Chapter IDs must be unique"
    
    def test_get_chapter_by_id(self):
        """Test retrieving a chapter by ID"""
        # Test valid ID
        chapter = get_chapter_by_id(1)
        assert chapter is not None
        assert chapter.chapter_id == 1
        
        # Test invalid ID
        chapter = get_chapter_by_id(9999)
        assert chapter is None
    
    def test_get_chapters_by_ids(self):
        """Test retrieving multiple chapters by IDs"""
        chapter_ids = [1, 2, 3]
        chapters = get_chapters_by_ids(chapter_ids)
        
        assert len(chapters) == 3
        retrieved_ids = [ch.chapter_id for ch in chapters]
        assert set(retrieved_ids) == set(chapter_ids)
    
    def test_get_chapters_by_category(self):
        """Test retrieving chapters by category"""
        history_chapters = get_chapters_by_category("History")
        assert len(history_chapters) > 0
        assert all(ch.category == "History" for ch in history_chapters)
        
        geography_chapters = get_chapters_by_category("Geography")
        assert len(geography_chapters) > 0
        assert all(ch.category == "Geography" for ch in geography_chapters)
        
        politics_chapters = get_chapters_by_category("Politics")
        assert len(politics_chapters) > 0
        assert all(ch.category == "Politics" for ch in politics_chapters)
        
        economics_chapters = get_chapters_by_category("Economics")
        assert len(economics_chapters) > 0
        assert all(ch.category == "Economics" for ch in economics_chapters)
    
    def test_all_categories_present(self):
        """Test that all four categories are represented"""
        all_chapters = get_all_chapters()
        categories = {ch.category for ch in all_chapters}
        
        expected_categories = {"History", "Geography", "Politics", "Economics"}
        assert categories == expected_categories
    
    def test_get_chapters_by_difficulty(self):
        """Test retrieving chapters by difficulty"""
        hard_chapters = get_chapters_by_difficulty(Difficulty.HARD)
        assert len(hard_chapters) > 0
        assert all(ch.difficulty == Difficulty.HARD for ch in hard_chapters)
        
        medium_chapters = get_chapters_by_difficulty(Difficulty.MEDIUM)
        assert len(medium_chapters) > 0
        assert all(ch.difficulty == Difficulty.MEDIUM for ch in medium_chapters)
        
        easy_chapters = get_chapters_by_difficulty(Difficulty.EASY)
        assert len(easy_chapters) > 0
        assert all(ch.difficulty == Difficulty.EASY for ch in easy_chapters)
    
    def test_all_difficulties_present(self):
        """Test that all difficulty levels are represented"""
        all_chapters = get_all_chapters()
        difficulties = {ch.difficulty for ch in all_chapters}
        
        expected_difficulties = {Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD}
        assert difficulties == expected_difficulties
    
    def test_get_total_study_hours(self):
        """Test calculating total study hours"""
        chapter_ids = [1, 2, 3]
        total_hours = get_total_study_hours(chapter_ids)
        
        assert total_hours > 0
        
        # Verify calculation
        chapters = get_chapters_by_ids(chapter_ids)
        expected_total = sum(ch.estimated_study_hours for ch in chapters)
        assert total_hours == expected_total
    
    def test_validate_chapter_ids_valid(self):
        """Test validation with valid chapter IDs"""
        valid_ids = [1, 2, 3, 4, 5]
        assert validate_chapter_ids(valid_ids) is True
    
    def test_validate_chapter_ids_invalid(self):
        """Test validation with invalid chapter IDs"""
        invalid_ids = [1, 2, 9999]
        assert validate_chapter_ids(invalid_ids) is False
        
        all_invalid = [8888, 9999]
        assert validate_chapter_ids(all_invalid) is False
    
    def test_validate_chapter_ids_empty(self):
        """Test validation with empty list"""
        assert validate_chapter_ids([]) is True  # Empty list is technically valid
    
    def test_difficulty_weights(self):
        """Test that difficulty weights are correctly defined"""
        hard_weight = get_difficulty_weight(Difficulty.HARD)
        medium_weight = get_difficulty_weight(Difficulty.MEDIUM)
        easy_weight = get_difficulty_weight(Difficulty.EASY)
        
        # Hard should have highest weight
        assert hard_weight > medium_weight
        assert hard_weight > easy_weight
        
        # Medium should be baseline
        assert medium_weight == 1.0
        
        # Easy should have lowest weight
        assert easy_weight < medium_weight
    
    def test_chapter_to_dict(self):
        """Test converting chapter to dictionary"""
        chapter = get_chapter_by_id(1)
        chapter_dict = chapter.to_dict()
        
        assert isinstance(chapter_dict, dict)
        assert 'chapter_id' in chapter_dict
        assert 'chapter_name' in chapter_dict
        assert 'category' in chapter_dict
        assert 'difficulty' in chapter_dict
        assert 'estimated_study_hours' in chapter_dict
        
        assert chapter_dict['chapter_id'] == chapter.chapter_id
        assert chapter_dict['chapter_name'] == chapter.chapter_name
    
    def test_chapter_repr(self):
        """Test chapter string representation"""
        chapter = get_chapter_by_id(1)
        repr_str = repr(chapter)
        
        assert isinstance(repr_str, str)
        assert str(chapter.chapter_id) in repr_str
        assert chapter.chapter_name in repr_str
    
    def test_realistic_study_hours(self):
        """Test that estimated study hours are realistic"""
        all_chapters = get_all_chapters()
        
        for chapter in all_chapters:
            # Study hours should be between 1 and 10 hours per chapter
            assert 1.0 <= chapter.estimated_study_hours <= 10.0, \
                f"Chapter {chapter.chapter_id} has unrealistic study hours"
    
    def test_difficulty_distribution(self):
        """Test that difficulty levels are reasonably distributed"""
        all_chapters = get_all_chapters()
        
        hard_count = len(get_chapters_by_difficulty(Difficulty.HARD))
        medium_count = len(get_chapters_by_difficulty(Difficulty.MEDIUM))
        easy_count = len(get_chapters_by_difficulty(Difficulty.EASY))
        
        total = len(all_chapters)
        
        # Each difficulty should have at least 20% representation
        assert hard_count >= total * 0.2
        assert medium_count >= total * 0.2
        assert easy_count >= total * 0.2
    
    def test_category_distribution(self):
        """Test that categories are reasonably distributed"""
        all_chapters = get_all_chapters()
        
        history_count = len(get_chapters_by_category("History"))
        geography_count = len(get_chapters_by_category("Geography"))
        politics_count = len(get_chapters_by_category("Politics"))
        economics_count = len(get_chapters_by_category("Economics"))
        
        total = len(all_chapters)
        
        # Each category should have at least 20% representation
        assert history_count >= total * 0.2
        assert geography_count >= total * 0.2
        assert politics_count >= total * 0.2
        assert economics_count >= total * 0.2
    
    def test_at_least_40_chapters(self):
        """Test that we have substantial chapter coverage"""
        all_chapters = get_all_chapters()
        assert len(all_chapters) >= 40, "Should have at least 40 chapters for comprehensive coverage"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
