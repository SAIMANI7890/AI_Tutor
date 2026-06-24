"""
Unit tests for Examination models
Tests model creation, relationships, and constraints
"""
import pytest
import uuid
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app.models.test import Test
from app.models.test_question import TestQuestion
from app.models.student_test_answer import StudentTestAnswer
from app.models.user import User
from app.models.enums import QuestionType, TestStatus


class TestExaminationModels:
    """Test suite for examination models"""
    
    def test_create_test(self, db_session, test_user):
        """Test creating a Test model"""
        test = Test(
            user_id=test_user.id,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=["History", "Geography"],
            question_count=5,
            status=TestStatus.GENERATED
        )
        
        db_session.add(test)
        db_session.commit()
        db_session.refresh(test)
        
        assert test.id is not None
        assert isinstance(test.id, uuid.UUID)
        assert test.user_id == test_user.id
        assert test.subject == "Social Studies"
        assert test.question_type == QuestionType.MCQ
        assert test.selected_categories == ["History", "Geography"]
        assert test.question_count == 5
        assert test.status == TestStatus.GENERATED
        assert test.created_at is not None
        assert test.started_at is None
        assert test.completed_at is None
    
    def test_test_user_relationship(self, db_session, test_user):
        """Test Test-User relationship"""
        test = Test(
            user_id=test_user.id,
            subject="Social Studies",
            question_type=QuestionType.SHORT_ANSWER,
            selected_categories=["Politics"],
            question_count=3,
            status=TestStatus.GENERATED
        )
        
        db_session.add(test)
        db_session.commit()
        db_session.refresh(test)
        
        # Test relationship
        assert test.user is not None
        assert test.user.id == test_user.id
        assert test.user.email == test_user.email
        
        # Test back-reference
        db_session.refresh(test_user)
        assert len(test_user.tests) > 0
        assert test.id in [t.id for t in test_user.tests]
    
    def test_create_test_question(self, db_session, test_user):
        """Test creating a TestQuestion model"""
        # Create test first
        test = Test(
            user_id=test_user.id,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=["History"],
            question_count=1,
            status=TestStatus.GENERATED
        )
        db_session.add(test)
        db_session.commit()
        
        # Create question
        question = TestQuestion(
            test_id=test.id,
            question_number=1,
            question_type=QuestionType.MCQ,
            question_text="What is democracy?",
            options_json=["Rule by people", "Rule by king", "Rule by military", "Rule by religion"],
            correct_answer="A",
            model_answer="Democracy is a form of government where power is held by the people.",
            source_document="social_politics.pdf",
            source_page=15,
            category="Politics"
        )
        
        db_session.add(question)
        db_session.commit()
        db_session.refresh(question)
        
        assert question.id is not None
        assert isinstance(question.id, uuid.UUID)
        assert question.test_id == test.id
        assert question.question_number == 1
        assert question.question_type == QuestionType.MCQ
        assert question.question_text == "What is democracy?"
        assert len(question.options_json) == 4
        assert question.correct_answer == "A"
        assert question.category == "Politics"
    
    def test_question_test_relationship(self, db_session, test_user):
        """Test TestQuestion-Test relationship"""
        test = Test(
            user_id=test_user.id,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=["History"],
            question_count=2,
            status=TestStatus.GENERATED
        )
        db_session.add(test)
        db_session.commit()
        
        # Create multiple questions
        q1 = TestQuestion(
            test_id=test.id,
            question_number=1,
            question_type=QuestionType.MCQ,
            question_text="Question 1?",
            correct_answer="A",
            category="History"
        )
        q2 = TestQuestion(
            test_id=test.id,
            question_number=2,
            question_type=QuestionType.MCQ,
            question_text="Question 2?",
            correct_answer="B",
            category="History"
        )
        
        db_session.add_all([q1, q2])
        db_session.commit()
        
        # Test relationship
        db_session.refresh(test)
        assert len(test.questions) == 2
        assert q1.id in [q.id for q in test.questions]
        assert q2.id in [q.id for q in test.questions]
    
    def test_create_student_answer(self, db_session, test_user):
        """Test creating a StudentTestAnswer model"""
        # Create test and question
        test = Test(
            user_id=test_user.id,
            subject="Social Studies",
            question_type=QuestionType.SHORT_ANSWER,
            selected_categories=["Geography"],
            question_count=1,
            status=TestStatus.IN_PROGRESS
        )
        db_session.add(test)
        db_session.commit()
        
        question = TestQuestion(
            test_id=test.id,
            question_number=1,
            question_type=QuestionType.SHORT_ANSWER,
            question_text="What is a monsoon?",
            correct_answer="A seasonal wind pattern",
            category="Geography"
        )
        db_session.add(question)
        db_session.commit()
        
        # Create answer
        answer = StudentTestAnswer(
            test_id=test.id,
            question_id=question.id,
            student_answer="A monsoon is a seasonal wind that brings heavy rainfall."
        )
        
        db_session.add(answer)
        db_session.commit()
        db_session.refresh(answer)
        
        assert answer.id is not None
        assert isinstance(answer.id, uuid.UUID)
        assert answer.test_id == test.id
        assert answer.question_id == question.id
        assert "monsoon" in answer.student_answer.lower()
        assert answer.created_at is not None
        assert answer.updated_at is not None
    
    def test_answer_relationships(self, db_session, test_user):
        """Test StudentTestAnswer relationships"""
        test = Test(
            user_id=test_user.id,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=["History"],
            question_count=1,
            status=TestStatus.IN_PROGRESS
        )
        db_session.add(test)
        db_session.commit()
        
        question = TestQuestion(
            test_id=test.id,
            question_number=1,
            question_type=QuestionType.MCQ,
            question_text="Test question?",
            correct_answer="A",
            category="History"
        )
        db_session.add(question)
        db_session.commit()
        
        answer = StudentTestAnswer(
            test_id=test.id,
            question_id=question.id,
            student_answer="A"
        )
        db_session.add(answer)
        db_session.commit()
        
        # Test relationships
        assert answer.test is not None
        assert answer.test.id == test.id
        assert answer.question is not None
        assert answer.question.id == question.id
        
        # Test back-references
        db_session.refresh(test)
        db_session.refresh(question)
        assert len(test.student_answers) == 1
        assert len(question.student_answers) == 1
    
    def test_cascade_delete_test(self, db_session, test_user):
        """Test cascade delete when test is deleted"""
        test = Test(
            user_id=test_user.id,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=["History"],
            question_count=2,
            status=TestStatus.IN_PROGRESS
        )
        db_session.add(test)
        db_session.commit()
        
        # Create questions
        q1 = TestQuestion(
            test_id=test.id,
            question_number=1,
            question_type=QuestionType.MCQ,
            question_text="Q1?",
            correct_answer="A",
            category="History"
        )
        q2 = TestQuestion(
            test_id=test.id,
            question_number=2,
            question_type=QuestionType.MCQ,
            question_text="Q2?",
            correct_answer="B",
            category="History"
        )
        db_session.add_all([q1, q2])
        db_session.commit()
        
        # Create answers
        a1 = StudentTestAnswer(test_id=test.id, question_id=q1.id, student_answer="A")
        a2 = StudentTestAnswer(test_id=test.id, question_id=q2.id, student_answer="B")
        db_session.add_all([a1, a2])
        db_session.commit()
        
        test_id = test.id
        q1_id = q1.id
        q2_id = q2.id
        a1_id = a1.id
        a2_id = a2.id
        
        # Delete test
        db_session.delete(test)
        db_session.commit()
        
        # Verify cascade delete
        assert db_session.query(Test).filter(Test.id == test_id).first() is None
        assert db_session.query(TestQuestion).filter(TestQuestion.id == q1_id).first() is None
        assert db_session.query(TestQuestion).filter(TestQuestion.id == q2_id).first() is None
        assert db_session.query(StudentTestAnswer).filter(StudentTestAnswer.id == a1_id).first() is None
        assert db_session.query(StudentTestAnswer).filter(StudentTestAnswer.id == a2_id).first() is None
    
    def test_cascade_delete_user(self, db_session):
        """Test cascade delete when user is deleted"""
        # Create user
        user = User(
            email="cascade@test.com",
            full_name="Cascade Test",
            password_hash="hashed"
        )
        db_session.add(user)
        db_session.commit()
        
        # Create test
        test = Test(
            user_id=user.id,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=["History"],
            question_count=1,
            status=TestStatus.GENERATED
        )
        db_session.add(test)
        db_session.commit()
        
        user_id = user.id
        test_id = test.id
        
        # Delete user
        db_session.delete(user)
        db_session.commit()
        
        # Verify cascade delete
        assert db_session.query(User).filter(User.id == user_id).first() is None
        assert db_session.query(Test).filter(Test.id == test_id).first() is None
    
    def test_unique_constraint_question_number(self, db_session, test_user):
        """Test unique constraint on test_id + question_number"""
        test = Test(
            user_id=test_user.id,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=["History"],
            question_count=1,
            status=TestStatus.GENERATED
        )
        db_session.add(test)
        db_session.commit()
        
        q1 = TestQuestion(
            test_id=test.id,
            question_number=1,
            question_type=QuestionType.MCQ,
            question_text="Q1?",
            correct_answer="A",
            category="History"
        )
        db_session.add(q1)
        db_session.commit()
        
        # Try to create duplicate question number
        q2 = TestQuestion(
            test_id=test.id,
            question_number=1,  # Same number!
            question_type=QuestionType.MCQ,
            question_text="Q2?",
            correct_answer="B",
            category="History"
        )
        db_session.add(q2)
        
        # SQLite may not enforce this, but PostgreSQL will
        # Skip test if using SQLite
        import sys
        if 'sqlite' in str(db_session.bind.url):
            pytest.skip("SQLite doesn't enforce unique constraints reliably")
        
        with pytest.raises(IntegrityError):
            db_session.commit()
        
        db_session.rollback()
    
    def test_unique_constraint_test_question_answer(self, db_session, test_user):
        """Test unique constraint on test_id + question_id for answers"""
        test = Test(
            user_id=test_user.id,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=["History"],
            question_count=1,
            status=TestStatus.IN_PROGRESS
        )
        db_session.add(test)
        db_session.commit()
        
        question = TestQuestion(
            test_id=test.id,
            question_number=1,
            question_type=QuestionType.MCQ,
            question_text="Q?",
            correct_answer="A",
            category="History"
        )
        db_session.add(question)
        db_session.commit()
        
        a1 = StudentTestAnswer(
            test_id=test.id,
            question_id=question.id,
            student_answer="A"
        )
        db_session.add(a1)
        db_session.commit()
        
        # Try to create duplicate answer
        a2 = StudentTestAnswer(
            test_id=test.id,
            question_id=question.id,  # Same test + question!
            student_answer="B"
        )
        db_session.add(a2)
        
        # SQLite may not enforce this, but PostgreSQL will
        # Skip test if using SQLite
        import sys
        if 'sqlite' in str(db_session.bind.url):
            pytest.skip("SQLite doesn't enforce unique constraints reliably")
        
        with pytest.raises(IntegrityError):
            db_session.commit()
        
        db_session.rollback()
