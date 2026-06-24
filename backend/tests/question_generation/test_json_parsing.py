"""
Unit tests for JSON parsing
"""
import pytest
from app.services.question_generation.generator import QuestionGeneratorService


class TestJSONParsing:
    """Tests for JSON parsing from LLM responses"""
    
    def test_parse_clean_json(self):
        """Test parsing clean JSON"""
        service = QuestionGeneratorService(api_key="test")
        
        response = '''
        {
            "questions": [
                {
                    "question_text": "What is democracy?",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "A"
                }
            ]
        }
        '''
        
        result = service.parse_json_response(response)
        
        assert "questions" in result
        assert len(result["questions"]) == 1
        assert result["questions"][0]["question_text"] == "What is democracy?"
    
    def test_parse_json_with_markdown_blocks(self):
        """Test parsing JSON wrapped in markdown code blocks"""
        service = QuestionGeneratorService(api_key="test")
        
        response = '''```json
        {
            "questions": [
                {
                    "question_text": "What is the capital?"
                }
            ]
        }
        ```'''
        
        result = service.parse_json_response(response)
        
        assert "questions" in result
        assert len(result["questions"]) == 1
    
    def test_parse_json_with_plain_markdown(self):
        """Test parsing JSON wrapped in plain markdown blocks"""
        service = QuestionGeneratorService(api_key="test")
        
        response = '''```
        {
            "questions": []
        }
        ```'''
        
        result = service.parse_json_response(response)
        
        assert "questions" in result
        assert isinstance(result["questions"], list)
    
    def test_parse_malformed_json(self):
        """Test parsing malformed JSON raises error"""
        service = QuestionGeneratorService(api_key="test")
        
        response = '''
        {
            "questions": [
                {
                    "question_text": "Invalid JSON
                }
            ]
        '''
        
        with pytest.raises(ValueError) as exc_info:
            service.parse_json_response(response)
        
        assert "Invalid JSON" in str(exc_info.value)
    
    def test_parse_empty_response(self):
        """Test parsing empty response"""
        service = QuestionGeneratorService(api_key="test")
        
        with pytest.raises(ValueError):
            service.parse_json_response("")
    
    def test_parse_json_with_whitespace(self):
        """Test parsing JSON with extra whitespace"""
        service = QuestionGeneratorService(api_key="test")
        
        response = '''
        
        
        {
            "questions": [
                {"question_text": "Test"}
            ]
        }
        
        
        '''
        
        result = service.parse_json_response(response)
        
        assert "questions" in result
