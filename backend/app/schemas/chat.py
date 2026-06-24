"""
Chat Schemas
Pydantic schemas for chat-related requests and responses
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# Chat Message Schemas
class ChatMessageBase(BaseModel):
    """Base chat message schema"""
    role: str
    message: str


class ChatMessageCreate(BaseModel):
    """Schema for creating a chat message"""
    session_id: int
    question: str = Field(..., min_length=1)


class SourceInfo(BaseModel):
    """Schema for source information"""
    document: str
    page: int
    category: str


class ChatMessageResponse(BaseModel):
    """Schema for chat message response"""
    id: int
    session_id: int
    role: str
    message: str
    sources: Optional[List[SourceInfo]] = []
    created_at: datetime
    
    class Config:
        from_attributes = True


# Chat Session Schemas
class ChatSessionCreate(BaseModel):
    """Schema for creating a chat session"""
    title: Optional[str] = "New Conversation"


class ChatSessionResponse(BaseModel):
    """Schema for chat session response"""
    id: int
    user_id: int
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = 0
    last_message: Optional[str] = None
    
    class Config:
        from_attributes = True


class ChatSessionDetail(BaseModel):
    """Schema for detailed chat session with messages"""
    id: int
    user_id: int
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[ChatMessageResponse]
    
    class Config:
        from_attributes = True


# Tutor Chat Schemas
class TutorChatRequest(BaseModel):
    """Schema for tutor chat request"""
    session_id: int
    question: str = Field(..., min_length=1, max_length=1000)


class TutorChatResponse(BaseModel):
    """Schema for tutor chat response"""
    answer: str
    sources: List[SourceInfo]
    message_id: int
    session_id: int
