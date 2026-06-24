"""
Verification Script for Phase 4B: Question Generation Service
Tests complete workflow from retrieval to database storage
"""
import sys
import os
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.config import settings
from app.services.question_generation.generator import QuestionGeneratorService
from app.services.question_generation.schemas import ExamGenerationRequest
from app.models.enums import QuestionType
from app.models.user import User
from app.repositories.test_repository import TestRepository
from app.repositories.question_repository import TestQuestionRepository


def verify_prerequisites():
    """Verify all prerequisites are met"""
    print("\n🔍 Verifying Prerequisites...")
    print("="*60)
    
    # Check environment variables
    print("\n✅ Checking Environment Variables:")
    required_vars = ["DATABASE_URL", "GEMINI_API_KEY"]
    for var in required_vars:
        value = getattr(settings, var, None) or os.getenv(var)
        if value:
            masked = value[:10] + "..." if len(value) > 10 else value
            print(f"  ✓ {var}: {masked}")
        else:
            print(f"  ✗ {var}: NOT SET")
            return False
    
    # Check ChromaDB
    print("\n✅ Checking ChromaDB:")
    if os.path.exists(settings.CHROMA_DB_PATH):
        print(f"  ✓ ChromaDB exists at: {settings.CHROMA_DB_PATH}")
    else:
        print(f"  ✗ ChromaDB not found at: {settings.CHROMA_DB_PATH}")
        print("    Please run ingestion first: python app/rag/ingestion/ingest_all_local.py")
        return False
    
    return True


def create_test_user(db: Session) -> User:
    """Create or get test user"""
    user = db.query(User).filter(User.email == "phase4b_test@example.com").first()
    
    if not user:
        user = User(
            email="phase4b_test@example.com",
            full_name="Phase 4B Test User",
            password_hash="hashed_password"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"\n✅ Created test user: {user.email}")
    else:
        print(f"\n✅ Using existing test user: {user.email}")
    
    return user


def test_mcq_generation(db: Session, service: QuestionGeneratorService, user: User):
    """Test MCQ generation"""
    print("\n" + "="*60)
    print("TEST 1: Generate 5 MCQs from History")
    print("="*60)
    
    try:
        request = ExamGenerationRequest(
            user_id=user.id,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=["History"],
            question_count=5
        )
        
        print(f"Request: {request.question_count} {request.question_type.value} questions from {request.selected_categories}")
        
        response = service.generate_exam(db, request)
        
        print(f"✅ Generated test: {response.test_id}")
        print(f"✅ Questions generated: {len(response.questions)}")
        
        # Display first question
        if response.questions:
            q = response.questions[0]
            print(f"\n📝 Sample Question:")
            print(f"   Question: {q.question_text}")
            print(f"   Options: {q.options}")
            print(f"   Answer: {q.correct_answer}")
            print(f"   Category: {q.category}")
            print(f"   Source: {q.source_document} (Page {q.source_page})")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False


def test_fill_blank_generation(db: Session, service: QuestionGeneratorService, user: User):
    """Test Fill in the Blanks generation"""
    print("\n" + "="*60)
    print("TEST 2: Generate 5 Fill in the Blanks from Politics")
    print("="*60)
    
    try:
        request = ExamGenerationRequest(
            user_id=user.id,
            subject="Social Studies",
            question_type=QuestionType.FILL_BLANKS,
            selected_categories=["Politics"],
            question_count=5
        )
        
        print(f"Request: {request.question_count} {request.question_type.value} questions from {request.selected_categories}")
        
        response = service.generate_exam(db, request)
        
        print(f"✅ Generated test: {response.test_id}")
        print(f"✅ Questions generated: {len(response.questions)}")
        
        # Display first question
        if response.questions:
            q = response.questions[0]
            print(f"\n📝 Sample Question:")
            print(f"   Question: {q.question_text}")
            print(f"   Answer: {q.correct_answer}")
            print(f"   Category: {q.category}")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False


def test_short_answer_generation(db: Session, service: QuestionGeneratorService, user: User):
    """Test Short Answer generation"""
    print("\n" + "="*60)
    print("TEST 3: Generate 3 Short Answers from Geography")
    print("="*60)
    
    try:
        request = ExamGenerationRequest(
            user_id=user.id,
            subject="Social Studies",
            question_type=QuestionType.SHORT_ANSWER,
            selected_categories=["Geography"],
            question_count=3
        )
        
        print(f"Request: {request.question_count} {request.question_type.value} questions from {request.selected_categories}")
        
        response = service.generate_exam(db, request)
        
        print(f"✅ Generated test: {response.test_id}")
        print(f"✅ Questions generated: {len(response.questions)}")
        
        # Display first question
        if response.questions:
            q = response.questions[0]
            print(f"\n📝 Sample Question:")
            print(f"   Question: {q.question_text}")
            print(f"   Model Answer: {q.model_answer[:100]}...")
            print(f"   Category: {q.category}")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False


def test_long_answer_generation(db: Session, service: QuestionGeneratorService, user: User):
    """Test Long Answer generation"""
    print("\n" + "="*60)
    print("TEST 4: Generate 3 Long Answers from All Categories")
    print("="*60)
    
    try:
        request = ExamGenerationRequest(
            user_id=user.id,
            subject="Social Studies",
            question_type=QuestionType.LONG_ANSWER,
            selected_categories=["History", "Geography", "Politics", "Economics"],
            question_count=3
        )
        
        print(f"Request: {request.question_count} {request.question_type.value} questions from {request.selected_categories}")
        
        response = service.generate_exam(db, request)
        
        print(f"✅ Generated test: {response.test_id}")
        print(f"✅ Questions generated: {len(response.questions)}")
        
        # Display first question
        if response.questions:
            q = response.questions[0]
            print(f"\n📝 Sample Question:")
            print(f"   Question: {q.question_text}")
            print(f"   Model Answer: {q.model_answer[:150]}...")
            print(f"   Category: {q.category}")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False


def test_database_storage(db: Session, user: User):
    """Verify questions are stored in database"""
    print("\n" + "="*60)
    print("TEST 5: Verify Database Storage")
    print("="*60)
    
    # Get user's tests
    tests = TestRepository.get_by_user(db, user.id)
    
    print(f"✅ Total tests for user: {len(tests)}")
    
    if tests:
        test = tests[0]
        print(f"✅ Latest test: {test.id}")
        print(f"   Subject: {test.subject}")
        print(f"   Type: {test.question_type.value}")
        print(f"   Count: {test.question_count}")
        print(f"   Status: {test.status.value}")
        
        # Get questions
        questions = TestQuestionRepository.get_by_test(db, test.id)
        print(f"✅ Questions in database: {len(questions)}")
        
        if questions:
            q = questions[0]
            print(f"\n📝 First Question:")
            print(f"   Number: {q.question_number}")
            print(f"   Type: {q.question_type.value}")
            print(f"   Text: {q.question_text[:80]}...")
            print(f"   Category: {q.category}")
            print(f"   Source: {q.source_document} (Page {q.source_page})")
        
        return True
    
    return False


def run_verification():
    """Run complete verification"""
    print("\n" + "="*60)
    print("PHASE 4B VERIFICATION: QUESTION GENERATION SERVICE")
    print("="*60)
    
    # Check prerequisites
    if not verify_prerequisites():
        print("\n❌ Prerequisites not met. Please fix the issues above.")
        return False
    
    # Initialize service
    print("\n✅ Initializing Question Generator Service...")
    service = QuestionGeneratorService(
        api_key=settings.GEMINI_API_KEY,
        chroma_db_path=settings.CHROMA_DB_PATH,
        use_local_embeddings=True
    )
    print("✅ Service initialized successfully")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Create test user
        user = create_test_user(db)
        
        # Run tests
        results = []
        
        results.append(("MCQ Generation", test_mcq_generation(db, service, user)))
        results.append(("Fill Blank Generation", test_fill_blank_generation(db, service, user)))
        results.append(("Short Answer Generation", test_short_answer_generation(db, service, user)))
        results.append(("Long Answer Generation", test_long_answer_generation(db, service, user)))
        results.append(("Database Storage", test_database_storage(db, user)))
        
        # Summary
        print("\n" + "="*60)
        print("VERIFICATION SUMMARY")
        print("="*60)
        
        for test_name, passed in results:
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"{status}: {test_name}")
        
        all_passed = all(result[1] for result in results)
        
        if all_passed:
            print("\n" + "="*60)
            print("✅ ALL TESTS PASSED - Phase 4B Complete!")
            print("="*60)
            return True
        else:
            print("\n" + "="*60)
            print("❌ SOME TESTS FAILED - Please review errors above")
            print("="*60)
            return False
            
    except Exception as e:
        print(f"\n❌ Verification failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        db.close()


if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)
