# Phase 4B: Question Generation Service - Usage Guide

## Quick Start

### Import and Initialize

```python
from app.services.question_generation import QuestionGeneratorService
from app.core.config import settings
from app.db.session import SessionLocal

# Initialize service
service = QuestionGeneratorService(
    api_key=settings.GEMINI_API_KEY,
    chroma_db_path=settings.CHROMA_DB_PATH
)

# Get database session
db = SessionLocal()
```

### Generate MCQ Exam

```python
response = service.generate_mcq_exam(
    db=db,
    user_id=1,
    categories=["History"],
    question_count=10
)

print(f"Exam ID: {response.test_id}")
print(f"Questions: {len(response.questions)}")
```

### Generate Other Question Types

```python
# Fill in the Blanks
fill_response = service.generate_fill_blank_exam(db, 1, ["Politics"], 5)

# Short Answer
short_response = service.generate_short_answer_exam(db, 1, ["Geography"], 8)

# Long Answer
long_response = service.generate_long_answer_exam(
    db, 1, ["History", "Geography"], 5
)
```

## Complete Example

```python
from app.services.question_generation import QuestionGeneratorService
from app.core.config import settings
from app.db.session import SessionLocal

service = QuestionGeneratorService(api_key=settings.GEMINI_API_KEY)
db = SessionLocal()

try:
    # Generate exam
    response = service.generate_mcq_exam(db, user_id=1, categories=["History"], question_count=5)
    
    # Display results
    for i, q in enumerate(response.questions, 1):
        print(f"Q{i}: {q.question_text}")
        print(f"Options: {q.options}")
        print(f"Answer: {q.correct_answer}\n")
        
finally:
    db.close()
```

## Error Handling

```python
try:
    response = service.generate_exam(db, request)
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Generation failed: {e}")
```

## Advanced Usage

### Custom Request

```python
from app.services.question_generation.schemas import ExamGenerationRequest
from app.models.enums import QuestionType

request = ExamGenerationRequest(
    user_id=1,
    subject="Social Studies",
    question_type=QuestionType.SHORT_ANSWER,
    selected_categories=["History", "Geography", "Politics"],
    question_count=6
)

response = service.generate_exam(db, request)
```

Done! Service is ready to use. 🚀
