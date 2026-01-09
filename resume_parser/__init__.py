"""Resume Parser Framework - A simple resume parsing library."""

__version__ = "1.0.0"

from .services.framework import ResumeParserFramework
from .parsers.pdf_parser import PDFParser
from .parsers.word_parser import WordParser
from .extractors.name_extractor import NameExtractor
from .extractors.email_extractor import EmailExtractor
from .extractors.skills_extractor import SkillsExtractor
from .models.resume_data import ResumeData

__all__ = [
    "ResumeParserFramework",
    "PDFParser",
    "WordParser",
    "NameExtractor",
    "EmailExtractor",
    "SkillsExtractor",
    "ResumeData",
]