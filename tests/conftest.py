"""Shared test fixtures and configuration."""

import pytest
import os
from unittest.mock import Mock

@pytest.fixture(autouse=True)
def clear_environment():
    """Clear and restore environment variables for clean tests."""
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)

@pytest.fixture
def mock_gemini_env():
    """Provide mocked Gemini environment."""
    return {"GEMINI_API_KEY": "test_api_key_12345"}

@pytest.fixture
def sample_resume_text():
    """Sample resume text for testing."""
    return """John Doe
Software Engineer
john.doe@example.com

Skills: Python, Java, Docker, AWS
Experience with web development and cloud services."""

@pytest.fixture
def mock_extractors():
    """Mock extractors for framework testing."""
    return {
        "name": Mock(extract=Mock(return_value="Test User")),
        "email": Mock(extract=Mock(return_value="test@example.com")),
        "skills": Mock(extract=Mock(return_value=["python", "java"]))
    }