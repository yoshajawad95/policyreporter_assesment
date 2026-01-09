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