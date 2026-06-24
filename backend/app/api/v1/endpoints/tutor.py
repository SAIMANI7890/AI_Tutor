"""
AI Tutor API Endpoints
Handles AI tutoring chat interactions
"""
import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.chat import TutorChatRequest, TutorChatResponse
from app.schemas.response import APIResponse
from app.services.tutor_service import TutorService
from app.services.chat_service import ChatService
from app.api.dependencies import get_current_user
from app.models.user import User
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize tutor service (singleton)
_tutor_service = None


def get_tutor_service() -> TutorService:
    """Get or create tutor service instance"""
    global _tutor_service
    
    if _tutor_service is None:
        # Get configuration from environment or settings
        api_key = os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY
        if not api_key or api_key.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="GEMINI_API_KEY not configured. Please set the API key in your environment variables or .env file."
            )
        
        chroma_db_path = os.getenv("CHROMA_DB_PATH", "./chroma_db")
        top_k = int(os.getenv("TOP_K_RESULTS", "5"))
        
        try:
            _tutor_service = TutorService(
                api_key=api_key,
                chroma_db_path=chroma_db_path,
                top_k=top_k
            )
            logger.info("Tutor service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize tutor service: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to initialize AI tutor. Please ensure the knowledge base has been ingested."
            )
    
    return _tutor_service


@router.post("/chat", response_model=APIResponse)
async def chat_with_tutor(
    chat_request: TutorChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    tutor_service: TutorService = Depends(get_tutor_service)
):
    """
    Chat with AI tutor
    
    Args:
        chat_request: Chat request containing session_id and question
        current_user: Current authenticated user
        db: Database session
        tutor_service: AI tutor service
        
    Returns:
        API response with answer and sources
    """
    try:
        # Verify session belongs to user
        session = ChatService.get_session_by_id(
            db=db,
            session_id=chat_request.session_id,
            user_id=current_user.id
        )
        
        # Save user message
        user_message = ChatService.add_message(
            db=db,
            session_id=chat_request.session_id,
            role="user",
            message=chat_request.question
        )
        
        logger.info(f"User {current_user.id} asked: {chat_request.question[:50]}...")
        
        # Get answer from AI tutor
        result = tutor_service.answer_question(chat_request.question)
        
        # Save assistant response
        assistant_message = ChatService.add_message(
            db=db,
            session_id=chat_request.session_id,
            role="assistant",
            message=result["answer"],
            sources=result["sources"]
        )
        
        # Prepare response
        response_data = TutorChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            message_id=assistant_message.id,
            session_id=chat_request.session_id
        )
        
        return APIResponse(
            success=True,
            message="Answer generated successfully",
            data=response_data.model_dump()
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process question: {str(e)}"
        )


@router.get("/health", response_model=APIResponse)
def check_tutor_health(tutor_service: TutorService = Depends(get_tutor_service)):
    """
    Check if tutor service is healthy and ready
    
    Returns:
        API response with health status
    """
    try:
        # Check if vector store has data
        collection_count = tutor_service.retriever.collection.count()
        
        return APIResponse(
            success=True,
            message="AI Tutor is ready",
            data={
                "status": "healthy",
                "chunks_loaded": collection_count,
                "model": "gemini-2.5-flash-lite"
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI Tutor service is not ready"
        )
