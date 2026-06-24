"""
Chat API Endpoints
Handles chat session management
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.chat import (
    ChatSessionCreate,
    ChatSessionResponse,
    ChatSessionDetail,
    ChatMessageResponse
)
from app.schemas.response import APIResponse
from app.services.chat_service import ChatService
from app.api.dependencies import get_current_user
from app.models.user import User
import json

router = APIRouter()


@router.post("/session", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def create_chat_session(
    session_data: ChatSessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new chat session
    
    Args:
        session_data: Session creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        API response with created session
    """
    try:
        session = ChatService.create_session(
            db=db,
            user_id=current_user.id,
            title=session_data.title
        )
        
        session_response = ChatSessionResponse(
            id=session.id,
            user_id=session.user_id,
            title=session.title,
            created_at=session.created_at,
            updated_at=session.updated_at,
            message_count=0
        )
        
        return APIResponse(
            success=True,
            message="Chat session created successfully",
            data=session_response.model_dump()
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create session: {str(e)}"
        )


@router.get("/sessions", response_model=APIResponse)
def get_user_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all chat sessions for current user
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        API response with list of sessions
    """
    sessions = ChatService.get_user_sessions(db=db, user_id=current_user.id)
    
    return APIResponse(
        success=True,
        message="Sessions retrieved successfully",
        data={"sessions": sessions}
    )


@router.get("/session/{session_id}", response_model=APIResponse)
def get_chat_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific chat session with all messages
    
    Args:
        session_id: Session ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        API response with session and messages
    """
    try:
        session = ChatService.get_session_by_id(
            db=db,
            session_id=session_id,
            user_id=current_user.id
        )
        
        messages = ChatService.get_session_messages(
            db=db,
            session_id=session_id,
            user_id=current_user.id
        )
        
        # Format messages
        formatted_messages = []
        for msg in messages:
            sources = json.loads(msg.sources) if msg.sources else []
            formatted_messages.append({
                "id": msg.id,
                "session_id": msg.session_id,
                "role": msg.role,
                "message": msg.message,
                "sources": sources,
                "created_at": msg.created_at
            })
        
        response_data = {
            "id": session.id,
            "user_id": session.user_id,
            "title": session.title,
            "created_at": session.created_at,
            "updated_at": session.updated_at,
            "messages": formatted_messages
        }
        
        return APIResponse(
            success=True,
            message="Session retrieved successfully",
            data=response_data
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve session: {str(e)}"
        )


@router.delete("/session/{session_id}", response_model=APIResponse)
def delete_chat_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a chat session
    
    Args:
        session_id: Session ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        API response confirming deletion
    """
    try:
        ChatService.delete_session(
            db=db,
            session_id=session_id,
            user_id=current_user.id
        )
        
        return APIResponse(
            success=True,
            message="Session deleted successfully",
            data=None
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete session: {str(e)}"
        )


@router.put("/session/{session_id}/title", response_model=APIResponse)
def update_session_title(
    session_id: int,
    title_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update session title
    
    Args:
        session_id: Session ID
        title_data: Dictionary with 'title' key
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        API response with updated session
    """
    try:
        session = ChatService.update_session_title(
            db=db,
            session_id=session_id,
            user_id=current_user.id,
            title=title_data.get("title", "New Conversation")
        )
        
        session_response = ChatSessionResponse(
            id=session.id,
            user_id=session.user_id,
            title=session.title,
            created_at=session.created_at,
            updated_at=session.updated_at
        )
        
        return APIResponse(
            success=True,
            message="Session title updated successfully",
            data=session_response.model_dump()
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update session: {str(e)}"
        )
