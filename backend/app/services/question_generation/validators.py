"""
Validators for Question Generation
Validates generated questions before database storage
"""
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class QuestionValidator:
    """Validates generated questions"""
    
    @staticmethod
    def validate_mcq(question: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate MCQ question with comprehensive checks
        
        Args:
            question: Question dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check required fields
        required_fields = ['question_text', 'options', 'correct_answer', 'category']
        for field in required_fields:
            if field not in question:
                return False, f"Missing required field: {field}"
            if not question[field]:
                return False, f"Empty field: {field}"
        
        # Validate question text
        question_text = question['question_text'].strip()
        if len(question_text) < 10:
            return False, "Question text too short (minimum 10 characters)"
        if len(question_text) > 500:
            return False, f"Question text too long ({len(question_text)} chars, max 500)"
        
        # Validate options
        options = question['options']
        if not isinstance(options, list):
            return False, "Options must be a list"
        
        if len(options) != 4:
            return False, f"MCQ must have exactly 4 options, found {len(options)}"
        
        # Check each option
        cleaned_options = []
        for i, option in enumerate(options):
            if not option or not str(option).strip():
                return False, f"Option {i+1} is empty"
            
            option_text = str(option).strip()
            
            # Length validation
            if len(option_text) > 200:
                return False, f"Option {i+1} too long ({len(option_text)} chars, max 200)"
            if len(option_text) < 1:
                return False, f"Option {i+1} is empty"
            
            cleaned_options.append(option_text)
        
        # Check for duplicate options
        unique_options = set(opt.lower() for opt in cleaned_options)
        if len(unique_options) < 4:
            return False, "MCQ options must be unique (found duplicates)"
        
        # Validate correct answer
        correct_answer = str(question['correct_answer']).strip()
        if correct_answer not in options:
            # Try case-insensitive match
            options_lower = [str(opt).lower() for opt in options]
            if correct_answer.lower() not in options_lower:
                return False, "Correct answer must be one of the options"
        
        # Validate category
        valid_categories = {'History', 'Geography', 'Politics', 'Economics'}
        if question['category'] not in valid_categories:
            return False, f"Invalid category: {question['category']}"
        
        # Check source metadata (optional but recommended)
        if 'source_document' in question and question['source_document']:
            if 'source_page' not in question or not question['source_page']:
                logger.warning("Source document provided but source page missing")
        
        return True, ""
    
    @staticmethod
    def validate_fill_blank(question: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate Fill in the Blank question with enhanced checks
        
        Args:
            question: Question dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check required fields
        required_fields = ['question_text', 'correct_answer', 'category']
        for field in required_fields:
            if field not in question:
                return False, f"Missing required field: {field}"
            if not question[field]:
                return False, f"Empty field: {field}"
        
        # Validate question text
        question_text = question['question_text'].strip()
        if len(question_text) < 10:
            return False, "Question text too short (minimum 10 characters)"
        if len(question_text) > 500:
            return False, f"Question text too long ({len(question_text)} chars, max 500)"
        
        # Check for blank marker - check longest pattern first to avoid overlapping counts
        has_blank = False
        blank_count = 0
        
        # Replace all blank patterns with a placeholder to count them correctly
        # Check for 5 underscores first (most specific)
        if '_____' in question_text:
            has_blank = True
            blank_count = question_text.count('_____')
        # If no 5-underscore blanks, check for 4 underscores
        elif '____' in question_text:
            has_blank = True
            blank_count = question_text.count('____')
        # If no 4-underscore blanks, check for 3 underscores
        elif '___' in question_text:
            has_blank = True
            blank_count = question_text.count('___')
        
        if not has_blank:
            return False, "Question must contain a blank marked with underscores (___)"
        
        # Should be exactly 1 blank
        if blank_count > 1:
            return False, f"Question should have exactly 1 blank, found {blank_count}"
        
        # Validate correct answer
        correct_answer = question['correct_answer'].strip()
        if len(correct_answer) < 1:
            return False, "Correct answer cannot be empty"
        if len(correct_answer) > 100:
            return False, f"Correct answer too long ({len(correct_answer)} chars, max 100)"
        
        # Check answer length (should be concise - 1-4 words typical)
        words = correct_answer.split()
        if len(words) > 10:
            logger.warning(f"Fill blank answer is long ({len(words)} words). Expected 1-4 words.")
        
        # Validate category
        valid_categories = {'History', 'Geography', 'Politics', 'Economics'}
        if question['category'] not in valid_categories:
            return False, f"Invalid category: {question['category']}"
        
        return True, ""
    
    @staticmethod
    def validate_short_answer(question: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate Short Answer question
        
        Args:
            question: Question dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check required fields
        required_fields = ['question_text', 'model_answer', 'category']
        for field in required_fields:
            if field not in question:
                return False, f"Missing required field: {field}"
            if not question[field]:
                return False, f"Empty field: {field}"
        
        # Check question text
        question_text = question['question_text']
        if len(question_text) < 10:
            return False, "Question text too short (minimum 10 characters)"
        
        # Check model answer
        model_answer = question['model_answer']
        word_count = len(model_answer.split())
        
        if word_count < 10:
            return False, f"Model answer too short ({word_count} words). Expected 20-40 words."
        
        if word_count > 60:
            logger.warning(f"Model answer is long ({word_count} words). Expected 20-40 words.")
        
        return True, ""
    
    @staticmethod
    def validate_long_answer(question: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate Long Answer question
        
        Args:
            question: Question dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check required fields
        required_fields = ['question_text', 'model_answer', 'category']
        for field in required_fields:
            if field not in question:
                return False, f"Missing required field: {field}"
            if not question[field]:
                return False, f"Empty field: {field}"
        
        # Check question text
        question_text = question['question_text']
        if len(question_text) < 10:
            return False, "Question text too short (minimum 10 characters)"
        
        # Check model answer
        model_answer = question['model_answer']
        word_count = len(model_answer.split())
        
        if word_count < 40:
            return False, f"Model answer too short ({word_count} words). Expected 80-120 words."
        
        if word_count > 200:
            logger.warning(f"Model answer is very long ({word_count} words). Expected 80-120 words.")
        
        return True, ""
    
    @staticmethod
    def validate_question(question: Dict[str, Any], question_type: str) -> tuple[bool, str]:
        """
        Validate question based on its type
        
        Args:
            question: Question dictionary
            question_type: Type of question
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if question_type == "MCQ":
            return QuestionValidator.validate_mcq(question)
        elif question_type == "FILL_BLANKS":
            return QuestionValidator.validate_fill_blank(question)
        elif question_type == "SHORT_ANSWER":
            return QuestionValidator.validate_short_answer(question)
        elif question_type == "LONG_ANSWER":
            return QuestionValidator.validate_long_answer(question)
        else:
            return False, f"Unsupported question type: {question_type}"
    
    @staticmethod
    def validate_batch(
        questions: List[Dict[str, Any]], 
        question_type: str
    ) -> tuple[List[Dict[str, Any]], List[str]]:
        """
        Validate a batch of questions
        
        Args:
            questions: List of question dictionaries
            question_type: Type of questions
            
        Returns:
            Tuple of (valid_questions, error_messages)
        """
        valid_questions = []
        errors = []
        
        for i, question in enumerate(questions):
            is_valid, error_msg = QuestionValidator.validate_question(question, question_type)
            
            if is_valid:
                valid_questions.append(question)
            else:
                error = f"Question {i+1} validation failed: {error_msg}"
                errors.append(error)
                logger.warning(error)
        
        logger.info(f"Validated {len(questions)} questions: {len(valid_questions)} valid, {len(errors)} invalid")
        
        return valid_questions, errors
