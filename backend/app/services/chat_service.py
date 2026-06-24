"""
Chat Service
Business logic for chat sessions and messages
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from fastapi import HTTPException, status
from app.models.chat import ChatSession, ChatMessage
from app.models.user import User
from app.schemas.chat import ChatSessionCreate, ChatMessageResponse
import json
import logging

logger = logging.getLogger(__name__)


class ChatService:
    """Service for managing chat sessions and messages"""
    
    @staticmethod
    def create_session(db: Session, user_id: int, title: str = "New Conversation") -> ChatSession:
        """
        Create a new chat session
        
        Args:
            db: Database session
            user_id: User ID
            title: Session title
            
        Returns:
            Created chat session
        """
        session = ChatSession(
            user_id=user_id,
            title=title
        )
        
        db.add(session)
        db.commit()
        db.refresh(session)
        
        logger.info(f"Created chat session {session.id} for user {user_id}")
        return session
    
    @staticmethod
    def get_user_sessions(db: Session, user_id: int) -> List[dict]:
        """
        Get all chat sessions for a user with summary info
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            List of chat sessions with metadata
        """
        # Get sessions with message count and last message
        sessions = db.query(ChatSession).filter(
            ChatSession.user_id == user_id
        ).order_by(desc(ChatSession.updated_at)).all()
        
        session_list = []
        for session in sessions:
            # Get message count
            message_count = db.query(func.count(ChatMessage.id)).filter(
                ChatMessage.session_id == session.id
            ).scalar()
            
            # Get last message
            last_message = db.query(ChatMessage).filter(
                ChatMessage.session_id == session.id,
                ChatMessage.role == "user"
            ).order_by(desc(ChatMessage.created_at)).first()
            
            session_dict = {
                "id": session.id,
                "user_id": session.user_id,
                "title": session.title,
                "created_at": session.created_at,
                "updated_at": session.updated_at,
                "message_count": message_count,
                "last_message": last_message.message[:100] if last_message else None
            }
            session_list.append(session_dict)
        
        return session_list
    
    @staticmethod
    def get_session_by_id(db: Session, session_id: int, user_id: int) -> ChatSession:
        """
        Get a chat session by ID
        
        Args:
            db: Database session
            session_id: Session ID
            user_id: User ID (for authorization)
            
        Returns:
            Chat session
            
        Raises:
            HTTPException: If session not found or unauthorized
        """
        session = db.query(ChatSession).filter(
            ChatSession.id == session_id
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found"
            )
        
        if session.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this session"
            )
        
        return session
    
    @staticmethod
    def delete_session(db: Session, session_id: int, user_id: int) -> None:
        """
        Delete a chat session
        
        Args:
            db: Database session
            session_id: Session ID
            user_id: User ID (for authorization)
        """
        session = ChatService.get_session_by_id(db, session_id, user_id)
        
        db.delete(session)
        db.commit()
        
        logger.info(f"Deleted chat session {session_id}")
    
    @staticmethod
    def add_message(
        db: Session,
        session_id: int,
        role: str,
        message: str,
        sources: Optional[List[dict]] = None
    ) -> ChatMessage:
        """
        Add a message to a chat session
        
        Args:
            db: Database session
            session_id: Session ID
            role: Message role ('user' or 'assistant')
            message: Message content
            sources: Optional list of sources
            
        Returns:
            Created chat message
        """
        # Convert sources to JSON string if provided
        sources_json = json.dumps(sources) if sources else None
        
        chat_message = ChatMessage(
            session_id=session_id,
            role=role,
            message=message,
            sources=sources_json
        )
        
        db.add(chat_message)
        
        # Update session updated_at
        session = db.query(ChatSession).filter(
            ChatSession.id == session_id
        ).first()
        if session:
            session.updated_at = func.now()
        
        db.commit()
        db.refresh(chat_message)
        
        return chat_message
    
    @staticmethod
    def get_session_messages(db: Session, session_id: int, user_id: int) -> List[ChatMessage]:
        """
        Get all messages in a session
        
        Args:
            db: Database session
            session_id: Session ID
            user_id: User ID (for authorization)
            
        Returns:
            List of chat messages
        """
        # Verify session belongs to user
        ChatService.get_session_by_id(db, session_id, user_id)
        
        messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.created_at).all()
        
        return messages
    
    @staticmethod
    def update_session_title(
        db: Session,
        session_id: int,
        user_id: int,
        title: str
    ) -> ChatSession:
        """
        Update session title
        
        Args:
            db: Database session
            session_id: Session ID
            user_id: User ID (for authorization)
            title: New title
            
        Returns:
            Updated session
        """
        session = ChatService.get_session_by_id(db, session_id, user_id)
        
        session.title = title
        db.commit()
        db.refresh(session)
        
        return session
