# ⚡ CRITICAL FIXES - QUICK START GUIDE
**Copy-paste ready code for immediate production readiness improvements**

## 🔴 PRIORITY 1: Redis-Based Rate Limiter

### 1. Install Dependencies
```bash
pip install redis aioredis
```

### 2. Create Redis Client
**File**: `backend/app/core/redis_client.py`

```python
"""Redis client configuration"""
import redis
from app.core.config import settings

# Synchronous Redis client
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_keepalive=True,
    health_check_interval=30
)

def get_redis():
    """Dependency for FastAPI routes"""
    return redis_client
```

### 3. Production Rate Limiter
**File**: `backend/app/services/production_rate_limiter.py`

```python
"""Production-grade Redis-based rate limiter"""
import time
from typing import Optional
from redis import Redis
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

class ProductionRateLimiter:
    """Redis-backed rate limiter for distributed systems"""
    
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.MAX_EXAMS_PER_HOUR = 5
        self.WINDOW_SECONDS = 3600
    
    def check_limit(
        self, 
        user_id: int, 
        resource: str = "exam_generation"
    ) -> None:
        """
        Check if user has exceeded rate limit
        
        Args:
            user_id: User ID
            resource: Resource being rate limited
            
        Raises:
            HTTPException 429: Rate limit exceeded
        """
        key = f"rate_limit:{resource}:{user_id}"
        now = int(time.time())
        
        try:
            # Use Redis sorted set for sliding window
            pipe = self.redis.pipeline()
            
            # Remove old entries outside the window
            pipe.zremrangebyscore(key, 0, now - self.WINDOW_SECONDS)
            
            # Count attempts in current window
            pipe.zcard(key)
            
            # Add current attempt
            pipe.zadd(key, {str(now): now})
            
            # Set expiry
            pipe.expire(key, self.WINDOW_SECONDS)
            
            results = pipe.execute()
            attempt_count = results[1]
            
            if attempt_count >= self.MAX_EXAMS_PER_HOUR:
                logger.warning(
                    f"Rate limit exceeded for user {user_id}: "
                    f"{attempt_count}/{self.MAX_EXAMS_PER_HOUR}"
                )
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "error": "rate_limit_exceeded",
                        "message": f"Maximum {self.MAX_EXAMS_PER_HOUR} "
                                   f"exam generations per hour.",
                        "retry_after": self.get_retry_after(user_id, resource)
                    }
                )
            
            logger.info(
                f"Rate limit check passed for user {user_id}: "
                f"{attempt_count + 1}/{self.MAX_EXAMS_PER_HOUR}"
            )
            
        except redis.RedisError as e:
            logger.error(f"Redis error in rate limiting: {e}")
            # Fail open - allow request if Redis is down
            logger.warning("Rate limiting disabled due to Redis error")
    
    def get_retry_after(self, user_id: int, resource: str) -> int:
        """Get seconds until rate limit resets"""
        key = f"rate_limit:{resource}:{user_id}"
        oldest = self.redis.zrange(key, 0, 0, withscores=True)
        
        if oldest:
            oldest_timestamp = int(oldest[0][1])
            retry_after = self.WINDOW_SECONDS - (int(time.time()) - oldest_timestamp)
            return max(0, retry_after)
        return 0
    
    def reset_user(self, user_id: int, resource: str = "exam_generation") -> None:
        """Reset rate limit for a user (admin function)"""
        key = f"rate_limit:{resource}:{user_id}"
        self.redis.delete(key)
        logger.info(f"Reset rate limit for user {user_id}, resource {resource}")

# Global instance
_rate_limiter: Optional[ProductionRateLimiter] = None

def get_rate_limiter(redis_client: Redis) -> ProductionRateLimiter:
    """Get or create rate limiter instance"""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = ProductionRateLimiter(redis_client)
    return _rate_limiter
```


### 4. Update exam endpoint
**File**: `backend/app/api/v1/endpoints/exams.py`

```python
# Replace old import:
# from app.services.rate_limiter import check_exam_generation_limit

# With new import:
from app.core.redis_client import get_redis
from app.services.production_rate_limiter import get_rate_limiter

@router.post("/generate", ...)
def generate_exam(
    request_body: ExamGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),  # Add Redis dependency
):
    # NEW: Use production rate limiter
    rate_limiter = get_rate_limiter(redis)
    rate_limiter.check_limit(current_user.id, "exam_generation")
    
    # Rest of your code...
```

### 5. Update config
**File**: `backend/app/core/config.py`

```python
class Settings(BaseSettings):
    # Existing settings...
    
    # NEW: Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    class Config:
        env_file = ".env"
```

### 6. Update .env
```env
# Add to .env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=your_redis_password_here
```

---

## 🔴 PRIORITY 2: Database Connection Pooling

**File**: `backend/app/db/session.py`

```python
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# PRODUCTION ENGINE with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,              # Max connections in pool
    max_overflow=40,           # Additional connections if pool exhausted
    pool_timeout=30,           # Wait 30s for connection
    pool_recycle=3600,         # Recycle connections after 1 hour
    pool_pre_ping=True,        # Test connections before use
    echo=False,                # Disable SQL logging in production
    connect_args={
        "connect_timeout": 10,
        "application_name": "ai_study_companion"
    }
)

# Event listeners for monitoring
@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    logger.debug("Database connection established")

@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_conn, connection_record, connection_proxy):
    logger.debug("Connection checked out from pool")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```


---

## 🔴 PRIORITY 3: Health Check Endpoints

**File**: `backend/app/api/v1/endpoints/health.py`

```python
"""Health check endpoints for load balancer and monitoring"""
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.redis_client import get_redis
from redis import Redis
import logging

router = APIRouter(tags=["Health"])
logger = logging.getLogger(__name__)

@router.get("/health", status_code=200)
def health_check():
    """
    Basic health check - returns 200 if application is running
    Used by: Load balancer basic health monitoring
    """
    return {"status": "healthy", "service": "ai-study-companion"}

@router.get("/health/ready")
def readiness_check(
    response: Response,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    """
    Readiness check - verifies all dependencies are available
    Used by: Kubernetes readiness probe, deployment verification
    
    Returns 200 if ready, 503 if not ready
    """
    checks = {
        "database": "unknown",
        "redis": "unknown",
        "vector_store": "unknown"
    }
    
    all_healthy = True
    
    # Check database
    try:
        db.execute("SELECT 1")
        checks["database"] = "connected"
        logger.debug("Database health check passed")
    except Exception as e:
        checks["database"] = f"error: {str(e)}"
        all_healthy = False
        logger.error(f"Database health check failed: {e}")
    
    # Check Redis
    try:
        redis.ping()
        checks["redis"] = "connected"
        logger.debug("Redis health check passed")
    except Exception as e:
        checks["redis"] = f"error: {str(e)}"
        all_healthy = False
        logger.error(f"Redis health check failed: {e}")
    
    # Check ChromaDB (optional - can be slow)
    try:
        from app.rag.retriever.retriever_service import RetrieverService
        retriever = RetrieverService(use_local=True)
        chunk_count = retriever.get_chunk_count()
        checks["vector_store"] = f"connected ({chunk_count} chunks)"
        logger.debug(f"Vector store health check passed: {chunk_count} chunks")
    except Exception as e:
        checks["vector_store"] = f"error: {str(e)}"
        # Vector store failure is not critical for readiness
        logger.warning(f"Vector store health check failed: {e}")
    
    if all_healthy:
        return {
            "status": "ready",
            "checks": checks
        }
    else:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "status": "not_ready",
            "checks": checks
        }

@router.get("/health/live")
def liveness_check():
    """
    Liveness check - simple check that process is alive
    Used by: Kubernetes liveness probe
    
    If this fails, container should be restarted
    """
    return {"status": "alive"}
```

**Register in router** (`backend/app/api/v1/router.py`):
```python
from app.api.v1.endpoints import health

api_router.include_router(health.router, tags=["Health"])
```


---

## 🔴 PRIORITY 4: Basic Monitoring (Sentry)

### 1. Install Sentry
```bash
pip install sentry-sdk[fastapi]
```

### 2. Configure Sentry
**File**: `backend/app/main.py`

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from app.core.config import settings

# Initialize Sentry BEFORE creating FastAPI app
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,  # "production", "staging", "development"
        traces_sample_rate=0.1,  # 10% of transactions for performance monitoring
        profiles_sample_rate=0.1,  # 10% for profiling
        integrations=[
            FastApiIntegration(transaction_style="url"),
            SqlalchemyIntegration(),
        ],
        # Don't send PII
        send_default_pii=False,
        # Custom tags
        before_send=lambda event, hint: event,
    )

app = FastAPI(...)

# Add user context to Sentry
@app.middleware("http")
async def add_sentry_context(request: Request, call_next):
    # Extract user from JWT if present
    auth_header = request.headers.get("authorization")
    if auth_header:
        try:
            from app.core.security import decode_access_token
            token = auth_header.replace("Bearer ", "")
            payload = decode_access_token(token)
            if payload:
                sentry_sdk.set_user({
                    "id": payload.get("sub"),
                    "email": payload.get("email")
                })
        except:
            pass
    
    response = await call_next(request)
    return response
```

### 3. Update config
```python
class Settings(BaseSettings):
    # Existing...
    
    # NEW: Sentry
    SENTRY_DSN: Optional[str] = None
    ENVIRONMENT: str = "development"  # production, staging, development
```

### 4. Manual error capture
```python
# In your services:
try:
    result = generate_exam(...)
except Exception as e:
    logger.error(f"Exam generation failed: {e}", exc_info=True)
    sentry_sdk.capture_exception(e)
    raise
```

---

## 🔴 PRIORITY 5: Security Headers

**File**: `backend/app/main.py`

```python
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""
    
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        
        # Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' https://api.yourdomain.com;"
        )
        
        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        
        # Prevent MIME sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # XSS Protection (legacy but still useful)
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Permissions Policy
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )
        
        return response

# Add middleware to app
app.add_middleware(SecurityHeadersMiddleware)

# CORS - STRICT CONFIGURATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://app.yourdomain.com",
        # For development only:
        "http://localhost:3000" if settings.ENVIRONMENT == "development" else ""
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=3600,  # Cache preflight requests for 1 hour
)
```


---

## 🟡 PRIORITY 6: Input Sanitization

**File**: `backend/app/utils/text_sanitizer.py`

```python
"""Input sanitization utilities"""
import re
import bleach
from typing import Optional

class TextSanitizer:
    """Sanitize user inputs to prevent XSS and injection attacks"""
    
    # Dangerous patterns that might indicate prompt injection
    PROMPT_INJECTION_PATTERNS = [
        r"ignore\s+(previous|above|all)\s+instructions?",
        r"disregard\s+(previous|above|all)",
        r"system\s+prompt",
        r"you\s+are\s+now",
        r"new\s+instructions?",
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",  # onclick=, onerror=, etc.
    ]
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """
        Remove all HTML tags and dangerous content
        Use for student answers and user-generated content
        """
        if not text:
            return ""
        
        # Remove all HTML tags
        cleaned = bleach.clean(
            text,
            tags=[],  # Allow no tags
            strip=True,
            strip_comments=True
        )
        
        return cleaned.strip()
    
    @staticmethod
    def detect_prompt_injection(text: str) -> tuple[bool, Optional[str]]:
        """
        Detect potential prompt injection attempts
        
        Returns:
            (is_safe, reason)
        """
        if not text:
            return True, None
        
        text_lower = text.lower()
        
        for pattern in TextSanitizer.PROMPT_INJECTION_PATTERNS:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                return False, f"Potential injection detected: {pattern}"
        
        return True, None
    
    @staticmethod
    def sanitize_for_ai(text: str, max_length: int = 5000) -> str:
        """
        Sanitize text before sending to AI
        - Remove HTML
        - Check for injection attempts
        - Truncate if too long
        
        Raises ValueError if injection detected
        """
        # Remove HTML
        cleaned = TextSanitizer.sanitize_html(text)
        
        # Check for injection
        is_safe, reason = TextSanitizer.detect_prompt_injection(cleaned)
        if not is_safe:
            raise ValueError(f"Input rejected: {reason}")
        
        # Truncate if too long
        if len(cleaned) > max_length:
            cleaned = cleaned[:max_length]
        
        return cleaned
    
    @staticmethod
    def validate_category(category: str, allowed: set[str]) -> str:
        """
        Validate category input (whitelist approach)
        
        Args:
            category: User-provided category
            allowed: Set of allowed categories
            
        Returns:
            Validated category
            
        Raises:
            ValueError if invalid
        """
        if category not in allowed:
            raise ValueError(
                f"Invalid category: '{category}'. "
                f"Allowed: {sorted(allowed)}"
            )
        return category

# Apply in exam service:
from app.utils.text_sanitizer import TextSanitizer

def save_answer(...):
    # Sanitize student answer before saving
    sanitized_answer = TextSanitizer.sanitize_for_ai(
        student_answer,
        max_length=10000
    )
    
    # Save sanitized answer
    answer = StudentAnswerRepository.upsert(
        db, 
        test_id=test.id, 
        question_id=question.id,
        student_answer=sanitized_answer  # Use sanitized version
    )
```


---

## 🟡 PRIORITY 7: Missing Database Indexes

**Create migration file**: `alembic revision -m "add_production_indexes"`

```python
"""add_production_indexes

Revision ID: 007_add_production_indexes
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Composite indexes for common query patterns
    op.create_index(
        'idx_tests_user_status_created',
        'tests',
        ['user_id', 'status', 'created_at'],
        postgresql_ops={'created_at': 'DESC'}
    )
    
    op.create_index(
        'idx_answers_test_question',
        'student_test_answers',
        ['test_id', 'question_id']
    )
    
    # Partial index for answered questions only
    op.execute("""
        CREATE INDEX idx_answers_answered 
        ON student_test_answers (test_id, question_id) 
        WHERE student_answer IS NOT NULL
    """)
    
    # Index for question retrieval in order
    op.create_index(
        'idx_questions_test_number',
        'test_questions',
        ['test_id', 'question_number']
    )
    
    # Data integrity constraints
    op.execute("""
        ALTER TABLE tests 
        ADD CONSTRAINT check_dates_order 
        CHECK (started_at IS NULL OR started_at >= created_at)
    """)
    
    op.execute("""
        ALTER TABLE tests 
        ADD CONSTRAINT check_completion_order
        CHECK (completed_at IS NULL OR completed_at >= started_at)
    """)

def downgrade():
    op.drop_index('idx_tests_user_status_created', 'tests')
    op.drop_index('idx_answers_test_question', 'student_test_answers')
    op.execute('DROP INDEX IF EXISTS idx_answers_answered')
    op.drop_index('idx_questions_test_number', 'test_questions')
    op.execute('ALTER TABLE tests DROP CONSTRAINT IF EXISTS check_dates_order')
    op.execute('ALTER TABLE tests DROP CONSTRAINT IF EXISTS check_completion_order')
```

**Run migration**:
```bash
cd backend
alembic upgrade head
```

---

## 🟡 PRIORITY 8: Structured Logging

```bash
pip install structlog
```

**File**: `backend/app/core/logging_config.py`

```python
"""Structured logging configuration"""
import structlog
import logging
import sys

def configure_logging(environment: str = "development"):
    """
    Configure structured logging for the application
    
    Args:
        environment: development, staging, or production
    """
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            # Development: Pretty console output
            # Production: JSON for log aggregation
            structlog.dev.ConsoleRenderer() 
                if environment == "development" 
                else structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO if environment == "production" else logging.DEBUG,
    )
    
    # Set log levels for noisy libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

# Usage in your code:
import structlog

logger = structlog.get_logger()

# Log with context:
logger.info(
    "exam_generated",
    test_id=str(test.id),
    user_id=user_id,
    question_type=request.question_type,
    question_count=len(questions),
    generation_time_ms=duration * 1000,
    retrieval_chunks=len(chunks)
)
```

**Initialize in main.py**:
```python
from app.core.logging_config import configure_logging
from app.core.config import settings

configure_logging(settings.ENVIRONMENT)
```


---

## 🟡 PRIORITY 9: Hallucination Detection

**File**: `backend/app/services/question_generation/hallucination_detector.py`

```python
"""Hallucination detection for AI-generated questions"""
from typing import Tuple
import logging
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

logger = logging.getLogger(__name__)

class HallucinationDetector:
    """Detect if AI-generated questions/answers match the source context"""
    
    def __init__(self):
        # Use same model as retrieval for consistency
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.SIMILARITY_THRESHOLD = 0.7  # 70% similarity required
        logger.info("Hallucination detector initialized")
    
    def verify_answer_from_context(
        self,
        question: str,
        answer: str,
        context: str
    ) -> Tuple[bool, float, str]:
        """
        Verify that the answer can be found in the context
        
        Args:
            question: The generated question
            answer: The correct answer
            context: Retrieved textbook context
            
        Returns:
            (is_valid, confidence_score, reason)
        """
        try:
            # Combine question + answer for better semantic matching
            qa_text = f"{question} {answer}"
            
            # Generate embeddings
            qa_embedding = self.model.encode([qa_text])
            context_embedding = self.model.encode([context])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(qa_embedding, context_embedding)[0][0]
            
            is_valid = similarity >= self.SIMILARITY_THRESHOLD
            
            if is_valid:
                reason = f"Answer verified in context (similarity: {similarity:.3f})"
                logger.debug(f"Verification passed: {reason}")
            else:
                reason = f"Potential hallucination detected (similarity: {similarity:.3f} < {self.SIMILARITY_THRESHOLD})"
                logger.warning(f"Verification failed: {reason}")
            
            return is_valid, float(similarity), reason
            
        except Exception as e:
            logger.error(f"Hallucination detection failed: {e}", exc_info=True)
            # Fail open - allow question if detector fails
            return True, 0.0, f"Detector error: {str(e)}"
    
    def verify_batch(
        self,
        questions: list[dict],
        context: str
    ) -> Tuple[list[dict], list[dict]]:
        """
        Verify multiple questions against context
        
        Args:
            questions: List of question dicts with 'question_text' and 'correct_answer'
            context: Retrieved context
            
        Returns:
            (valid_questions, rejected_questions)
        """
        valid = []
        rejected = []
        
        for q in questions:
            is_valid, score, reason = self.verify_answer_from_context(
                q['question_text'],
                q['correct_answer'],
                context
            )
            
            if is_valid:
                q['verification_score'] = score
                valid.append(q)
            else:
                q['rejection_reason'] = reason
                q['verification_score'] = score
                rejected.append(q)
        
        logger.info(
            f"Verification complete: {len(valid)} valid, "
            f"{len(rejected)} rejected (threshold: {self.SIMILARITY_THRESHOLD})"
        )
        
        return valid, rejected
```

**Integrate in generator** (`backend/app/services/question_generation/generator.py`):

```python
from app.services.question_generation.hallucination_detector import HallucinationDetector

class QuestionGeneratorService:
    def __init__(self, ...):
        # Existing initialization...
        self.hallucination_detector = HallucinationDetector()
    
    def generate_exam(self, db: Session, request: ExamGenerationRequest):
        # ... existing code ...
        
        # AFTER generating questions, BEFORE validation:
        valid_questions, rejected = self.hallucination_detector.verify_batch(
            all_generated_questions,
            context
        )
        
        if rejected:
            logger.warning(f"Rejected {len(rejected)} questions due to hallucination")
            # Log rejected questions for analysis
            for r in rejected:
                logger.warning(
                    f"Rejected question: {r['question_text'][:50]}... "
                    f"Reason: {r['rejection_reason']}"
                )
        
        # Continue with validation on valid_questions only
        valid_validated, errors = self.validator.validate_batch(
            valid_questions,
            request.question_type.value
        )
        
        # ... rest of code ...
```

---

## 🟢 BONUS: Docker Compose for Development

**File**: `docker-compose.yml` (project root)

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: ai_tutor_db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: ai_study_companion
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: ai_tutor_redis
    command: redis-server --appendonly yes --requirepass redis_password_here
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "redis_password_here", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: ai_tutor_backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/ai_study_companion
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=redis_password_here
      - ENVIRONMENT=development
    volumes:
      - ./backend:/app
      - ./chroma_db:/app/chroma_db
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

**File**: `backend/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Start services**:
```bash
docker-compose up -d
docker-compose logs -f backend
```

---

## ✅ VERIFICATION CHECKLIST

After implementing these fixes, verify each one:

### Priority 1: Redis Rate Limiter
```bash
# Test rate limiting
for i in {1..6}; do
  curl -X POST http://localhost:8000/api/v1/exams/generate \
    -H "Authorization: Bearer YOUR_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"categories":["History"],"question_type":"MCQ","question_count":5}'
  echo "\nRequest $i completed"
  sleep 1
done
# Expected: First 5 succeed, 6th returns 429
```

### Priority 2: Database Connection Pool
```python
# Check pool status
from app.db.session import engine
print(f"Pool size: {engine.pool.size()}")
print(f"Connections checked out: {engine.pool.checkedout()}")
print(f"Overflow: {engine.pool.overflow()}")
```

### Priority 3: Health Checks
```bash
# Test health endpoints
curl http://localhost:8000/health
curl http://localhost:8000/health/ready
curl http://localhost:8000/health/live
# All should return 200
```

### Priority 4: Sentry
```python
# Trigger test error
raise Exception("Test Sentry integration")
# Check Sentry dashboard for error
```

### Priority 5: Security Headers
```bash
curl -I http://localhost:8000/health
# Verify headers present:
# - Content-Security-Policy
# - X-Frame-Options: DENY
# - X-Content-Type-Options: nosniff
```

### Priority 6: Input Sanitization
```python
from app.utils.text_sanitizer import TextSanitizer

# Test HTML removal
assert TextSanitizer.sanitize_html("<script>alert('xss')</script>Hello") == "Hello"

# Test injection detection
safe, reason = TextSanitizer.detect_prompt_injection("Ignore all previous instructions")
assert safe == False
```

### Priority 7: Database Indexes
```sql
-- Verify indexes created
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename IN ('tests', 'test_questions', 'student_test_answers')
ORDER BY tablename, indexname;
```

### Priority 9: Hallucination Detection
```python
from app.services.question_generation.hallucination_detector import HallucinationDetector

detector = HallucinationDetector()
is_valid, score, reason = detector.verify_answer_from_context(
    "Who was the first president?",
    "George Washington",
    "George Washington was the first president of the United States..."
)
print(f"Valid: {is_valid}, Score: {score:.3f}, Reason: {reason}")
# Should show high similarity score (>0.7)
```

---

## 📝 INSTALLATION SCRIPT

**File**: `scripts/install_production_fixes.sh`

```bash
#!/bin/bash
set -e

echo "🚀 Installing Production Fixes..."

# Install dependencies
echo "📦 Installing Python packages..."
pip install redis aioredis sentry-sdk[fastapi] structlog bleach sentence-transformers scikit-learn

# Create new files
echo "📄 Creating new modules..."
touch backend/app/core/redis_client.py
touch backend/app/core/logging_config.py
touch backend/app/services/production_rate_limiter.py
touch backend/app/utils/text_sanitizer.py
touch backend/app/services/question_generation/hallucination_detector.py
touch backend/app/api/v1/endpoints/health.py

# Run database migration
echo "🗄️ Running database migrations..."
cd backend
alembic revision -m "add_production_indexes"
# (Manually add migration code from Priority 7)
alembic upgrade head

echo "✅ Installation complete!"
echo "📋 Next steps:"
echo "   1. Copy code from CRITICAL_FIXES_QUICK_START.md"
echo "   2. Update .env with Redis credentials"
echo "   3. Update main.py with middleware"
echo "   4. Test each fix with verification commands"
echo "   5. Deploy to staging environment"
```

---

## 🎯 FINAL NOTES

**Time Estimate**: 2-3 days for implementation + testing

**Team Size**: 1-2 engineers

**Risk Level**: Low (all backwards compatible)

**Rollback Plan**: 
1. Keep old rate limiter code as fallback
2. Database migrations are reversible
3. Middleware can be disabled via feature flags

**Testing Strategy**:
1. Unit tests for each component
2. Integration tests for API endpoints
3. Load test with 100 concurrent users
4. Monitor Sentry for 24 hours before production

**Success Criteria**:
- ✅ All health checks passing
- ✅ Rate limiting works across multiple servers
- ✅ No errors in Sentry for 24 hours
- ✅ Database queries <50ms (P95)
- ✅ Zero hallucinated questions in sample of 100

---

## 📞 SUPPORT

If you encounter issues:

1. **Redis connection failed**: Check REDIS_HOST and REDIS_PASSWORD in .env
2. **Database pool exhausted**: Increase pool_size in session.py
3. **Sentry not capturing**: Verify SENTRY_DSN is correct
4. **Hallucination detector slow**: Use smaller embedding model or cache results
5. **Security headers not appearing**: Check middleware order in main.py

**Get help**: Create GitHub issue with error logs and environment details

---

**Document Version**: 1.0  
**Last Updated**: June 15, 2026  
**Estimated Implementation Time**: 2-3 days  
**Status**: Ready for Implementation

🚀 **START WITH PRIORITY 1** (Redis Rate Limiter) and work your way down! 🚀
