"""
Standard API Response Schemas
"""
from typing import Any, List, Optional
from pydantic import BaseModel


class APIResponse(BaseModel):
    """Standard API response format"""
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[List[str]] = None
    
    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Error response format"""
    success: bool = False
    message: str
    errors: List[str] = []
    
    class Config:
        from_attributes = True
