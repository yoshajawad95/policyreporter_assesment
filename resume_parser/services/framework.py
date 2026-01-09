"""Main framework orchestration and facade."""

from typing import Dict, List
from pathlib import Path

from ..models.resume_data import ResumeData


class ResumeParserFramework:
    """Main framework for resume parsing."""
    
    def __init__(self, parsers: Dict[str, object], extractors: Dict[str, object]):
        self.parsers = parsers
        self.extractors = extractors
    
    def parse_resume(self, file_path: str) -> ResumeData:
        """Parse resume file and extract information."""
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension not in self.parsers:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        parser = self.parsers[file_extension]
        raw_text = parser.parse(file_path)
        
        extracted_data = {}
        for field_name, extractor in self.extractors.items():
            try:
                extracted_data[field_name] = extractor.extract(raw_text)
            except Exception:
                if field_name == "name":
                    extracted_data[field_name] = "Unknown"
                elif field_name == "email":
                    extracted_data[field_name] = ""
                elif field_name == "skills":
                    extracted_data[field_name] = []
        
        return ResumeData(
            name=extracted_data.get("name", "Unknown"),
            email=extracted_data.get("email", ""),
            skills=extracted_data.get("skills", [])
        )
    
    
    @property
    def supported_file_types(self) -> List[str]:
        return list(self.parsers.keys())