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

@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
def test_malformed_json_response(mock_model_class, mock_configure):
    """Test malformed JSON response handling."""
    mock_response = Mock()
    mock_response.text = '{"skills": ["python", "java"'  # Missing closing bracket and brace
    
    mock_model = Mock()
    mock_model.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model
    
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
        extractor = SkillsExtractor()
        result = extractor.extract("Python Java")
        assert result == []

@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
def test_non_json_response(mock_model_class, mock_configure):
    """Test non-JSON response handling."""
    mock_response = Mock()
    mock_response.text = "Python, Java, Docker are the skills"
    
    mock_model = Mock()
    mock_model.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model
    
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
        extractor = SkillsExtractor()
        result = extractor.extract("Python Java Docker")
        assert result == []

@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
def test_missing_skills_key(mock_model_class, mock_configure):
    """Test JSON response missing 'skills' key."""
    mock_response = Mock()
    mock_response.text = '{"technologies": ["python", "java"]}'
    
    mock_model = Mock()
    mock_model.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model
    
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
        extractor = SkillsExtractor()
        result = extractor.extract("Python Java")
        assert result == []

@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
def test_non_list_skills_value(mock_model_class, mock_configure):
    """Test when skills value is not a list."""
    mock_response = Mock()
    mock_response.text = '{"skills": "python, java, docker"}'
    
    mock_model = Mock()
    mock_model.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model
    
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
        extractor = SkillsExtractor()
        result = extractor.extract("Python Java Docker")
        assert result == []

@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
def test_duplicate_skills_removal(mock_model_class, mock_configure):
    """Test removal of duplicate skills."""
    mock_response = Mock()
    mock_response.text = '{"skills": ["python", "java", "python", "docker", "java"]}'
    
    mock_model = Mock()
    mock_model.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model
    
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
        extractor = SkillsExtractor()
        result = extractor.extract("Python Java Docker")
        
        assert len(result) == 3
        assert "python" in result
        assert "java" in result
        assert "docker" in result
        assert result.count("python") == 1
        assert result.count("java") == 1

@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
def test_case_normalization(mock_model_class, mock_configure):
    """Test case normalization of skills."""
    mock_response = Mock()
    mock_response.text = '{"skills": ["PYTHON", "Java", "docker", "JavaScript"]}'
    
    mock_model = Mock()
    mock_model.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model
    
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
        extractor = SkillsExtractor()
        result = extractor.extract("PYTHON Java docker JavaScript")
        
        assert "python" in result
        assert "java" in result
        assert "docker" in result
        assert "javascript" in result

@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
def test_special_characters_in_skills(mock_model_class, mock_configure):
    """Test skills with special characters."""
    mock_response = Mock()
    mock_response.text = '{"skills": ["C++", "C#", ".NET", "Node.js", "Vue.js"]}'
    
    mock_model = Mock()
    mock_model.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model
    
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
        extractor = SkillsExtractor()
        result = extractor.extract("C++ C# .NET Node.js Vue.js")
        
        assert "c++" in result
        assert "c#" in result
        assert ".net" in result
        assert "node.js" in result
        assert "vue.js" in result

@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
def test_very_long_skills_list(mock_model_class, mock_configure):
    """Test handling of very long skills list."""
    import json
    long_skills_list = [f"skill_{i}" for i in range(100)]
    mock_response = Mock()
    mock_response.text = json.dumps({"skills": long_skills_list})
    
    mock_model = Mock()
    mock_model.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model
    
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
        extractor = SkillsExtractor()
        result = extractor.extract("Many skills text")
        
        assert len(result) == 100
        assert "skill_0" in result
        assert "skill_99" in result

if __name__ == "__main__":
    test_successful_extraction()
    test_data_cleaning()
    test_api_error_handling()
    test_empty_text()
    print("Skills extractor tests passed")