"""
Unit tests for Question Generation Schemas
"""
import pytest
from pydantic import ValidationError
from app.services.question_generation.schemas import (
    ExamGenerationRequest,
    GeneratedQuestion,
    ExamGenerationResponse
)
from app.models.enums import QuestionType


class TestExamGenerationRequest:
    """Tests for ExamGenerationRequest schema"""
    
    def test_valid_request(self):
        """Test creating valid exam generation request"""
        request = ExamGenerationRequest(
            user_id=1,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=["History", "Geography"],
            question_count=5
        )
        
        assert request.user_id == 1
        assert request.subject == "Social Studies"
        assert request.question_type == QuestionType.MCQ
        assert len(request.selected_categories) == 2
        assert request.question_count == 5
    
    def test_question_count_too_low(self):
        """Test request with question count below minimum"""
        with pytest.raises(ValidationError) as exc_info:
            ExamGenerationRequest(
                user_id=1,
                subject="Social Studies",
                question_type=QuestionType.MCQ,
                selected_categories=["History"],
                question_count=0  # Invalid
            )
        
        assert "question_count" in str(exc_info.value).lower()
    
    def test_question_count_too_high(self):
        """Test request with question count above maximum"""
        with pytest.raises(ValidationError) as exc_info:
            ExamGenerationRequest(
                user_id=1,
                subject="Social Studies",
                question_type=QuestionType.MCQ,
                selected_categories=["History"],
                question_count=11  # Invalid
            )
        
        assert "question_count" in str(exc_info.value).lower()
    
    def test_empty_categories(self):
        """Test request with empty categories list"""
        with pytest.raises(ValidationError) as exc_info:
            ExamGenerationRequest(
                user_id=1,
                subject="Social Studies",
                question_type=QuestionType.MCQ,
                selected_categories=[],  # Invalid
                question_count=5
            )
        
        assert "categories" in str(exc_info.value).lower()
    
    def test_invalid_category(self):
        """Test request with invalid category"""
        with pytest.raises(ValidationError) as exc_info:
            ExamGenerationRequest(
                user_id=1,
                subject="Social Studies",
                question_type=QuestionType.MCQ,
                selected_categories=["InvalidCategory"],  # Invalid
                question_count=5
            )
        
        assert "Invalid category" in str(exc_info.value)
    
    def test_all_valid_categories(self):
        """Test request with all valid categories"""
        request = ExamGenerationRequest(
            user_id=1,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            selected_categories=["History", "Geography", "Politics", "Economics"],
            question_count=10
        )
        
        assert len(request.selected_categories) == 4


class TestGeneratedQuestion:
    """Tests for GeneratedQuestion schema"""
    
    def test_mcq_question(self):
        """Test creating MCQ question"""
        question = GeneratedQuestion(
            question_type=QuestionType.MCQ,
            question_text="What is democracy?",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            category="Politics"
        )
        
        assert question.question_type == QuestionType.MCQ
        assert len(question.options) == 4
        assert question.correct_answer == "A"
    
    def test_fill_blank_question(self):
        """Test creating Fill in the Blank question"""
        question = GeneratedQuestion(
            question_type=QuestionType.FILL_BLANKS,
            question_text="The capital of India is _____.",
            correct_answer="New Delhi",
            category="Geography"
        )
        
        assert question.question_type == QuestionType.FILL_BLANKS
        assert question.options is None
        assert question.correct_answer == "New Delhi"
    
    def test_short_answer_question(self):
        """Test creating Short Answer question"""
        question = GeneratedQuestion(
            question_type=QuestionType.SHORT_ANSWER,
            question_text="What is democracy?",
            correct_answer="Democracy is government by the people.",
            model_answer="Democracy is a form of government where citizens have the power to elect their representatives.",
            category="Politics"
        )
        
        assert question.question_type == QuestionType.SHORT_ANSWER
        assert question.model_answer is not None
    
    def test_question_with_source(self):
        """Test question with source metadata"""
        question = GeneratedQuestion(
            question_type=QuestionType.MCQ,
            question_text="Test question?",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            category="History",
            source_document="history.pdf",
            source_page=15
        )
        
        assert question.source_document == "history.pdf"
        assert question.source_page == 15


class TestExamGenerationResponse:
    """Tests for ExamGenerationResponse schema"""
    
    def test_valid_response(self):
        """Test creating valid exam generation response"""
        response = ExamGenerationResponse(
            test_id="123e4567-e89b-12d3-a456-426614174000",
            user_id=1,
            subject="Social Studies",
            question_type=QuestionType.MCQ,
            question_count=2,
            questions=[
                GeneratedQuestion(
                    question_type=QuestionType.MCQ,
                    question_text="Question 1?",
                    options=["A", "B", "C", "D"],
                    correct_answer="A",
                    category="History"
                ),
                GeneratedQuestion(
                    question_type=QuestionType.MCQ,
                    question_text="Question 2?",
                    options=["A", "B", "C", "D"],
                    correct_answer="B",
                    category="Geography"
                )
            ],
            status="GENERATED"
        )
        
        assert response.test_id == "123e4567-e89b-12d3-a456-426614174000"
        assert response.question_count == 2
        assert len(response.questions) == 2
        assert response.status == "GENERATED"
