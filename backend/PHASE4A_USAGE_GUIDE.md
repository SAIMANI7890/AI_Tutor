# Phase 4A: Examination Module - Developer Usage Guide

This guide shows how to use the examination database foundation in your code.

## Table of Contents
1. [Quick Start](#quick-start)
2. [Creating Tests](#creating-tests)
3. [Managing Questions](#managing-questions)
4. [Handling Student Answers](#handling-student-answers)
5. [Common Patterns](#common-patterns)

## Quick Start

### Import Required Components

```python
from sqlalchemy.orm import Session
from app.models.test import Test
from app.models.test_question import TestQuestion
from app.models.student_test_answer import StudentTestAnswer
from app.models.enums import QuestionType, TestStatus
from app.repositories.test_repository import TestRepository
from app.repositories.question_repository import TestQuestionRepository
from app.repositories.answer_repository import StudentAnswerRepository
from app.schemas.test import TestCreate, TestRead
from app.schemas.question import TestQuestionCreate
from app.schemas.answer import StudentAnswerCreate
```

## Creating Tests

### 1. Create a New Test

```python
def create_examination(db: Session, user_id: int, test_data: TestCreate) -> Test:
    """
    Create a new examination for a user
    """
    # Create Test model instance
    new_test = Test(
        user_id=user_id,
        subject=test_data.subject,
        question_type=test_data.question_type,
        selected_categories=test_data.selected_categories,
        question_count=test_data.question_count,
        status=TestStatus.GENERATED  # Initial status
    )
    
    # Save to database
    test = TestRepository.create(db, new_test)
    return test
```

### 2. Get User's Tests

```python
def get_user_tests(db: Session, user_id: int) -> list[Test]:
    """
    Get all tests for a user (newest first)
    """
    return TestRepository.get_by_user(db, user_id)
```

### 3. Get Tests by Status

```python
def get_in_progress_tests(db: Session, user_id: int) -> list[Test]:
    """
    Get tests that are currently in progress
    """
    return TestRepository.get_by_user_and_status(
        db, user_id, TestStatus.IN_PROGRESS
    )
```

### 4. Update Test Status

```python
from datetime import datetime

def start_test(db: Session, test_id: UUID) -> Test:
    """
    Mark test as started
    """
    test = TestRepository.get_by_id(db, test_id)
    if not test:
        raise ValueError("Test not found")
    
    test.status = TestStatus.IN_PROGRESS
    test.started_at = datetime.utcnow()
    
    return TestRepository.update(db, test)

def submit_test(db: Session, test_id: UUID) -> Test:
    """
    Mark test as submitted
    """
    test = TestRepository.get_by_id(db, test_id)
    if not test:
        raise ValueError("Test not found")
    
    test.status = TestStatus.SUBMITTED
    test.completed_at = datetime.utcnow()
    
    return TestRepository.update(db, test)
```

## Managing Questions

### 1. Create Questions for a Test (Bulk)

```python
def generate_questions(db: Session, test_id: UUID, questions_data: list) -> list[TestQuestion]:
    """
    Generate multiple questions for a test
    """
    questions = []
    
    for i, q_data in enumerate(questions_data, start=1):
        question = TestQuestion(
            test_id=test_id,
            question_number=i,
            question_type=q_data["question_type"],
            question_text=q_data["question_text"],
            options_json=q_data.get("options_json"),  # For MCQ
            correct_answer=q_data["correct_answer"],
            model_answer=q_data.get("model_answer"),
            source_document=q_data.get("source_document"),
            source_page=q_data.get("source_page"),
            category=q_data["category"]
        )
        questions.append(question)
    
    # Bulk create for efficiency
    return TestQuestionRepository.create_bulk(db, questions)
```

### 2. Get Questions for a Test

```python
def get_test_questions(db: Session, test_id: UUID) -> list[TestQuestion]:
    """
    Get all questions for a test (ordered by question_number)
    """
    return TestQuestionRepository.get_by_test(db, test_id)
```

### 3. Get Questions for Students (Hide Answers)

```python
from app.schemas.question import TestQuestionForStudent

def get_student_questions(db: Session, test_id: UUID) -> list[TestQuestionForStudent]:
    """
    Get questions without showing correct answers
    """
    questions = TestQuestionRepository.get_by_test(db, test_id)
    
    # Convert to student-safe schema
    return [
        TestQuestionForStudent(
            id=q.id,
            question_number=q.question_number,
            question_type=q.question_type,
            question_text=q.question_text,
            options_json=q.options_json,
            category=q.category
        )
        for q in questions
    ]
```

## Handling Student Answers

### 1. Save Student Answer (Upsert Pattern)

```python
def save_student_answer(
    db: Session, 
    test_id: UUID, 
    question_id: UUID, 
    answer: str
) -> StudentTestAnswer:
    """
    Save or update student answer
    Upsert ensures idempotent operation
    """
    return StudentAnswerRepository.upsert(
        db, test_id, question_id, answer
    )
```

### 2. Get All Student Answers for a Test

```python
def get_test_answers(db: Session, test_id: UUID) -> list[StudentTestAnswer]:
    """
    Get all student answers for a test
    """
    return StudentAnswerRepository.get_by_test(db, test_id)
```

### 3. Check Test Completion

```python
def check_test_completion(db: Session, test_id: UUID) -> dict:
    """
    Check how many questions are answered
    """
    test = TestRepository.get_by_id(db, test_id)
    answered_count = StudentAnswerRepository.count_answered(db, test_id)
    
    return {
        "total_questions": test.question_count,
        "answered": answered_count,
        "remaining": test.question_count - answered_count,
        "is_complete": answered_count == test.question_count
    }
```

### 4. Reset Test Answers

```python
def reset_test(db: Session, test_id: UUID) -> dict:
    """
    Clear all answers for a test (allow retake)
    """
    deleted_count = StudentAnswerRepository.delete_by_test(db, test_id)
    
    # Reset test status
    test = TestRepository.get_by_id(db, test_id)
    test.status = TestStatus.GENERATED
    test.started_at = None
    test.completed_at = None
    TestRepository.update(db, test)
    
    return {
        "message": "Test reset successfully",
        "answers_deleted": deleted_count
    }
```

## Common Patterns

### Complete Test Creation Workflow

```python
from uuid import UUID

def create_complete_test(
    db: Session, 
    user_id: int, 
    subject: str,
    question_type: QuestionType,
    categories: list[str],
    generated_questions: list[dict]
) -> dict:
    """
    Complete workflow: Create test and add questions
    """
    # 1. Create test
    test = Test(
        user_id=user_id,
        subject=subject,
        question_type=question_type,
        selected_categories=categories,
        question_count=len(generated_questions),
        status=TestStatus.GENERATED
    )
    test = TestRepository.create(db, test)
    
    # 2. Add questions in bulk
    questions = []
    for i, q_data in enumerate(generated_questions, start=1):
        question = TestQuestion(
            test_id=test.id,
            question_number=i,
            question_type=question_type,
            question_text=q_data["text"],
            options_json=q_data.get("options"),
            correct_answer=q_data["answer"],
            model_answer=q_data.get("explanation"),
            source_document=q_data.get("source"),
            source_page=q_data.get("page"),
            category=q_data["category"]
        )
        questions.append(question)
    
    TestQuestionRepository.create_bulk(db, questions)
    
    return {
        "test_id": test.id,
        "question_count": len(questions),
        "status": test.status
    }
```

### Student Test Taking Workflow

```python
def take_test_workflow(db: Session, test_id: UUID, user_id: int):
    """
    Complete student test-taking workflow
    """
    # 1. Verify test belongs to user
    test = TestRepository.get_by_id(db, test_id)
    if test.user_id != user_id:
        raise PermissionError("Test does not belong to user")
    
    # 2. Start test if not started
    if test.status == TestStatus.GENERATED:
        test.status = TestStatus.IN_PROGRESS
        test.started_at = datetime.utcnow()
        test = TestRepository.update(db, test)
    
    # 3. Get questions (without answers)
    questions = TestQuestionRepository.get_by_test(db, test_id)
    
    # 4. Get current answers
    answers = StudentAnswerRepository.get_by_test(db, test_id)
    answer_map = {ans.question_id: ans.student_answer for ans in answers}
    
    # 5. Build response
    question_list = []
    for q in questions:
        question_list.append({
            "id": q.id,
            "number": q.question_number,
            "type": q.question_type,
            "text": q.question_text,
            "options": q.options_json,
            "category": q.category,
            "student_answer": answer_map.get(q.id)
        })
    
    return {
        "test": test,
        "questions": question_list,
        "progress": {
            "answered": len([a for a in answer_map.values() if a]),
            "total": len(questions)
        }
    }
```

### Evaluation Preparation (Phase 5 Ready)

```python
def get_test_for_evaluation(db: Session, test_id: UUID) -> dict:
    """
    Get complete test data for evaluation
    Returns questions with correct answers and student answers
    """
    test = TestRepository.get_by_id(db, test_id)
    if test.status != TestStatus.SUBMITTED:
        raise ValueError("Test must be submitted before evaluation")
    
    questions = TestQuestionRepository.get_by_test(db, test_id)
    answers = StudentAnswerRepository.get_by_test(db, test_id)
    
    # Map answers to questions
    answer_map = {ans.question_id: ans for ans in answers}
    
    evaluation_data = []
    for q in questions:
        student_ans = answer_map.get(q.id)
        evaluation_data.append({
            "question_id": q.id,
            "question_number": q.question_number,
            "question_type": q.question_type,
            "question_text": q.question_text,
            "options": q.options_json,
            "correct_answer": q.correct_answer,
            "model_answer": q.model_answer,
            "student_answer": student_ans.student_answer if student_ans else None,
            "category": q.category
        })
    
    return {
        "test_id": test.id,
        "user_id": test.user_id,
        "subject": test.subject,
        "question_type": test.question_type,
        "questions": evaluation_data
    }
```

## Error Handling

### Safe Repository Operations

```python
from sqlalchemy.exc import IntegrityError

def safe_create_test(db: Session, user_id: int, test_data: dict) -> Test | None:
    """
    Create test with error handling
    """
    try:
        test = Test(
            user_id=user_id,
            subject=test_data["subject"],
            question_type=test_data["question_type"],
            selected_categories=test_data["categories"],
            question_count=test_data["question_count"],
            status=TestStatus.GENERATED
        )
        return TestRepository.create(db, test)
    except IntegrityError as e:
        db.rollback()
        print(f"Database integrity error: {e}")
        return None
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {e}")
        return None
```

## Performance Tips

### 1. Use Bulk Operations for Questions

```python
# ✅ GOOD: Bulk create
questions = [TestQuestion(...) for _ in range(10)]
TestQuestionRepository.create_bulk(db, questions)

# ❌ BAD: Individual creates
for q_data in questions_data:
    question = TestQuestion(...)
    TestQuestionRepository.create(db, question)  # Multiple commits!
```

### 2. Use Relationships for Loading

```python
# ✅ GOOD: Relationships are pre-configured with selectin loading
test = TestRepository.get_by_id(db, test_id)
questions = test.questions  # Already loaded efficiently

# ❌ BAD: Manual query
questions = TestQuestionRepository.get_by_test(db, test_id)
```

### 3. Count Before Loading

```python
# ✅ GOOD: Check count first
if TestQuestionRepository.count_by_test(db, test_id) > 0:
    questions = TestQuestionRepository.get_by_test(db, test_id)

# ❌ BAD: Load then check
questions = TestQuestionRepository.get_by_test(db, test_id)
if len(questions) > 0:
    # ...
```

## Database Session Management

### Using Dependency Injection (FastAPI)

```python
from fastapi import Depends
from app.api.dependencies import get_db

@app.post("/tests/", response_model=TestRead)
def create_test(
    test_data: TestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    API endpoint using dependency injection
    """
    test = Test(
        user_id=current_user.id,
        subject=test_data.subject,
        question_type=test_data.question_type,
        selected_categories=test_data.selected_categories,
        question_count=test_data.question_count,
        status=TestStatus.GENERATED
    )
    return TestRepository.create(db, test)
```

## Next Steps

Once Phase 4B (Question Generation) is implemented, you'll add:
- Gemini AI integration for question generation
- RAG retrieval for context-aware questions
- Question quality validation
- Difficulty adjustment

Once Phase 5 (Evaluation) is implemented, you'll add:
- Automatic MCQ evaluation
- AI-powered subjective answer evaluation
- Marks calculation
- Feedback generation

This foundation is ready to support all future functionality! 🚀
