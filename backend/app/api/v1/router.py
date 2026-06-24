"""
Main API Router
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, chat, tutor, study_plans, exams, evaluations

api_router = APIRouter()

# Include authentication routes
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Include chat routes
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])

# Include tutor routes
api_router.include_router(tutor.router, prefix="/tutor", tags=["AI Tutor"])

# Include study plans routes
api_router.include_router(study_plans.router, prefix="/study-plans", tags=["Study Plans"])

# Include examination routes (Phase 4C)
api_router.include_router(exams.router, prefix="/exams", tags=["Examinations"])

# Include evaluation routes (Phase 7B)
api_router.include_router(evaluations.router, prefix="/evaluations", tags=["Evaluations"])
