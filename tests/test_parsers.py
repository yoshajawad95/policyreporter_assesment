"""Tests for file parsers."""

import sys
sys.path.insert(0, '.')

from resume_parser.parsers.pdf_parser import PDFParser
from resume_parser.parsers.word_parser import WordParser

def test_pdf_parser_init():
    """Test PDF parser initialization."""
    parser = PDFParser()
    assert parser is not None

def test_word_parser_init():
    """Test Word parser initialization."""
    parser = WordParser()
    assert parser is not None

def test_file_not_found():
    """Test file not found handling."""
    pdf_parser = PDFParser()
    word_parser = WordParser()
    
    try:
        pdf_parser.parse("nonexistent.pdf")
        assert False, "Should raise FileNotFoundError"
    except FileNotFoundError:
        pass
    
    try:
        word_parser.parse("nonexistent.docx")
        assert False, "Should raise FileNotFoundError"
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    test_pdf_parser_init()
    test_word_parser_init()
    test_file_not_found()
    print("Parser tests passed")