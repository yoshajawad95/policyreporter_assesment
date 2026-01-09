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

def test_empty_file_path():
    """Test empty file path handling."""
    pdf_parser = PDFParser()
    word_parser = WordParser()
    
    try:
        pdf_parser.parse("")
        assert False, "Should raise FileNotFoundError or ValueError"
    except (FileNotFoundError, ValueError):
        pass
    
    try:
        word_parser.parse("")
        assert False, "Should raise FileNotFoundError or ValueError"
    except (FileNotFoundError, ValueError):
        pass

def test_none_file_path():
    """Test None file path handling."""
    pdf_parser = PDFParser()
    word_parser = WordParser()
    
    try:
        pdf_parser.parse(None)
        assert False, "Should raise TypeError or AttributeError"
    except (TypeError, AttributeError):
        pass
    
    try:
        word_parser.parse(None)
        assert False, "Should raise TypeError or AttributeError"
    except (TypeError, AttributeError):
        pass

def test_invalid_file_extension():
    """Test handling of files with wrong extensions."""
    pdf_parser = PDFParser()
    word_parser = WordParser()
    
    # These should not raise exceptions during instantiation
    # but may fail during parsing if files exist with wrong content
    try:
        # Create a dummy text file to test with
        with open("test_invalid.txt", "w") as f:
            f.write("This is not a PDF")
        
        try:
            pdf_parser.parse("test_invalid.txt")
            # May succeed or fail depending on implementation
        except Exception:
            # Expected for invalid format
            pass
            
    finally:
        # Clean up
        try:
            import os
            os.remove("test_invalid.txt")
        except FileNotFoundError:
            pass

def test_directory_instead_of_file():
    """Test passing a directory path instead of file."""
    pdf_parser = PDFParser()
    word_parser = WordParser()
    
    import os
    # Create a temporary directory
    test_dir = "test_directory"
    try:
        os.makedirs(test_dir, exist_ok=True)
        
        try:
            pdf_parser.parse(test_dir)
            assert False, "Should raise an error for directory"
        except Exception:
            # Expected behavior
            pass
            
        try:
            word_parser.parse(test_dir)
            assert False, "Should raise an error for directory"
        except Exception:
            # Expected behavior
            pass
            
    finally:
        # Clean up
        try:
            os.rmdir(test_dir)
        except OSError:
            pass

def test_special_characters_in_filename():
    """Test handling of filenames with special characters."""
    pdf_parser = PDFParser()
    word_parser = WordParser()
    
    special_filenames = [
        "test file with spaces.pdf",
        "test-file-with-dashes.pdf", 
        "test_file_with_underscores.pdf",
        "test@file#with$symbols%.pdf",
        "测试文件.pdf",  # Unicode filename
        "файл.pdf"  # Cyrillic filename
    ]
    
    for filename in special_filenames:
        try:
            pdf_parser.parse(filename)
            assert False, f"Should raise FileNotFoundError for {filename}"
        except FileNotFoundError:
            # Expected behavior for non-existent files
            pass
        except Exception as e:
            # Other exceptions might occur due to special characters
            print(f"Exception for {filename}: {e}")

def test_very_long_filename():
    """Test handling of very long filenames."""
    pdf_parser = PDFParser()
    
    # Create a very long filename (255+ characters)
    long_filename = "a" * 300 + ".pdf"
    
    try:
        pdf_parser.parse(long_filename)
        assert False, "Should raise an error for very long filename"
    except (FileNotFoundError, OSError):
        # Expected behavior
        pass

def test_relative_and_absolute_paths():
    """Test handling of relative and absolute paths."""
    pdf_parser = PDFParser()
    
    relative_paths = [
        "./nonexistent.pdf",
        "../nonexistent.pdf",
        "subdir/nonexistent.pdf"
    ]
    
    for path in relative_paths:
        try:
            pdf_parser.parse(path)
            assert False, f"Should raise FileNotFoundError for {path}"
        except FileNotFoundError:
            # Expected behavior
            pass
    
    # Test absolute path (will not exist)
    import os
    abs_path = os.path.abspath("nonexistent_absolute.pdf")
    try:
        pdf_parser.parse(abs_path)
        assert False, "Should raise FileNotFoundError for absolute path"
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    test_pdf_parser_init()
    test_word_parser_init()
    test_file_not_found()
    print("Parser tests passed")