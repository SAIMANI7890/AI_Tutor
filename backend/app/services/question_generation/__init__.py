"""
Question Generation Service Package
Generates examination questions using RAG and Gemini AI
"""
from app.services.question_generation.generator import QuestionGeneratorService
from app.services.question_generation.schemas import (
    ExamGenerationRequest,
    ExamGenerationResponse,
    GeneratedQuestion
)

__all__ = [
    "QuestionGeneratorService",
    "ExamGenerationRequest",
    "ExamGenerationResponse",
    "GeneratedQuestion"
]
