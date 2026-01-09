"""Tests for data models."""

import sys
sys.path.insert(0, '.')

from resume_parser.models.resume_data import ResumeData

def test_resume_data_creation():
    """Test ResumeData creation."""
    data = ResumeData("John Doe", "john@test.com", ["python", "java"])
    
    assert data.name == "John Doe"
    assert data.email == "john@test.com"
    assert "python" in data.skills
    assert len(data.skills) == 2

def test_to_dict():
    """Test conversion to dictionary."""
    data = ResumeData("Jane", "jane@test.com", ["react"])
    result = data.to_dict()
    
    assert isinstance(result, dict)
    assert result["name"] == "Jane"
    assert result["email"] == "jane@test.com"
    assert result["skills"] == ["react"]

def test_to_json():
    """Test JSON serialization."""
    data = ResumeData("Bob", "bob@test.com", ["go"])
    json_str = data.to_json()
    
    assert isinstance(json_str, str)
    assert "Bob" in json_str
    assert "bob@test.com" in json_str

if __name__ == "__main__":
    test_resume_data_creation()
    test_to_dict()
    test_to_json()
    print("Model tests passed")