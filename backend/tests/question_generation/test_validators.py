"""
Unit tests for Question Validators
"""
import pytest
from app.services.question_generation.validators import QuestionValidator


class TestMCQValidator:
    """Tests for MCQ validation"""
    
    def test_valid_mcq(self):
        """Test validating a correct MCQ"""
        question = {
            "question_text": "What is the capital of India?",
            "options": [
                "New Delhi",
                "Mumbai",
                "Kolkata",
                "Chennai"
            ],
            "correct_answer": "New Delhi",
            "category": "Geography",
            "source_document": "geography.pdf",
            "source_page": 15
        }
        
        is_valid, error = QuestionValidator.validate_mcq(question)
        
        assert is_valid is True
        assert error == ""
    
    def test_mcq_missing_field(self):
        """Test MCQ with missing required field"""
        question = {
            "question_text": "What is democracy?",
            "options": ["A", "B", "C", "D"],
            # Missing correct_answer
            "category": "Politics"
        }
        
        is_valid, error = QuestionValidator.validate_mcq(question)
        
        assert is_valid is False
        assert "correct_answer" in error
    
    def test_mcq_wrong_number_of_options(self):
        """Test MCQ with wrong number of options"""
        question = {
            "question_text": "What is democracy?",
            "options": ["A", "B", "C"],  # Only 3 options
            "correct_answer": "A",
            "category": "Politics"
        }
        
        is_valid, error = QuestionValidator.validate_mcq(question)
        
        assert is_valid is False
        assert "4 options" in error
    
    def test_mcq_correct_answer_not_in_options(self):
        """Test MCQ where correct answer is not one of the options"""
        question = {
            "question_text": "What is democracy?",
            "options": ["A", "B", "C", "D"],
            "correct_answer": "E",  # Not in options
            "category": "Politics"
        }
        
        is_valid, error = QuestionValidator.validate_mcq(question)
        
        assert is_valid is False
        assert "one of the options" in error
    
    def test_mcq_empty_option(self):
        """Test MCQ with empty option"""
        question = {
            "question_text": "What is democracy?",
            "options": ["A", "", "C", "D"],  # Empty option
            "correct_answer": "A",
            "category": "Politics"
        }
        
        is_valid, error = QuestionValidator.validate_mcq(question)
        
        assert is_valid is False
        assert "empty" in error.lower()
    
    def test_mcq_short_question_text(self):
        """Test MCQ with too short question text"""
        question = {
            "question_text": "What?",  # Too short
            "options": ["A", "B", "C", "D"],
            "correct_answer": "A",
            "category": "Politics"
        }
        
        is_valid, error = QuestionValidator.validate_mcq(question)
        
        assert is_valid is False
        assert "too short" in error.lower()


class TestFillBlankValidator:
    """Tests for Fill in the Blank validation"""
    
    def test_valid_fill_blank(self):
        """Test validating a correct Fill in the Blank"""
        question = {
            "question_text": "The capital of India is _____.",
            "correct_answer": "New Delhi",
            "category": "Geography",
            "source_document": "geography.pdf",
            "source_page": 15
        }
        
        is_valid, error = QuestionValidator.validate_fill_blank(question)
        
        assert is_valid is True
        assert error == ""
    
    def test_fill_blank_missing_blank_marker(self):
        """Test Fill blank without blank marker"""
        question = {
            "question_text": "The capital of India is New Delhi.",  # No blank
            "correct_answer": "New Delhi",
            "category": "Geography"
        }
        
        is_valid, error = QuestionValidator.validate_fill_blank(question)
        
        assert is_valid is False
        assert "blank" in error.lower()
    
    def test_fill_blank_empty_answer(self):
        """Test Fill blank with empty answer"""
        question = {
            "question_text": "The capital of India is _____.",
            "correct_answer": "",  # Empty
            "category": "Geography"
        }
        
        is_valid, error = QuestionValidator.validate_fill_blank(question)
        
        assert is_valid is False
        assert "empty" in error.lower()


class TestShortAnswerValidator:
    """Tests for Short Answer validation"""
    
    def test_valid_short_answer(self):
        """Test validating a correct Short Answer"""
        question = {
            "question_text": "What is democracy?",
            "model_answer": "Democracy is a form of government where power is held by the people through elected representatives.",
            "category": "Politics",
            "source_document": "politics.pdf",
            "source_page": 20
        }
        
        is_valid, error = QuestionValidator.validate_short_answer(question)
        
        assert is_valid is True
        assert error == ""
    
    def test_short_answer_too_short(self):
        """Test Short Answer with too short model answer"""
        question = {
            "question_text": "What is democracy?",
            "model_answer": "Government by people.",  # Too short
            "category": "Politics"
        }
        
        is_valid, error = QuestionValidator.validate_short_answer(question)
        
        assert is_valid is False
        assert "too short" in error.lower()
    
    def test_short_answer_missing_model_answer(self):
        """Test Short Answer without model answer"""
        question = {
            "question_text": "What is democracy?",
            "category": "Politics"
            # Missing model_answer
        }
        
        is_valid, error = QuestionValidator.validate_short_answer(question)
        
        assert is_valid is False
        assert "model_answer" in error


class TestLongAnswerValidator:
    """Tests for Long Answer validation"""
    
    def test_valid_long_answer(self):
        """Test validating a correct Long Answer"""
        question = {
            "question_text": "Discuss the key features of Indian democracy.",
            "model_answer": "Indian democracy is characterized by several key features. First, it is based on universal adult suffrage, allowing all citizens above 18 to vote. Second, it follows the principle of separation of powers among the legislature, executive, and judiciary. Third, it guarantees fundamental rights to all citizens, ensuring equality and freedom. Fourth, it is a federal system with power shared between central and state governments.",
            "category": "Politics",
            "source_document": "politics.pdf",
            "source_page": 25
        }
        
        is_valid, error = QuestionValidator.validate_long_answer(question)
        
        assert is_valid is True
        assert error == ""
    
    def test_long_answer_too_short(self):
        """Test Long Answer with too short model answer"""
        question = {
            "question_text": "Discuss the key features of Indian democracy.",
            "model_answer": "Democracy in India has several features including voting rights and fundamental rights.",  # Too short
            "category": "Politics"
        }
        
        is_valid, error = QuestionValidator.validate_long_answer(question)
        
        assert is_valid is False
        assert "too short" in error.lower()


class TestBatchValidator:
    """Tests for batch validation"""
    
    def test_validate_batch_all_valid(self):
        """Test batch validation with all valid questions"""
        questions = [
            {
                "question_text": "What is the capital of India?",
                "options": ["New Delhi", "Mumbai", "Kolkata", "Chennai"],
                "correct_answer": "New Delhi",
                "category": "Geography"
            },
            {
                "question_text": "What is democracy?",
                "options": ["A", "B", "C", "D"],
                "correct_answer": "A",
                "category": "Politics"
            }
        ]
        
        valid, errors = QuestionValidator.validate_batch(questions, "MCQ")
        
        assert len(valid) == 2
        assert len(errors) == 0
    
    def test_validate_batch_some_invalid(self):
        """Test batch validation with some invalid questions"""
        questions = [
            {
                "question_text": "What is the capital of India?",
                "options": ["New Delhi", "Mumbai", "Kolkata", "Chennai"],
                "correct_answer": "New Delhi",
                "category": "Geography"
            },
            {
                "question_text": "What is democracy?",
                "options": ["A", "B"],  # Invalid: only 2 options
                "correct_answer": "A",
                "category": "Politics"
            }
        ]
        
        valid, errors = QuestionValidator.validate_batch(questions, "MCQ")
        
        assert len(valid) == 1
        assert len(errors) == 1
        assert "4 options" in errors[0]
    
    def test_validate_batch_empty(self):
        """Test batch validation with empty list"""
        valid, errors = QuestionValidator.validate_batch([], "MCQ")
        
        assert len(valid) == 0
        assert len(errors) == 0
