# Evaluation Module Architecture

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     FRONTEND (Phase 7C)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Evaluation  │  │ Performance  │  │   Chapter    │        │
│  │   Display    │  │  Dashboard   │  │  Analytics   │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└───────────────────────────────┬─────────────────────────────────┘
                                │ HTTP/REST API
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API LAYER (Phase 7B)                         │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  FastAPI Endpoints (/api/v1/evaluations)            │      │
│  │  - POST /evaluations                                 │      │
│  │  - GET /evaluations/{id}                            │      │
│  │  - GET /evaluations/user/{user_id}                  │      │
│  │  - GET /evaluations/stats                           │      │
│  │  - DELETE /evaluations/{id}                         │      │
│  └──────────────────────────────────────────────────────┘      │
│                          │                                       │
│                          │ Authentication & Authorization       │
│                          ▼                                       │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│              SERVICE LAYER (Phase 7A - COMPLETE ✅)             │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  EvaluationService                                   │      │
│  │  - create_evaluation()                               │      │
│  │  - get_user_evaluations()                            │      │
│  │  - get_chapter_performance()                         │      │
│  │  - get_user_performance_stats()                      │      │
│  │  - delete_evaluation()                               │      │
│  │                                                       │      │
│  │  ✅ Business Logic                                   │      │
│  │  ✅ Validation                                       │      │
│  │  ✅ Authorization                                    │      │
│  │  ✅ Error Handling                                   │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│           REPOSITORY LAYER (Phase 7A - COMPLETE ✅)             │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  EvaluationRepository                                │      │
│  │  - create()                                          │      │
│  │  - get_by_id()                                       │      │
│  │  - get_by_user()                                     │      │
│  │  - get_by_chapter()                                  │      │
│  │  - get_chapter_statistics()                          │      │
│  │  - get_user_statistics()                             │      │
│  │  - update()                                          │      │
│  │  - delete()                                          │      │
│  │                                                       │      │
│  │  ✅ Data Access                                      │      │
│  │  ✅ Query Optimization                               │      │
│  │  ✅ Aggregations                                     │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│              MODEL LAYER (Phase 7A - COMPLETE ✅)               │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  SQLAlchemy Models                                   │      │
│  │  ┌──────────────┐                                    │      │
│  │  │  Evaluation  │                                    │      │
│  │  │  - id (UUID) │                                    │      │
│  │  │  - user_id   │◄──────────┐                       │      │
│  │  │  - test_id   │◄────┐     │                       │      │
│  │  │  - question  │     │     │                       │      │
│  │  │  - answers   │     │     │                       │      │
│  │  │  - marks     │     │     │                       │      │
│  │  │  - feedback  │     │     │                       │      │
│  │  └──────────────┘     │     │                       │      │
│  │                        │     │                       │      │
│  │  ┌──────────────┐     │     │                       │      │
│  │  │     Test     │─────┘     │                       │      │
│  │  └──────────────┘           │                       │      │
│  │  ┌──────────────┐           │                       │      │
│  │  │     User     │───────────┘                       │      │
│  │  └──────────────┘                                    │      │
│  │  ┌──────────────┐                                    │      │
│  │  │TestQuestion  │                                    │      │
│  │  └──────────────┘                                    │      │
│  │                                                       │      │
│  │  ✅ Relationships                                    │      │
│  │  ✅ Constraints                                      │      │
│  │  ✅ Indexes                                          │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATABASE (PostgreSQL)                         │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  Tables                                              │      │
│  │  - evaluations         ✅ NEW                        │      │
│  │  - users              (existing)                     │      │
│  │  - tests              (existing)                     │      │
│  │  - test_questions     (existing)                     │      │
│  │                                                       │      │
│  │  Foreign Keys                                        │      │
│  │  - user_id → users.id (CASCADE DELETE)              │      │
│  │  - test_id → tests.id (SET NULL)                    │      │
│  │  - question_id → test_questions.id (SET NULL)       │      │
│  │                                                       │      │
│  │  Indexes                                             │      │
│  │  - Primary: id                                       │      │
│  │  - Foreign Keys: user_id, test_id, question_id      │      │
│  │  - Filters: chapter_name, created_at                │      │
│  │  - Composite: (user_id, chapter_name)               │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

### Create Evaluation Flow

```
1. API Endpoint (Phase 7B)
   POST /api/v1/evaluations
   │
   ├─► Authentication Check
   ├─► Request Validation (Pydantic)
   │
   ▼
2. Service Layer ✅
   EvaluationService.create_evaluation()
   │
   ├─► Business Logic Validation
   │   - Marks validation
   │   - User authorization
   │
   ▼
3. Repository Layer ✅
   EvaluationRepository.create()
   │
   ├─► SQL Query Generation
   ├─► Transaction Management
   │
   ▼
4. Model Layer ✅
   Evaluation model
   │
   ├─► SQLAlchemy ORM
   ├─► Database Constraints
   │
   ▼
5. Database
   INSERT INTO evaluations
   │
   └─► Returns created record
```

### Get User Performance Flow

```
1. API Endpoint (Phase 7B)
   GET /api/v1/evaluations/stats/user/{user_id}
   │
   ├─► Authentication Check
   ├─► Authorization (own data only)
   │
   ▼
2. Service Layer ✅
   EvaluationService.get_user_performance_stats()
   │
   ├─► Orchestrate multiple calls
   │   - Get overall statistics
   │   - Get recent evaluations
   │
   ▼
3. Repository Layer ✅
   EvaluationRepository.get_user_statistics()
   EvaluationRepository.get_recent_by_user()
   │
   ├─► Aggregation queries
   │   - SUM(marks_awarded)
   │   - COUNT(id)
   │   - AVG percentage calculation
   │
   ▼
4. Model Layer ✅
   Evaluation model
   │
   ├─► SQLAlchemy ORM
   │
   ▼
5. Database
   SELECT with aggregations
   │
   └─► Returns statistics + recent evaluations
```

---

## 📊 Database Schema Visualization

```
┌─────────────────────────────────────────────────────┐
│                    EVALUATIONS                      │
├─────────────────────────────────────────────────────┤
│ 🔑 id                  UUID (PK)                    │
│ 🔗 user_id             INTEGER (FK → users.id)      │
│ 🔗 test_id             UUID (FK → tests.id)         │
│ 🔗 question_id         UUID (FK → test_questions.id)│
│ 📝 question            TEXT                         │
│ 📝 student_answer      TEXT                         │
│ 📝 model_answer        TEXT                         │
│ 📊 marks_awarded       INTEGER                      │
│ 📊 total_marks         INTEGER                      │
│ 💬 feedback            TEXT                         │
│ 📋 strengths           JSON[]                       │
│ 📋 improvements        JSON[]                       │
│ 🏷️  chapter_name       VARCHAR(255)                 │
│ 🕐 created_at          TIMESTAMP WITH TZ            │
└─────────────────────────────────────────────────────┘
          │         │          │
          │         │          │
          ▼         ▼          ▼
    ┌─────────┐ ┌────────┐ ┌──────────────┐
    │  USERS  │ │ TESTS  │ │TEST_QUESTIONS│
    └─────────┘ └────────┘ └──────────────┘

CASCADE Behavior:
- User deleted → Evaluations CASCADE DELETED
- Test deleted → test_id SET NULL (preserve history)
- Question deleted → question_id SET NULL (preserve history)

Constraints:
✅ marks_awarded >= 0
✅ total_marks > 0
✅ marks_awarded <= total_marks

Indexes:
✅ id (PRIMARY)
✅ user_id
✅ test_id
✅ question_id
✅ chapter_name
✅ created_at
✅ (user_id, chapter_name) COMPOSITE
```

---

## 🎯 Layer Responsibilities

### ✅ Model Layer (COMPLETE)
**Responsibility**: Data structure and relationships
- Define database schema
- Manage relationships
- Define constraints
- ORM mapping

**Does NOT**:
- Business logic
- HTTP handling
- User authentication

---

### ✅ Repository Layer (COMPLETE)
**Responsibility**: Data access
- CRUD operations
- Database queries
- Aggregations
- Query optimization

**Does NOT**:
- Business logic validation
- HTTP exceptions
- User authorization

---

### ✅ Service Layer (COMPLETE)
**Responsibility**: Business logic
- Validation rules
- Authorization checks
- Orchestration
- Error handling

**Does NOT**:
- Direct database access
- HTTP request handling
- Response formatting

---

### 🔄 API Layer (Phase 7B - Next)
**Responsibility**: HTTP interface
- Request handling
- Response formatting
- Authentication
- API documentation

**Does NOT**:
- Business logic
- Direct database access
- Complex calculations

---

## 🔐 Security Architecture

```
┌──────────────────────────────────────────┐
│          Request from Frontend           │
└─────────────────┬────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────┐
│    JWT Authentication Middleware         │
│    ✅ Token validation                   │
│    ✅ User extraction                    │
└─────────────────┬────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────┐
│         API Endpoint Handler             │
│    ✅ Input validation (Pydantic)        │
│    ✅ Rate limiting                      │
└─────────────────┬────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────┐
│          Service Layer ✅                │
│    ✅ Authorization checks               │
│    ✅ Business logic validation          │
│    ✅ User can only access own data      │
└─────────────────┬────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────┐
│        Repository Layer ✅               │
│    ✅ Parameterized queries              │
│    ✅ SQL injection prevention           │
└─────────────────┬────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────┐
│          Database ✅                     │
│    ✅ Constraints enforcement            │
│    ✅ Foreign key validation             │
│    ✅ Check constraints                  │
└──────────────────────────────────────────┘
```

---

## 📈 Performance Optimization

### Indexing Strategy ✅

1. **Primary Key Index**
   - Column: `id`
   - Type: UUID
   - Usage: Direct lookups

2. **Foreign Key Indexes**
   - Columns: `user_id`, `test_id`, `question_id`
   - Usage: JOIN operations, filtering

3. **Filter Indexes**
   - Columns: `chapter_name`, `created_at`
   - Usage: WHERE clauses, time-based queries

4. **Composite Index**
   - Columns: `(user_id, chapter_name)`
   - Usage: Chapter performance queries
   - High impact: Most common query pattern

### Query Optimization ✅

1. **Pagination**
   - LIMIT and OFFSET support
   - Prevents large result sets

2. **Selective Loading**
   - Summary schema for list views
   - Full schema only when needed

3. **Aggregation at Database**
   - COUNT, SUM, AVG in SQL
   - Reduces data transfer

4. **Eager Loading**
   - Relationships loaded efficiently
   - Prevents N+1 queries

---

## 🧪 Testing Strategy

### Unit Tests (Recommended)

```python
# Test Model
def test_evaluation_percentage():
    eval = Evaluation(marks_awarded=8, total_marks=10)
    assert eval.percentage == 80.0

# Test Repository
def test_create_evaluation():
    repo = EvaluationRepository()
    eval = repo.create(db, evaluation_data)
    assert eval.id is not None

# Test Service
def test_create_evaluation_validation():
    service = EvaluationService(db)
    with pytest.raises(HTTPException):
        service.create_evaluation(invalid_data)
```

### Integration Tests

```python
# Test API Endpoint
def test_create_evaluation_endpoint():
    response = client.post(
        "/api/v1/evaluations",
        json=evaluation_data,
        headers=auth_headers
    )
    assert response.status_code == 201
```

---

## 📦 Dependencies

### Installed (Already in Project)
- ✅ SQLAlchemy - ORM
- ✅ Alembic - Migrations
- ✅ Pydantic - Validation
- ✅ FastAPI - Framework
- ✅ PostgreSQL - Database

### No New Dependencies Required
All implementation uses existing project dependencies.

---

## 🚀 Deployment Checklist

### Before Deployment
- [ ] Apply migration: `alembic upgrade head`
- [ ] Verify migration: `alembic current`
- [ ] Test database connection
- [ ] Run unit tests
- [ ] Run integration tests
- [ ] Review indexes: `EXPLAIN ANALYZE`
- [ ] Check constraint enforcement

### Production Considerations
- Backup database before migration
- Test rollback procedure
- Monitor index usage
- Set up error logging
- Configure rate limiting
- Enable query performance monitoring

---

## 📚 Related Documentation

- **Implementation Guide**: `PHASE_7A_EVALUATION_DATABASE_LAYER.md`
- **Migration Guide**: `APPLY_EVALUATION_MIGRATION.md`
- **Summary**: `EVALUATION_MODULE_SUMMARY.md`
- **Architecture**: This document

---

**Status**: ✅ Phase 7A Architecture Complete
**Next**: Phase 7B - API Layer Implementation
