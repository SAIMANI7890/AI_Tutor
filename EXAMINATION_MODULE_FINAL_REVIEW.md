# Phase 6F — Examination Module Architecture Review

> **Produced:** 2026-06-15  
> **Scope:** Complete AI-Powered Examination Module (Phases 6A–6E)  
> **Stack:** FastAPI · SQLAlchemy 2.0 · PostgreSQL · ChromaDB · Gemini · Next.js 15

---

## Architecture Diagram

```mermaid
flowchart TB
    subgraph Frontend ["Frontend — Next.js 15"]
        CFG["/examination — Config Form"]
        TEST["/examination/test/[testId] — Test Taking"]
        HIST["/examination/history — History"]
        SVC["exam.service.ts"]
        HOOKS["useExam · useSubmitExam · useExamHistory"]
        CFG --> SVC
        TEST --> HOOKS --> SVC
        HIST --> HOOKS
    end

    subgraph API ["API Layer — FastAPI"]
        R1["POST /exams/generate"]
        R2["GET  /exams/history"]
        R3["GET  /exams/{id}"]
        R4["GET  /exams/{id}/questions"]
        R5["POST /exams/{id}/answer"]
        R6["GET  /exams/{id}/answers"]
        R7["POST /exams/{id}/submit"]
    end

    subgraph Services ["Service Layer"]
        ES["ExamService"]
        QG["QuestionGeneratorService"]
        RL["RateLimiter (5/hr)"]
    end

    subgraph AI ["AI Layer"]
        PROM["prompts_v3.py — V3 Prompts\n(Bloom's · Anti-hallucination · Difficulty)"]
        GEMINI["Gemini 1.5 Flash"]
        VAL["QuestionValidator · QualityControl"]
    end

    subgraph RAG ["RAG Layer"]
        RET["RetrieverService"]
        CHROMA["ChromaDB — Textbook Vectors"]
    end

    subgraph DB ["PostgreSQL"]
        T["tests"]
        Q["test_questions"]
        A["student_test_answers"]
        T --> Q
        T --> A
        Q --> A
    end

    SVC -- "JWT Bearer" --> API
    API --> ES
    ES --> QG
    ES --> RL
    QG --> PROM --> GEMINI
    QG --> RET --> CHROMA
    GEMINI --> VAL
    ES --> DB
```

---

## 1. Database Design — Review

### Schema

| Table | Primary Key | Key Columns | Indexes |
|-------|-------------|-------------|---------|
| `tests` | `UUID` | `user_id`, `question_type`, `selected_categories (JSON)`, `status`, `question_count` | `user_id`, `status`, `created_at` |
| `test_questions` | `UUID` | `test_id`, `question_number`, `question_type`, `question_text`, `options_json`, `correct_answer`, `model_answer`, `category` | `test_id`, `category` |
| `student_test_answers` | `UUID` | `test_id`, `question_id`, `student_answer` | `test_id`, `question_id` + UNIQUE constraint |

### Strengths
- ✅ UUID primary keys — globally unique, safe for distributed deployments
- ✅ Cascade deletes on all FK relationships — no orphaned records
- ✅ `UniqueConstraint('test_id', 'question_id')` on answers — enables safe atomic upsert
- ✅ `selectin` lazy loading on test relationships — avoids N+1 queries
- ✅ Status enum (`GENERATED → IN_PROGRESS → SUBMITTED → EVALUATED`) — clean lifecycle

### Recommendations

> [!TIP]
> **Add a `difficulty` column** to `test_questions` — v3 prompts already generate this field but it is discarded. Storing it enables future difficulty analytics and adaptive testing.

```sql
-- Future migration
ALTER TABLE test_questions ADD COLUMN difficulty VARCHAR(10);  -- Easy / Medium / Hard
ALTER TABLE test_questions ADD COLUMN blooms_level VARCHAR(20); -- L1_Remember ... L5_Evaluate
```

> [!NOTE]
> Consider adding **composite index** on `(user_id, status)` on the `tests` table for the common filter pattern used by the history endpoint.

```sql
CREATE INDEX idx_tests_user_status ON tests(user_id, status);
```

---

## 2. API Design — Review

### Endpoints

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| `POST` | `/exams/generate` | JWT | Generate new exam via RAG + Gemini |
| `GET` | `/exams/` | JWT | List user's exams (compact) |
| `GET` | `/exams/history` | JWT | Exam history (semantic alias) |
| `GET` | `/exams/{id}` | JWT + ownership | Full exam + questions |
| `GET` | `/exams/{id}/questions` | JWT + ownership | Questions only (auto-starts exam) |
| `POST` | `/exams/{id}/answer` | JWT + ownership | Save/upsert one answer |
| `GET` | `/exams/{id}/answers` | JWT + ownership | Retrieve saved answers |
| `POST` | `/exams/{id}/submit` | JWT + ownership | Submit exam |

### Strengths
- ✅ Correct_answer / model_answer **never exposed** to student API responses
- ✅ Ownership validation on every exam-scoped endpoint (403 if not owner)
- ✅ Status-transition guards (cannot answer/submit already-submitted exams)
- ✅ Idempotent answer upsert — safe for autosave
- ✅ Rate limiter on generate (5 exams/hour/user)

### Recommendations

> [!IMPORTANT]
> **Add pagination** to list/history endpoints before production. Currently returns all exams — will degrade as users accumulate hundreds of tests.

```python
# Recommended query signature
GET /exams/?page=1&page_size=20&status=SUBMITTED
```

> [!TIP]
> Consider a `DELETE /exams/{id}` endpoint so students can remove unwanted generated tests (status=GENERATED only).

---

## 3. RAG Quality — Review

### Pipeline

1. Category-filtered ChromaDB query (`where={"category": category}`)
2. Top-10 chunks per category retrieved
3. Similarity scored via `1 / (1 + distance)`
4. Context formatted and passed to Gemini V3 prompt

### V3 Prompt Quality Framework
- **5-Layer Hallucination Prevention**: Source fidelity, verification requirement, fact-checking, prohibited patterns, self-verification
- **Bloom's Taxonomy**: L1 (Remember) → L5 (Evaluate) systematically enforced
- **Difficulty Distribution**: 30% Easy / 50% Medium / 20% Hard target
- **Few-Shot Examples**: All four question types have 3 annotated examples

### Recommendations

> [!TIP]
> **Store difficulty and blooms_level** from generated questions (v3 prompts return these — currently discarded). This enables future analytics dashboards.

> [!NOTE]
> Consider increasing `top_k_per_category` from 10 → 15 for LONG_ANSWER questions which benefit from broader context.

---

## 4. Security Analysis

### Current Protections
- ✅ JWT Bearer token required on all endpoints
- ✅ Ownership verification (user_id match) before any data access
- ✅ Correct answers never sent to the frontend
- ✅ Rate limiting on compute-intensive generation (5/hr)
- ✅ Input validation via Pydantic with enum and range constraints

### Recommendations

> [!WARNING]
> **Add SQL injection protection audit** — SQLAlchemy ORM usage prevents direct injection, but verify no raw SQL in repositories.

> [!CAUTION]
> **Gemini API key security**: Ensure `GEMINI_API_KEY` is never logged. Add a startup check that masks key in logs.

```python
# In settings / startup
logger.info(f"Gemini API key: {'*' * len(key[:-4]) + key[-4:]}")
```

> [!WARNING]
> **CORS configuration**: `allow_origins=settings.ALLOWED_ORIGINS` should be an explicit list in production, never `["*"]`.

---

## 5. Performance Optimizations

### Current Bottlenecks
1. **Exam generation** (~15-30s): Gemini API latency dominates — unavoidable
2. **Context retrieval**: 10 × num_categories ChromaDB queries per generation

### Recommendations

| Optimization | Impact | Effort |
|---|---|---|
| Add Redis caching for RAG context (TTL=1hr per category) | -70% RAG latency on repeat requests | Medium |
| Run generation in a background task (Celery/ARQ) + WebSocket progress | Better UX, non-blocking | High |
| Add `question_count` index to avoid table scans on large datasets | Marginal | Low |
| Composite index `(user_id, status)` on tests | Fast history queries | Low |
| Connection pooling configuration (SQLAlchemy pool_size=10) | Concurrency | Low |

---

## 6. Scalability Analysis

### Current Architecture
- Single FastAPI process (Uvicorn)
- Single PostgreSQL instance
- Local ChromaDB file store
- Synchronous Gemini calls block request threads

### Scale-Up Path

```mermaid
flowchart LR
    LB["Load Balancer"] --> A1["FastAPI Worker 1"]
    LB --> A2["FastAPI Worker 2"]
    LB --> A3["FastAPI Worker N"]
    A1 & A2 & A3 --> PG[("PostgreSQL\n(Primary + Replica)")]
    A1 & A2 & A3 --> REDIS[("Redis\nCache + Queue")]
    A1 & A2 & A3 --> CHROMA[("ChromaDB\nRemote Server")]
    REDIS --> W1["Celery Worker 1\n(Exam Generation)"]
    REDIS --> W2["Celery Worker 2\n(Exam Generation)"]
```

### Immediate Wins (before scale-out)
1. `uvicorn --workers 4` — simple multi-process
2. SQLAlchemy async session (asyncpg) — non-blocking DB
3. Move ChromaDB to remote server (Chroma Cloud or self-hosted)

---

## 7. Maintainability

### Folder Structure (Actual vs. Recommended)

```
backend/app/
├── api/v1/endpoints/
│   ├── exams.py              ← 8 endpoints, well-organised ✅
│   ├── exam_schemas.py       ← should move to app/schemas/examination.py
│   └── exam_dependencies.py  ← good pattern ✅
├── models/                   ← clean separation ✅
├── repositories/             ← clean repository pattern ✅
├── services/
│   ├── exam_service.py       ← business logic ✅
│   └── question_generation/  ← sub-package ✅
├── prompts/                  ← NEW: canonical prompt module ✅
└── rag/                      ← RAG pipeline ✅
```

> [!NOTE]
> Move `exam_schemas.py` from `api/v1/endpoints/` to `app/schemas/examination.py` for consistency with other schemas.

---

## 8. Monitoring & Logging Strategy

### Current Logging
- `logging.getLogger(__name__)` in all services ✅
- Request-level logs: user_id, question_type, count ✅
- Generation success/failure logs ✅

### Recommended Additions

```python
# Structured logging with context (add to exam_service.py)
import structlog
log = structlog.get_logger()

log.info(
    "exam_generated",
    user_id=user_id,
    test_id=str(test.id),
    question_type=question_type,
    question_count=question_count,
    generation_time_ms=elapsed_ms,
)
```

### Metrics to Track
| Metric | Why |
|--------|-----|
| `exam_generation_duration_seconds` | SLA monitoring |
| `exam_generation_error_rate` | Quality alert |
| `questions_answered_per_exam` | Engagement |
| `submission_rate` | Completion funnel |
| `rag_retrieval_chunk_count` | RAG health |

---

## 9. UX Review

### Current UX Flow

```
/examination (config) → Generate → /test/{id} (take test) → Submit → Success Screen
                                                                         ↓
                                       /examination/history (view all tests)
```

### Strengths
- ✅ Autosave with debounce (1000ms) + save indicator
- ✅ Page-refresh answer recovery (GET /answers on mount)
- ✅ Submission confirmation dialog with unanswered count warning
- ✅ Mobile-responsive design (hamburger nav on mobile)
- ✅ Question palette with answered/unanswered visual states
- ✅ Before-unload warning if save is pending

### Recommendations
1. **Timer**: Add optional countdown timer for exam simulation
2. **Skipped questions indicator**: Highlight which questions have no answer in the navigator
3. **Offline support**: Cache answers in localStorage as backup to autosave
4. **Loading progress**: Show generation progress (step 1/3: retrieving... step 2/3: generating...)

---

## 10. Future Evaluation Integration

The database schema is specifically designed to support a future **AI Evaluation Phase (Phase 7)**:

```
Current:  GENERATED → IN_PROGRESS → SUBMITTED
Future:   GENERATED → IN_PROGRESS → SUBMITTED → EVALUATED
```

### Recommended Phase 7 Schema Extensions

```python
# Additions to StudentTestAnswer for evaluation
marks_obtained   = Column(Float, nullable=True)        # Score for this answer
ai_feedback      = Column(Text, nullable=True)          # Gemini evaluation feedback
evaluation_status = Column(Enum("PENDING", "DONE"))    # Per-answer status
evaluated_at     = Column(DateTime, nullable=True)

# Additions to Test for overall score
total_marks      = Column(Integer, nullable=True)       # Max possible
obtained_marks   = Column(Float, nullable=True)         # Student score
pass_percentage  = Column(Float, nullable=True)         # Configured pass mark
```

### Evaluation API (Phase 7 Preview)

```
POST /exams/{test_id}/evaluate    → Trigger AI evaluation
GET  /exams/{test_id}/results     → Get detailed scores + feedback per question
GET  /exams/{test_id}/report      → Performance report (by category, Bloom's level)
```

---

## Deployment Recommendations

### Environment Variables

```env
# Required
DATABASE_URL=postgresql://user:pass@host:5432/dbname
GEMINI_API_KEY=...
SECRET_KEY=...  # JWT signing key — must be long random string

# Recommended for production
CHROMA_DB_PATH=/data/chroma_db  # Mount persistent volume
ALLOWED_ORIGINS=https://yourdomain.com
RATE_LIMIT_EXAMS_PER_HOUR=5
LOG_LEVEL=INFO

# Optional
REDIS_URL=redis://localhost:6379  # For future caching/queues
```

### Docker Deployment

```dockerfile
# Dockerfile (backend)
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

### Health Check

```bash
# Verify deployment
curl http://localhost:8000/health
# → {"success": true, "message": "Service is healthy", "data": {"status": "ok"}}

curl http://localhost:8000/api/v1/docs
# → FastAPI Swagger UI
```

---

## Summary Table

| Area | Score | Key Finding |
|------|-------|-------------|
| Database Design | ⭐⭐⭐⭐⭐ | Production-ready schema with proper FKs, cascades, and indexes |
| API Design | ⭐⭐⭐⭐☆ | Clean REST + ownership validation; needs pagination |
| RAG Quality | ⭐⭐⭐⭐⭐ | V3 prompts now active with full anti-hallucination + Bloom's |
| Prompt Quality | ⭐⭐⭐⭐⭐ | V3 system is best-in-class for educational assessment |
| Security | ⭐⭐⭐⭐☆ | JWT + ownership + rate limiting; review CORS in production |
| Scalability | ⭐⭐⭐☆☆ | Good foundation; needs async + caching for scale |
| Maintainability | ⭐⭐⭐⭐⭐ | Clean layered architecture: router → service → repo → model |
| Performance | ⭐⭐⭐☆☆ | Generation latency inherent; caching + async are next steps |
| UX | ⭐⭐⭐⭐☆ | Excellent autosave + recovery; add timer + progress for v2 |
| Future Evaluation | ⭐⭐⭐⭐⭐ | Schema pre-designed for Phase 7; clean migration path |
