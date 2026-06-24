"""
Unit tests for Examination repositories
Tests CRUD operations and business logic
"""
import pytest
from app.models.test import Test
from app.models.test_question import TestQuestion
from app.models.student_test_answer import StudentTestAnswer
from app.models.enums import QuestionType, TestStatus
from app.repositories.test_repository import TestRepository
from app.repositories.question_repository import TestQuestionRepository
from app.repositories.answer_repository import StudentAnswerRepository


class TestTestRepositoryTests:
    """Test suite for TestRepository"""
    
    def test_create_test(self, db_session, test_user):
        """Test creating a test via repository"""
        test = Test(
            user_id=test_user.id,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=["History"],
            question_count=5,
            status=TestStatus.GENERATED
        )
        
        created = TestRepository.create(db_session, test)
        
        assert created.id is not None
        assert created.user_id == test_user.id
        assert created.question_count == 5
    
    def test_get_by_id(self, db_session, test_user):
        """Test getting test by ID"""
        test = Test(
            user_id=test_user.id,
            subject="Social Studies",
            question_type=QuestionType.SHORT_ANSWER,
            selected_categories=["Geography"],
            question_count=3,
            status=TestStatus.GENERATED
        )
        created = TestRepository.create(db_session, test)
        
        found = TestRepository.get_by_id(db_session, created.id)
        
        assert found is not None
        assert found.id == created.id
        assert found.question_count == 3
    
    def test_get_by_user(self, db_session, test_user):
        """Test getting all tests for a user"""
        # Create multiple tests
        test1 = Test(
            user_id=test_user.id,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=["History"],
            question_count=5,
            status=TestStatus.GENERATED
        )
        test2 = Test(
            user_id=test_user.id,
            subject="Social Studies",
            question_type=QuestionType.FILL_BLANKS,
            selected_categories=["Geography"],
            question_count=3,
            status=TestStatus.IN_PROGRESS
        )
        
        TestRepository.create(db_session, test1)
        TestRepository.create(db_session, test2)
        
        tests = TestRepository.get_by_user(db_session, test_user.id)
        
        assert len(tests) >= 2
        assert all(t.user_id == test_user.id for t in tests)
    
    def test_get_by_user_and_status(self, db_session, test_user):
        """Test filtering tests by status"""
        test1 = Test(
            user_id=test_user.id,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=["History"],
            question_count=5,
            status=TestStatus.GENERATED
        )
        test2 = Test(
            user_id=test_user.id,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=["Geography"],
            question_count=3,
            status=TestStatus.IN_PROGRESS
        )
        
        TestRepository.create(db_session, test1)
        TestRepository.create(db_session, test2)
        
        generated = TestRepository.get_by_user_and_status(
            db_session, test_user.id, TestStatus.GENERATED
        )
        in_progress = TestRepository.get_by_user_and_status(
            db_session, test_user.id, TestStatus.IN_PROGRESS
        )
        
        assert len(generated) >= 1
        assert len(in_progress) >= 1
        assert all(t.status == TestStatus.GENERATED for t in generated)
        assert all(t.status == TestStatus.IN_PROGRESS for t in in_progress)
    
    def test_update_test(self, db_session, test_user):
        """Test updating a test"""
        test = Test(
            user_id=test_user.id,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=["History"],
            question_count=5,
            status=TestStatus.GENERATED
        )
        created = TestRepository.create(db_session, test)
        
        # Update status
        created.status = TestStatus.IN_PROGRESS
        updated = TestRepository.update(db_session, created)
        
        assert updated.status == TestStatus.IN_PROGRESS
    
    def test_delete_test(self, db_session, test_user):
        """Test deleting a test"""
        test = Test(
            user_id=test_user.id,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=["History"],
            question_count=5,
            status=TestStatus.GENERATED
        )
        created = TestRepository.create(db_session, test)
        test_id = created.id
        
        result = TestRepository.delete(db_session, created)
        
        assert result is True
        assert TestRepository.get_by_id(db_session, test_id) is None
    
    def test_count_by_user(self, db_session, test_user):
        """Test counting tests for a user"""
        initial_count = TestRepository.count_by_user(db_session, test_user.id)
        
        test = Test(
            user_id=test_user.id,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=["History"],
            question_count=5,
            status=TestStatus.GENERATED
        )
        TestRepository.create(db_session, test)
        
        new_count = TestRepository.count_by_user(db_session, test_user.id)
        
        assert new_count == initial_count + 1


class TestQuestionRepositoryTests:
    """Test suite for TestQuestionRepository"""
    
    def test_create_question(self, db_session, sample_test):
        """Test creating a question via repository"""
        question = TestQuestion(
            test_id=sample_test.id,
            question_number=1,
            question_type=QuestionType.MCQ,
            question_text="What is democracy?",
            correct_answer="A",
            category="Politics"
        )
        
        created = TestQuestionRepository.create(db_session, question)
        
        assert created.id is not None
        assert created.test_id == sample_test.id
        assert created.question_number == 1
    
    def test_create_bulk(self, db_session, sample_test):
        """Test bulk creating questions"""
        questions = [
            TestQuestion(
                test_id=sample_test.id,
                question_number=i,
                question_type=QuestionType.MCQ,
                question_text=f"Question {i}?",
                correct_answer=f"Answer {i}",
                category="History"
            )
            for i in range(1, 6)
        ]
        
        created = TestQuestionRepository.create_bulk(db_session, questions)
        
        assert len(created) == 5
        assert all(q.id is not None for q in created)
    
    def test_get_by_test(self, db_session, sample_test):
        """Test getting all questions for a test"""
        q1 = TestQuestion(
            test_id=sample_test.id,
            question_number=1,
            question_type=QuestionType.MCQ,
            question_text="Q1?",
            correct_answer="A1",
            category="History"
        )
        q2 = TestQuestion(
            test_id=sample_test.id,
            question_number=2,
            question_type=QuestionType.MCQ,
            question_text="Q2?",
            correct_answer="A2",
            category="History"
        )
        
        TestQuestionRepository.create(db_session, q1)
        TestQuestionRepository.create(db_session, q2)
        
        questions = TestQuestionRepository.get_by_test(db_session, sample_test.id)
        
        assert len(questions) >= 2
        # Verify ordering by question_number
        assert questions[0].question_number < questions[1].question_number
    
    def test_get_by_test_and_number(self, db_session, sample_test):
        """Test getting specific question by number"""
        question = TestQuestion(
            test_id=sample_test.id,
            question_number=5,
            question_type=QuestionType.SHORT_ANSWER,
            question_text="Specific question?",
            correct_answer="Specific answer",
            category="Geography"
        )
        TestQuestionRepository.create(db_session, question)
        
        found = TestQuestionRepository.get_by_test_and_number(
            db_session, sample_test.id, 5
        )
        
        assert found is not None
        assert found.question_number == 5
        assert found.question_text == "Specific question?"
    
    def test_count_by_test(self, db_session, sample_test):
        """Test counting questions in a test"""
        initial_count = TestQuestionRepository.count_by_test(db_session, sample_test.id)
        
        question = TestQuestion(
            test_id=sample_test.id,
            question_number=10,
            question_type=QuestionType.MCQ,
            question_text="New question?",
            correct_answer="Answer",
            category="History"
        )
        TestQuestionRepository.create(db_session, question)
        
        new_count = TestQuestionRepository.count_by_test(db_session, sample_test.id)
        
        assert new_count == initial_count + 1


class TestStudentAnswerRepositoryTests:
    """Test suite for StudentAnswerRepository"""
    
    def test_create_answer(self, db_session, sample_test, sample_question):
        """Test creating an answer via repository"""
        answer = StudentTestAnswer(
            test_id=sample_test.id,
            question_id=sample_question.id,
            student_answer="Student's answer"
        )
        
        created = StudentAnswerRepository.create(db_session, answer)
        
        assert created.id is not None
        assert created.test_id == sample_test.id
        assert created.question_id == sample_question.id
    
    def test_get_by_test_and_question(self, db_session, sample_test, sample_question):
        """Test getting answer by test and question"""
        answer = StudentTestAnswer(
            test_id=sample_test.id,
            question_id=sample_question.id,
            student_answer="Unique answer"
        )
        StudentAnswerRepository.create(db_session, answer)
        
        found = StudentAnswerRepository.get_by_test_and_question(
            db_session, sample_test.id, sample_question.id
        )
        
        assert found is not None
        assert found.student_answer == "Unique answer"
    
    def test_upsert_create(self, db_session, sample_test, sample_question):
        """Test upsert creating new answer"""
        result = StudentAnswerRepository.upsert(
            db_session,
            sample_test.id,
            sample_question.id,
            "New answer"
        )
        
        assert result.id is not None
        assert result.student_answer == "New answer"
    
    def test_upsert_update(self, db_session, sample_test, sample_question):
        """Test upsert updating existing answer"""
        # Create initial answer
        answer = StudentTestAnswer(
            test_id=sample_test.id,
            question_id=sample_question.id,
            student_answer="Old answer"
        )
        created = StudentAnswerRepository.create(db_session, answer)
        answer_id = created.id
        
        # Upsert should update
        result = StudentAnswerRepository.upsert(
            db_session,
            sample_test.id,
            sample_question.id,
            "Updated answer"
        )
        
        assert result.id == answer_id  # Same ID
        assert result.student_answer == "Updated answer"  # Updated content
    
    def test_count_answered(self, db_session, sample_test):
        """Test counting answered questions"""
        # Create questions
        q1 = TestQuestion(
            test_id=sample_test.id,
            question_number=1,
            question_type=QuestionType.MCQ,
            question_text="Q1?",
            correct_answer="A",
            category="History"
        )
        q2 = TestQuestion(
            test_id=sample_test.id,
            question_number=2,
            question_type=QuestionType.MCQ,
            question_text="Q2?",
            correct_answer="B",
            category="History"
        )
        q3 = TestQuestion(
            test_id=sample_test.id,
            question_number=3,
            question_type=QuestionType.MCQ,
            question_text="Q3?",
            correct_answer="C",
            category="History"
        )
        TestQuestionRepository.create_bulk(db_session, [q1, q2, q3])
        
        # Answer only 2 questions
        StudentAnswerRepository.create(db_session, StudentTestAnswer(
            test_id=sample_test.id, question_id=q1.id, student_answer="A"
        ))
        StudentAnswerRepository.create(db_session, StudentTestAnswer(
            test_id=sample_test.id, question_id=q2.id, student_answer="B"
        ))
        # q3 not answered
        
        count = StudentAnswerRepository.count_answered(db_session, sample_test.id)
        
        assert count == 2
    
    def test_delete_by_test(self, db_session, sample_test):
        """Test deleting all answers for a test"""
        # Create questions and answers
        q1 = TestQuestion(
            test_id=sample_test.id,
            question_number=1,
            question_type=QuestionType.MCQ,
            question_text="Q1?",
            correct_answer="A",
            category="History"
        )
        q2 = TestQuestion(
            test_id=sample_test.id,
            question_number=2,
            question_type=QuestionType.MCQ,
            question_text="Q2?",
            correct_answer="B",
            category="History"
        )
        TestQuestionRepository.create_bulk(db_session, [q1, q2])
        
        StudentAnswerRepository.create(db_session, StudentTestAnswer(
            test_id=sample_test.id, question_id=q1.id, student_answer="A"
        ))
        StudentAnswerRepository.create(db_session, StudentTestAnswer(
            test_id=sample_test.id, question_id=q2.id, student_answer="B"
        ))
        
        deleted_count = StudentAnswerRepository.delete_by_test(db_session, sample_test.id)
        
        assert deleted_count == 2
        answers = StudentAnswerRepository.get_by_test(db_session, sample_test.id)
        assert len(answers) == 0
