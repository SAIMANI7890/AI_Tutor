"""
Chapter Configuration
Metadata for all Social Studies chapters

This configuration allows adding new chapters without modifying algorithm code.
Each chapter contains: ID, name, category, difficulty, and estimated study hours.
"""
from typing import List, Dict, Optional
from enum import Enum


class Difficulty(str, Enum):
    """Difficulty levels for chapters"""
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class Chapter:
    """Chapter metadata model"""
    
    def __init__(
        self,
        chapter_id: int,
        chapter_name: str,
        category: str,
        difficulty: Difficulty,
        estimated_study_hours: float
    ):
        self.chapter_id = chapter_id
        self.chapter_name = chapter_name
        self.category = category
        self.difficulty = difficulty
        self.estimated_study_hours = estimated_study_hours
    
    def to_dict(self) -> Dict:
        """Convert chapter to dictionary"""
        return {
            "chapter_id": self.chapter_id,
            "chapter_name": self.chapter_name,
            "category": self.category,
            "difficulty": self.difficulty.value,
            "estimated_study_hours": self.estimated_study_hours
        }
    
    def __repr__(self):
        return f"<Chapter {self.chapter_id}: {self.chapter_name} ({self.difficulty.value})>"


# ============================================================
# SOCIAL STUDIES CHAPTERS CONFIGURATION
# ============================================================

CHAPTERS: List[Chapter] = [
    # ===== HISTORY CHAPTERS =====
    Chapter(
        chapter_id=1,
        chapter_name="French Revolution",
        category="History",
        difficulty=Difficulty.HARD,
        estimated_study_hours=5.0
    ),
    Chapter(
        chapter_id=2,
        chapter_name="Industrial Revolution",
        category="History",
        difficulty=Difficulty.HARD,
        estimated_study_hours=4.5
    ),
    Chapter(
        chapter_id=3,
        chapter_name="World War I",
        category="History",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=4.0
    ),
    Chapter(
        chapter_id=4,
        chapter_name="World War II",
        category="History",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=4.0
    ),
    Chapter(
        chapter_id=5,
        chapter_name="Colonialism and Imperialism",
        category="History",
        difficulty=Difficulty.HARD,
        estimated_study_hours=5.0
    ),
    Chapter(
        chapter_id=6,
        chapter_name="The Renaissance",
        category="History",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=3.5
    ),
    Chapter(
        chapter_id=7,
        chapter_name="Indian Independence Movement",
        category="History",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=4.0
    ),
    Chapter(
        chapter_id=8,
        chapter_name="Cold War Era",
        category="History",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=3.5
    ),
    Chapter(
        chapter_id=9,
        chapter_name="Ancient Civilizations",
        category="History",
        difficulty=Difficulty.EASY,
        estimated_study_hours=3.0
    ),
    Chapter(
        chapter_id=10,
        chapter_name="Medieval Period",
        category="History",
        difficulty=Difficulty.EASY,
        estimated_study_hours=3.0
    ),
    
    # ===== GEOGRAPHY CHAPTERS =====
    Chapter(
        chapter_id=11,
        chapter_name="Climate and Weather Patterns",
        category="Geography",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=3.5
    ),
    Chapter(
        chapter_id=12,
        chapter_name="Monsoon Systems",
        category="Geography",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=3.0
    ),
    Chapter(
        chapter_id=13,
        chapter_name="Major Rivers and Water Bodies",
        category="Geography",
        difficulty=Difficulty.EASY,
        estimated_study_hours=2.5
    ),
    Chapter(
        chapter_id=14,
        chapter_name="Mountain Ranges and Plateaus",
        category="Geography",
        difficulty=Difficulty.EASY,
        estimated_study_hours=2.5
    ),
    Chapter(
        chapter_id=15,
        chapter_name="Natural Resources",
        category="Geography",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=3.5
    ),
    Chapter(
        chapter_id=16,
        chapter_name="Soil Types and Agriculture",
        category="Geography",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=3.0
    ),
    Chapter(
        chapter_id=17,
        chapter_name="Population Distribution",
        category="Geography",
        difficulty=Difficulty.EASY,
        estimated_study_hours=2.5
    ),
    Chapter(
        chapter_id=18,
        chapter_name="Environmental Issues",
        category="Geography",
        difficulty=Difficulty.HARD,
        estimated_study_hours=4.0
    ),
    Chapter(
        chapter_id=19,
        chapter_name="Map Reading and Skills",
        category="Geography",
        difficulty=Difficulty.EASY,
        estimated_study_hours=2.0
    ),
    Chapter(
        chapter_id=20,
        chapter_name="Climate Zones",
        category="Geography",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=3.0
    ),
    
    # ===== POLITICS CHAPTERS =====
    Chapter(
        chapter_id=21,
        chapter_name="Democracy and Its Features",
        category="Politics",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=3.5
    ),
    Chapter(
        chapter_id=22,
        chapter_name="Constitutional Framework",
        category="Politics",
        difficulty=Difficulty.HARD,
        estimated_study_hours=4.5
    ),
    Chapter(
        chapter_id=23,
        chapter_name="Fundamental Rights",
        category="Politics",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=3.5
    ),
    Chapter(
        chapter_id=24,
        chapter_name="Directive Principles",
        category="Politics",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=3.0
    ),
    Chapter(
        chapter_id=25,
        chapter_name="Three Branches of Government",
        category="Politics",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=4.0
    ),
    Chapter(
        chapter_id=26,
        chapter_name="Electoral System",
        category="Politics",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=3.5
    ),
    Chapter(
        chapter_id=27,
        chapter_name="Political Parties",
        category="Politics",
        difficulty=Difficulty.EASY,
        estimated_study_hours=2.5
    ),
    Chapter(
        chapter_id=28,
        chapter_name="Local Self-Government",
        category="Politics",
        difficulty=Difficulty.EASY,
        estimated_study_hours=2.5
    ),
    Chapter(
        chapter_id=29,
        chapter_name="Judiciary and Legal System",
        category="Politics",
        difficulty=Difficulty.HARD,
        estimated_study_hours=4.0
    ),
    Chapter(
        chapter_id=30,
        chapter_name="Federal Structure",
        category="Politics",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=3.5
    ),
    
    # ===== ECONOMICS CHAPTERS =====
    Chapter(
        chapter_id=31,
        chapter_name="Supply and Demand",
        category="Economics",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=3.5
    ),
    Chapter(
        chapter_id=32,
        chapter_name="Economic Systems",
        category="Economics",
        difficulty=Difficulty.HARD,
        estimated_study_hours=4.5
    ),
    Chapter(
        chapter_id=33,
        chapter_name="National Income and GDP",
        category="Economics",
        difficulty=Difficulty.HARD,
        estimated_study_hours=4.0
    ),
    Chapter(
        chapter_id=34,
        chapter_name="Money and Banking",
        category="Economics",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=3.5
    ),
    Chapter(
        chapter_id=35,
        chapter_name="Inflation and Deflation",
        category="Economics",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=3.0
    ),
    Chapter(
        chapter_id=36,
        chapter_name="International Trade",
        category="Economics",
        difficulty=Difficulty.HARD,
        estimated_study_hours=4.0
    ),
    Chapter(
        chapter_id=37,
        chapter_name="Poverty and Unemployment",
        category="Economics",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=3.5
    ),
    Chapter(
        chapter_id=38,
        chapter_name="Economic Development",
        category="Economics",
        difficulty=Difficulty.MEDIUM,
        estimated_study_hours=3.5
    ),
    Chapter(
        chapter_id=39,
        chapter_name="Consumer Rights",
        category="Economics",
        difficulty=Difficulty.EASY,
        estimated_study_hours=2.5
    ),
    Chapter(
        chapter_id=40,
        chapter_name="Globalization",
        category="Economics",
        difficulty=Difficulty.HARD,
        estimated_study_hours=4.0
    ),
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_all_chapters() -> List[Chapter]:
    """Get all available chapters"""
    return CHAPTERS


def get_chapter_by_id(chapter_id: int) -> Optional[Chapter]:
    """Get a specific chapter by ID"""
    for chapter in CHAPTERS:
        if chapter.chapter_id == chapter_id:
            return chapter
    return None


def get_chapters_by_ids(chapter_ids: List[int]) -> List[Chapter]:
    """Get multiple chapters by their IDs"""
    return [chapter for chapter in CHAPTERS if chapter.chapter_id in chapter_ids]


def get_chapters_by_category(category: str) -> List[Chapter]:
    """Get all chapters in a specific category"""
    return [chapter for chapter in CHAPTERS if chapter.category == category]


def get_chapters_by_difficulty(difficulty: Difficulty) -> List[Chapter]:
    """Get all chapters with a specific difficulty level"""
    return [chapter for chapter in CHAPTERS if chapter.difficulty == difficulty]


def get_total_study_hours(chapter_ids: List[int]) -> float:
    """Calculate total estimated study hours for given chapters"""
    chapters = get_chapters_by_ids(chapter_ids)
    return sum(chapter.estimated_study_hours for chapter in chapters)


def validate_chapter_ids(chapter_ids: List[int]) -> bool:
    """Validate if all chapter IDs exist"""
    valid_ids = {chapter.chapter_id for chapter in CHAPTERS}
    return all(cid in valid_ids for cid in chapter_ids)


# ============================================================
# DIFFICULTY WEIGHTS FOR SCHEDULING
# ============================================================

DIFFICULTY_WEIGHTS = {
    Difficulty.HARD: 1.5,    # Hard chapters get 50% more sessions
    Difficulty.MEDIUM: 1.0,  # Medium chapters baseline
    Difficulty.EASY: 0.7     # Easy chapters get 30% fewer sessions
}


def get_difficulty_weight(difficulty: Difficulty) -> float:
    """Get the scheduling weight for a difficulty level"""
    return DIFFICULTY_WEIGHTS.get(difficulty, 1.0)
