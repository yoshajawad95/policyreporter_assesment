"""Main framework orchestration and facade."""

from typing import Dict, List
from pathlib import Path
import logging

from ..models.resume_data import ResumeData

logger = logging.getLogger(__name__)


class ResumeParserFramework:
    """Main framework for resume parsing."""
    
    def __init__(self, parsers: Dict[str, object], extractors: Dict[str, object]):
        self.parsers = parsers
        self.extractors = extractors
        logger.info(f"Framework initialized with {len(parsers)} parsers and {len(extractors)} extractors")
    
    def parse_resume(self, file_path: str) -> ResumeData:
        """Parse resume file and extract information."""
        logger.info(f"Starting resume parsing for: {file_path}")
        
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension not in self.parsers:
            logger.error(f"Unsupported file type: {file_extension}. Supported: {list(self.parsers.keys())}")
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        # Parse file to extract raw text
        parser = self.parsers[file_extension]
        logger.debug(f"Using {parser.__class__.__name__} to parse file")
        raw_text = parser.parse(file_path)
        
        # Extract structured data using extractors
        extracted_data = {}
        for field_name, extractor in self.extractors.items():
            logger.debug(f"Running {extractor.__class__.__name__} for {field_name}")
            try:
                extracted_data[field_name] = extractor.extract(raw_text)
            except Exception as e:
                logger.error(f"Extractor {field_name} failed: {e}")
                # Provide fallback values
                if field_name == "name":
                    extracted_data[field_name] = "Unknown"
                elif field_name == "email":
                    extracted_data[field_name] = ""
                elif field_name == "skills":
                    extracted_data[field_name] = []
        
        result = ResumeData(
            name=extracted_data.get("name", "Unknown"),
            email=extracted_data.get("email", ""),
            skills=extracted_data.get("skills", [])
        )
        
        skills_count = len(result.skills) if result.skills is not None else 0
        logger.info(f"Successfully parsed resume: {result.name}, {result.email}, {skills_count} skills")
        return result
    
    
    @property
    def supported_file_types(self) -> List[str]:
        return list(self.parsers.keys())