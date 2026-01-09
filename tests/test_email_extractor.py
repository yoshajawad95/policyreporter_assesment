"""Tests for email extraction functionality."""

import pytest
from resume_parser.extractors.email_extractor import EmailExtractor


class TestEmailExtractor:
    """Test cases for EmailExtractor."""

    @pytest.fixture
    def extractor(self):
        """Create EmailExtractor instance."""
        return EmailExtractor()

    def test_extract_valid_email(self, extractor):
        """Test extraction of valid email address."""
        result = extractor.extract("Contact: john@example.com")
        assert result == "john@example.com"

    def test_extract_no_email_found(self, extractor):
        """Test when no email is present."""
        result = extractor.extract("No email address here")
        assert result == ""

    def test_extract_multiple_emails_returns_first(self, extractor):
        """Test multiple emails returns first match."""
        text = "Primary: john@test.com, Secondary: jane@test.com"
        result = extractor.extract(text)
        assert result == "john@test.com"

    @pytest.mark.parametrize("input_text,expected", [
        ("", ""),
        (None, ""),
        ("   ", ""),
    ])
    def test_extract_empty_or_invalid_input(self, extractor, input_text, expected):
        """Test extraction with empty or invalid input."""
        assert extractor.extract(input_text) == expected

    def test_extract_complex_email_format(self, extractor):
        """Test extraction of complex email formats."""
        text = "Email: user.name+tag@company.co.uk"
        result = extractor.extract(text)
        assert result == "user.name+tag@company.co.uk"