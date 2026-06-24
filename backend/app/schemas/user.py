"""
User Schemas for Request/Response validation
"""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator


# Request Schemas
class UserRegister(BaseModel):
    """Schema for user registration"""
    full_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str = Field(..., min_length=8, max_length=100)
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Validate that password and confirm_password match"""
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    
    class Config:
        from_attributes = True


# Response Schemas
class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    full_name: str
    email: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: str = Field(..., min_length=2, max_length=255)
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    
    class Config:
        from_attributes = True
