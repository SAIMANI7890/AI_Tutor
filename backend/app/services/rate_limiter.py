"""
Rate Limiting Service
Protects expensive AI operations from abuse
"""
import time
from typing import Dict
from datetime import datetime, timedelta
from fastapi import HTTPException, status


class RateLimiter:
    """
    In-memory rate limiter for exam generation
    
    For production, replace with Redis-based solution
    """
    
    def __init__(self):
        # user_id -> List[(timestamp, count)]
        self._attempts: Dict[int, list] = {}
        
        # Configuration
        self.MAX_EXAMS_PER_HOUR = 5
        self.WINDOW_SECONDS = 3600  # 1 hour
        
    def check_limit(self, user_id: int) -> None:
        """
        Check if user has exceeded rate limit
        
        Args:
            user_id: User ID to check
            
        Raises:
            HTTPException 429: Rate limit exceeded
        """
        now = time.time()
        window_start = now - self.WINDOW_SECONDS
        
        # Get user's attempts
        if user_id not in self._attempts:
            self._attempts[user_id] = []
        
        # Remove expired attempts
        self._attempts[user_id] = [
            timestamp for timestamp in self._attempts[user_id]
            if timestamp > window_start
        ]
        
        # Check limit
        if len(self._attempts[user_id]) >= self.MAX_EXAMS_PER_HOUR:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {self.MAX_EXAMS_PER_HOUR} exam generations per hour."
            )
        
        # Record this attempt
        self._attempts[user_id].append(now)
    
    def reset_user(self, user_id: int) -> None:
        """Reset rate limit for a user (admin function)"""
        if user_id in self._attempts:
            del self._attempts[user_id]


# Global rate limiter instance
_rate_limiter = RateLimiter()


def check_exam_generation_limit(user_id: int) -> None:
    """
    Check if user can generate an exam
    
    Args:
        user_id: User ID
        
    Raises:
        HTTPException 429: Too many requests
    """
    _rate_limiter.check_limit(user_id)


def reset_user_limit(user_id: int) -> None:
    """Reset user's rate limit (admin function)"""
    _rate_limiter.reset_user(user_id)
