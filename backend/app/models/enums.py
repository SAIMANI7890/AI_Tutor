"""
Enums for the application
Centralized enum definitions for consistency
"""
from enum import Enum


class QuestionType(str, Enum):
    """
    Types of questions that can be generated
    """
    MCQ = "MCQ"
    FILL_BLANKS = "FILL_BLANKS"
    SHORT_ANSWER = "SHORT_ANSWER"
    LONG_ANSWER = "LONG_ANSWER"


class TestStatus(str, Enum):
    """
    Status workflow for tests:
    GENERATED → IN_PROGRESS → SUBMITTED → EVALUATED
    """
    GENERATED = "GENERATED"      # Test created, questions generated
    IN_PROGRESS = "IN_PROGRESS"  # Student has started answering
    SUBMITTED = "SUBMITTED"      # Student submitted all answers
    EVALUATED = "EVALUATED"      # Answers have been evaluated (Phase 5)


class Difficulty(str, Enum):
    """
    Difficulty levels for chapters and questions
    Used in study planner and examination modules
    """
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class ActivityType(str, Enum):
    """
    Types of study activities in the planner
    """
    STUDY = "Study"
    REVISION = "Revision"
    MOCK_TEST = "MockTest"


class StudyStatus(str, Enum):
    """
    Status of study plan items
    """
    PENDING = "Pending"
    COMPLETED = "Completed"
    SKIPPED = "Skipped"
