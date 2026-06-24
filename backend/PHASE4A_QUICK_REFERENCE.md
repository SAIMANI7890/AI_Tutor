# Phase 4A: Quick Reference Card

## 📊 Database Schema

### Tests Table
```sql
tests (
    id UUID PRIMARY KEY,
    user_id INTEGER → users.id,
    subject VARCHAR(255),
    question_type ENUM(MCQ, FILL_BLANKS, SHORT_ANSWER, LONG_ANSWER),
    selected_categories JSON,
    question_count INTEGER CHECK(1-10),
    status ENUM(GENERATED, IN_PROGRESS, SUBMITTED, EVALUATED),
    created_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
)
```

### Test Questions Table
```sql
test_questions (
    id UUID PRIMARY KEY,
    test_id UUID → tests.id,
    question_number INTEGER,
    question_type ENUM,
    question_text TEXT,
    options_json JSON,
    correct_answer TEXT,
    model_answer TEXT,
    source_document VARCHAR(255),
    source_page INTEGER,
    category VARCHAR(255),
    created_at TIMESTAMP,
    UNIQUE(test_id, question_number)
)
```

### Student Test Answers Table
```sql
student_test_answers (
    id UUID PRIMARY KEY,
    test_id UUID → tests.id,
    question_id UUID → test_questions.id,
    student_answer TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    UNIQUE(test_id, question_id)
)
```

## 🔧 Repository Methods

### TestRepository
```python
TestRepository.create(db, test)                              # Create test
TestRepository.get_by_id(db, test_id)                        # Get by UUID
TestRepository.get_by_user(db, user_id)                      # Get user tests
TestRepository.get_by_user_and_status(db, user_id, status)   # Filter by status
TestRepository.update(db, test)                              # Update test
TestRepository.delete(db, test)                              # Delete test
TestRepository.count_by_user(db, user_id)                    # Count tests
```

### TestQuestionRepository
```python
TestQuestionRepository.create(db, question)                  # Create question
TestQuestionRepository.create_bulk(db, questions)            # Bulk create ⚡
TestQuestionRepository.get_by_id(db, question_id)            # Get by UUID
TestQuestionRepository.get_by_test(db, test_id)              # Get test questions
TestQuestionRepository.get_by_test_and_number(db, test_id, n)# Get specific Q
TestQuestionRepository.update(db, question)                  # Update question
TestQuestionRepository.delete(db, question)                  # Delete question
TestQuestionRepository.count_by_test(db, test_id)            # Count questions
```

### StudentAnswerRepository
```python
StudentAnswerRepository.create(db, answer)                   # Create answer
StudentAnswerRepository.get_by_id(db, answer_id)             # Get by UUID
StudentAnswerRepository.get_by_test(db, test_id)             # Get test answers
StudentAnswerRepository.get_by_test_and_question(db, t, q)   # Get specific answer
StudentAnswerRepository.update(db, answer)                   # Update answer
StudentAnswerRepository.upsert(db, test_id, q_id, answer)    # Create or update ⚡
StudentAnswerRepository.delete(db, answer)                   # Delete answer
StudentAnswerRepository.count_answered(db, test_id)          # Count answered
StudentAnswerRepository.delete_by_test(db, test_id)          # Delete all (reset)
```

## 📦 Pydantic Schemas

### Test Schemas
```python
TestCreate(subject, question_type, selected_categories, question_count)
TestUpdate(status, started_at?, completed_at?)
TestRead  # Full test data
TestSummary  # Compact without questions
```

### Question Schemas
```python
TestQuestionCreate(test_id, question_number, question_type, question_text, 
                   options_json?, correct_answer, model_answer?, 
                   source_document?, source_page?, category)
TestQuestionUpdate(question_text?, options_json?, correct_answer?, model_answer?)
TestQuestionRead  # Full question data
TestQuestionForStudent  # Without correct_answer (for students)
```

### Answer Schemas
```python
StudentAnswerCreate(test_id, question_id, student_answer?)
StudentAnswerUpdate(student_answer?)
StudentAnswerRead  # Full answer data
StudentAnswerWithQuestion  # With question details
```

## 🎯 Common Workflows

### Create Test with Questions
```python
# 1. Create test
test = Test(user_id=user_id, subject="Social Studies", 
           question_type=QuestionType.MCQ, 
           selected_categories=["History"], question_count=5)
test = TestRepository.create(db, test)

# 2. Add questions (bulk)
questions = [TestQuestion(...) for _ in range(5)]
TestQuestionRepository.create_bulk(db, questions)
```

### Student Takes Test
```python
# 1. Start test
test = TestRepository.get_by_id(db, test_id)
test.status = TestStatus.IN_PROGRESS
test.started_at = datetime.utcnow()
TestRepository.update(db, test)

# 2. Save answers (upsert for idempotency)
StudentAnswerRepository.upsert(db, test_id, question_id, answer)

# 3. Submit test
test.status = TestStatus.SUBMITTED
test.completed_at = datetime.utcnow()
TestRepository.update(db, test)
```

### Check Progress
```python
total = test.question_count
answered = StudentAnswerRepository.count_answered(db, test_id)
progress = (answered / total) * 100
```

## 🔐 Data Integrity

### Cascade Deletes
- Delete User → Deletes all Tests
- Delete Test → Deletes all Questions + Answers
- Delete Question → Deletes all Student Answers

### Unique Constraints
- (test_id, question_number) - No duplicate question numbers
- (test_id, question_id) - One answer per question per test

### Check Constraints
- question_count: 1 ≤ count ≤ 10
- question_number: number > 0

## 📈 Performance

### Indexed Fields
- tests: id, user_id, status, question_type, created_at
- test_questions: id, test_id, category
- student_test_answers: id, test_id, question_id

### Optimization Tips
✅ Use `create_bulk()` for multiple questions
✅ Use `upsert()` for idempotent answer saves
✅ Use `count_by_test()` before loading
✅ Relationships use `selectin` loading strategy

## 🚀 Test Results

```
✅ 26 passed
⏭️  2 skipped (SQLite-specific)
📝 Total: 28 tests
⏱️  Runtime: 0.61s
```

### Database Verification
```
✅ 3 tables created
✅ 2 enums created
✅ 16 indexes created
✅ 4 foreign keys created
✅ 5 constraints created
```

## 📚 Import Statements

```python
# Models
from app.models.test import Test
from app.models.test_question import TestQuestion
from app.models.student_test_answer import StudentTestAnswer
from app.models.enums import QuestionType, TestStatus

# Repositories
from app.repositories.test_repository import TestRepository
from app.repositories.question_repository import TestQuestionRepository
from app.repositories.answer_repository import StudentAnswerRepository

# Schemas
from app.schemas.test import TestCreate, TestUpdate, TestRead
from app.schemas.question import TestQuestionCreate, TestQuestionRead
from app.schemas.answer import StudentAnswerCreate, StudentAnswerRead
```

## 🔮 Future Extensions (Phase 5)

### Add to test_questions table:
```python
marks = Column(Integer)  # Per-question marks
difficulty = Column(String)  # Easy/Medium/Hard
bloom_taxonomy = Column(String)  # Remember/Understand/Apply/...
```

### Add to student_test_answers table:
```python
marks_obtained = Column(Integer)
feedback = Column(Text)  # AI feedback
evaluation_status = Column(Enum)  # PENDING/EVALUATED
evaluated_at = Column(DateTime)
evaluated_by = Column(String)  # AI/Teacher
```

### Schema fully supports future evaluation without redesign! ✨

## 📖 Documentation

- **Complete Guide**: `PHASE4A_COMPLETE.md`
- **Usage Examples**: `PHASE4A_USAGE_GUIDE.md`
- **This Reference**: `PHASE4A_QUICK_REFERENCE.md`
- **Verification Script**: `verify_phase4a.py`
- **Tests**: `tests/examination/`

---
**Phase 4A Status**: ✅ COMPLETE AND PRODUCTION READY
