"""Tests for main framework."""

import pytest
from unittest.mock import Mock, patch
from resume_parser import ResumeParserFramework, PDFParser, WordParser


class TestResumeParserFramework:
    """Test cases for ResumeParserFramework."""

    @pytest.fixture
    def basic_parsers(self):
        """Provide basic parser configuration."""
        return {".pdf": PDFParser(), ".docx": WordParser()}

    def test_initialization_with_valid_components(self, basic_parsers, mock_extractors):
        """Test framework initializes with valid parsers and extractors."""
        framework = ResumeParserFramework(basic_parsers, mock_extractors)
        
        assert framework is not None
        assert ".pdf" in framework.supported_file_types
        assert ".docx" in framework.supported_file_types

    def test_unsupported_file_type_raises_error(self, basic_parsers, mock_extractors):
        """Test framework rejects unsupported file types."""
        framework = ResumeParserFramework(basic_parsers, mock_extractors)
        
        with pytest.raises(ValueError, match="Unsupported file type"):
            framework.parse_resume("document.txt")

    def test_case_insensitive_file_extensions(self, basic_parsers, mock_extractors):
        """Test framework handles case-insensitive file extensions."""
        framework = ResumeParserFramework(basic_parsers, mock_extractors)
        
        with patch.object(PDFParser, 'parse', return_value="sample content"):
            result = framework.parse_resume("resume.PDF")
            assert result.name == "Test User"

    def test_parse_resume_coordinates_extractors(self, basic_parsers):
        """Test framework coordinates all extractors properly."""
        # Create fresh mocks for this test
        fresh_extractors = {
            "name": Mock(extract=Mock(return_value="Test User")),
            "email": Mock(extract=Mock(return_value="test@example.com")), 
            "skills": Mock(extract=Mock(return_value=["python", "java"]))
        }
        
        framework = ResumeParserFramework(basic_parsers, fresh_extractors)
        
        with patch.object(PDFParser, 'parse', return_value="John Doe john@test.com"):
            result = framework.parse_resume("test.pdf")
            
            # Verify all extractors were called
            fresh_extractors["name"].extract.assert_called_once()
            fresh_extractors["email"].extract.assert_called_once()
            fresh_extractors["skills"].extract.assert_called_once()
            
            # Verify results
            assert result.name == "Test User"
            assert result.email == "test@example.com"
            assert result.skills == ["python", "java"]