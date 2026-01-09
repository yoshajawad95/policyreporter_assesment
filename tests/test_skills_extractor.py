"""Tests for skills extraction functionality."""

import sys
from unittest.mock import Mock, patch

sys.path.insert(0, '.')

from resume_parser.extractors.skills_extractor import SkillsExtractor

@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
def test_successful_extraction(mock_model_class, mock_configure):
    """Test successful skills extraction."""
    mock_response = Mock()
    mock_response.text = '{"skills": ["python", "java", "docker"]}'
    
    mock_model = Mock()
    mock_model.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model
    
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
        extractor = SkillsExtractor()
        result = extractor.extract("Skills: Python, Java, Docker")
        
        assert isinstance(result, list)
        assert "python" in result
        assert "java" in result
        assert "docker" in result

@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
def test_data_cleaning(mock_model_class, mock_configure):
    """Test data cleaning and validation."""
    mock_response = Mock()
    mock_response.text = '{"skills": ["python", "", "   ", "java"]}'
    
    mock_model = Mock()
    mock_model.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model
    
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
        extractor = SkillsExtractor()
        result = extractor.extract("Python Java")
        
        assert "python" in result
        assert "java" in result
        assert "" not in result
        assert "   " not in result

@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
def test_api_error_handling(mock_model_class, mock_configure):
    """Test API error handling."""
    mock_model = Mock()
    mock_model.generate_content.side_effect = Exception("API Error")
    mock_model_class.return_value = mock_model
    
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
        extractor = SkillsExtractor()
        result = extractor.extract("Python Java")
        assert result == []

@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
def test_empty_text(mock_model_class, mock_configure):
    """Test empty text handling."""
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
        extractor = SkillsExtractor()
        result = extractor.extract("")
        assert result == []

if __name__ == "__main__":
    test_successful_extraction()
    test_data_cleaning()
    test_api_error_handling()
    test_empty_text()
    print("Skills extractor tests passed")