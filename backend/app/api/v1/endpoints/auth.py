"""
Authentication Endpoints
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserRegister, UserLogin, TokenResponse, UserResponse, UserUpdate
from app.schemas.response import APIResponse
from app.services.user_service import UserService
from app.core.security import create_access_token
from app.core.config import settings
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user
    
    Args:
        user_data: User registration data
        db: Database session
        
    Returns:
        API response with user data and access token
    """
    try:
        # Create user
        user = UserService.create_user(db, user_data)
        
        # Create access token
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        # Prepare response
        user_response = UserResponse.model_validate(user)
        token_data = TokenResponse(
            access_token=access_token,
            user=user_response
        )
        
        return APIResponse(
            success=True,
            message="Registration successful",
            data=token_data.model_dump()
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=APIResponse)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return access token
    
    Args:
        user_data: User login credentials
        db: Database session
        
    Returns:
        API response with user data and access token
    """
    # Authenticate user
    user = UserService.authenticate_user(db, user_data.email, user_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    # Prepare response
    user_response = UserResponse.model_validate(user)
    token_data = TokenResponse(
        access_token=access_token,
        user=user_response
    )
    
    return APIResponse(
        success=True,
        message="Login successful",
        data=token_data.model_dump()
    )


@router.get("/me", response_model=APIResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        API response with user data
    """
    user_response = UserResponse.model_validate(current_user)
    
    return APIResponse(
        success=True,
        message="User retrieved successfully",
        data=user_response.model_dump()
    )


@router.put("/me", response_model=APIResponse)
def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user profile
    
    Args:
        user_data: Updated user data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        API response with updated user data
    """
    try:
        updated_user = UserService.update_user(db, current_user.id, user_data)
        user_response = UserResponse.model_validate(updated_user)
        
        return APIResponse(
            success=True,
            message="Profile updated successfully",
            data=user_response.model_dump()
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Update failed: {str(e)}"
        )
