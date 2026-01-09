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

    def test_file_not_found_error(self, basic_parsers, mock_extractors):
        """Test framework handles file not found gracefully."""
        framework = ResumeParserFramework(basic_parsers, mock_extractors)
        
        with pytest.raises(FileNotFoundError):
            framework.parse_resume("nonexistent.pdf")

    def test_parser_failure_handling(self, mock_extractors):
        """Test framework handles parser failures gracefully."""
        failing_parser = Mock()
        failing_parser.parse.side_effect = Exception("Parser failed")
        
        parsers = {".pdf": failing_parser}
        framework = ResumeParserFramework(parsers, mock_extractors)
        
        with pytest.raises(Exception, match="Parser failed"):
            framework.parse_resume("test.pdf")

    def test_extractor_failure_handling(self, basic_parsers):
        """Test framework handles extractor failures gracefully."""
        failing_extractors = {
            "name": Mock(extract=Mock(side_effect=Exception("Name extraction failed"))),
            "email": Mock(extract=Mock(return_value="test@example.com")),
            "skills": Mock(extract=Mock(return_value=["python"]))
        }
        
        framework = ResumeParserFramework(basic_parsers, failing_extractors)
        
        with patch.object(PDFParser, 'parse', return_value="sample content"):
            result = framework.parse_resume("test.pdf")
            
            # Should gracefully handle the failure and provide fallbacks
            assert result.name == "Unknown"  # Fallback for failed name extraction
            assert result.email == "test@example.com"  # Successful extraction
            assert result.skills == ["python"]  # Successful extraction

    def test_empty_extracted_content(self, basic_parsers, mock_extractors):
        """Test framework handles empty content from parser."""
        framework = ResumeParserFramework(basic_parsers, mock_extractors)
        
        with patch.object(PDFParser, 'parse', return_value=""):
            result = framework.parse_resume("test.pdf")
            
            # Should still call extractors even with empty content
            mock_extractors["name"].extract.assert_called_once_with("")
            mock_extractors["email"].extract.assert_called_once_with("")
            mock_extractors["skills"].extract.assert_called_once_with("")

    def test_missing_extractor_type(self, basic_parsers):
        """Test framework with incomplete extractor configuration."""
        incomplete_extractors = {
            "name": Mock(extract=Mock(return_value="Test User")),
            # Missing email and skills extractors
        }
        
        framework = ResumeParserFramework(basic_parsers, incomplete_extractors)
        
        with patch.object(PDFParser, 'parse', return_value="sample content"):
            result = framework.parse_resume("test.pdf")
            
            # Should use extracted name and provide defaults for missing extractors
            assert result.name == "Test User"
            assert result.email == ""  # Default fallback
            assert result.skills == []  # Default fallback

    def test_none_values_from_extractors(self, basic_parsers):
        """Test framework handles None values from extractors."""
        none_extractors = {
            "name": Mock(extract=Mock(return_value=None)),
            "email": Mock(extract=Mock(return_value=None)),
            "skills": Mock(extract=Mock(return_value=None))
        }
        
        framework = ResumeParserFramework(basic_parsers, none_extractors)
        
        with patch.object(PDFParser, 'parse', return_value="sample content"):
            result = framework.parse_resume("test.pdf")
            
            assert result.name is None
            assert result.email is None
            assert result.skills is None

    def test_very_large_content(self, basic_parsers, mock_extractors):
        """Test framework handles very large content."""
        large_content = "A" * 100000  # 100KB of text
        
        framework = ResumeParserFramework(basic_parsers, mock_extractors)
        
        with patch.object(PDFParser, 'parse', return_value=large_content):
            result = framework.parse_resume("test.pdf")
            
            # Verify extractors were called with large content
            mock_extractors["name"].extract.assert_called_once_with(large_content)
            assert result.name == "Test User"

    def test_unicode_content_handling(self, basic_parsers, mock_extractors):
        """Test framework handles unicode content properly."""
        unicode_content = "José María García-López 🚀 résumé@company.com"
        
        framework = ResumeParserFramework(basic_parsers, mock_extractors)
        
        with patch.object(PDFParser, 'parse', return_value=unicode_content):
            result = framework.parse_resume("test.pdf")
            
            mock_extractors["name"].extract.assert_called_once_with(unicode_content)
            mock_extractors["email"].extract.assert_called_once_with(unicode_content)
            mock_extractors["skills"].extract.assert_called_once_with(unicode_content)

    def test_multiple_file_extensions(self, mock_extractors):
        """Test framework with multiple similar file extensions."""
        parsers = {
            ".pdf": PDFParser(),
            ".PDF": PDFParser(),  # Different case
            ".docx": WordParser(),
            ".doc": WordParser()
        }
        
        framework = ResumeParserFramework(parsers, mock_extractors)
        
        # Should support both cases
        assert ".pdf" in framework.supported_file_types
        assert ".PDF" in framework.supported_file_types
        assert ".docx" in framework.supported_file_types
        assert ".doc" in framework.supported_file_types