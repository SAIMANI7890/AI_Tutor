"""
Models package
Import all models here to ensure they are registered with SQLAlchemy Base
"""
from app.models.user import User
from app.models.chat import ChatSession, ChatMessage
from app.models.study_plan import StudyPlan, StudyPlanItem
from app.models.test import Test
from app.models.test_question import TestQuestion
from app.models.student_test_answer import StudentTestAnswer
from app.models.evaluation import Evaluation
from app.models.enums import QuestionType, TestStatus, Difficulty, ActivityType, StudyStatus

__all__ = [
    "User",
    "ChatSession",
    "ChatMessage",
    "StudyPlan",
    "StudyPlanItem",
    "Test",
    "TestQuestion",
    "StudentTestAnswer",
    "Evaluation",
    "QuestionType",
    "TestStatus",
    "Difficulty",
    "ActivityType",
    "StudyStatus"
]
