"""Data models for resume information."""

from dataclasses import dataclass, asdict
from typing import List
import json


@dataclass
class ResumeData:
    """Structured resume information."""
    name: str
    email: str
    skills: List[str]
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)
    
