"""Tests for name extraction functionality."""

import pytest
from unittest.mock import Mock, patch
from resume_parser.extractors.name_extractor import NameExtractor


class TestNameExtractor:
    """Test cases for NameExtractor."""

    def test_initialization_without_api_key_raises_error(self):
        """Test that missing API key raises ValueError."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="GEMINI_API_KEY not found"):
                NameExtractor()

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_extract_successful_json_response(self, mock_model_class, mock_configure):
        """Test successful name extraction with JSON response."""
        # Setup
        mock_response = Mock()
        mock_response.text = '{"name": "John Doe"}'
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        # Execute
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
            extractor = NameExtractor()
            result = extractor.extract("John Doe Software Engineer")
        
        # Assert
        assert result == "John Doe"
        mock_model.generate_content.assert_called_once()

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_extract_handles_api_error_gracefully(self, mock_model_class, mock_configure):
        """Test graceful handling of API errors."""
        # Setup
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("API connection failed")
        mock_model_class.return_value = mock_model
        
        # Execute
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
            extractor = NameExtractor()
            result = extractor.extract("John Doe")
        
        # Assert - should not raise exception
        assert result == "Unknown"

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_extract_empty_text_returns_unknown(self, mock_model_class, mock_configure):
        """Test empty text handling."""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
            extractor = NameExtractor()
            result = extractor.extract("")
            assert result == "Unknown"

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_extract_malformed_json_response(self, mock_model_class, mock_configure):
        """Test handling of malformed JSON response."""
        mock_response = Mock()
        mock_response.text = '{"name": "John Doe"'  # Missing closing brace
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
            extractor = NameExtractor()
            result = extractor.extract("John Doe")
            assert result == "Unknown"

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_extract_non_json_response(self, mock_model_class, mock_configure):
        """Test handling of non-JSON response."""
        mock_response = Mock()
        mock_response.text = "John Doe is the name"
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
            extractor = NameExtractor()
            result = extractor.extract("John Doe")
            assert result == "Unknown"

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_extract_missing_name_key_in_json(self, mock_model_class, mock_configure):
        """Test JSON response missing 'name' key."""
        mock_response = Mock()
        mock_response.text = '{"full_name": "John Doe"}'
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
            extractor = NameExtractor()
            result = extractor.extract("John Doe")
            assert result == "Unknown"

    @pytest.mark.parametrize("input_text,expected_name", [
        ("", "Unknown"),
        (None, "Unknown"),
        ("   ", "Unknown"),
        ("123456", "Unknown"),
        ("@#$%^&*()", "Unknown"),
    ])
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_extract_invalid_inputs(self, mock_model_class, mock_configure, input_text, expected_name):
        """Test various invalid input scenarios."""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
            extractor = NameExtractor()
            result = extractor.extract(input_text)
            assert result == expected_name

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_extract_unicode_name_handling(self, mock_model_class, mock_configure):
        """Test extraction with unicode characters in names."""
        mock_response = Mock()
        mock_response.text = '{"name": "José María García-López"}'
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
            extractor = NameExtractor()
            result = extractor.extract("José María García-López Software Engineer")
            assert result == "José María García-López"