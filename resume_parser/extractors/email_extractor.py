"""Email extraction using regex."""

import re


class EmailExtractor:
    """Extract email addresses using regex patterns."""
    
    def extract(self, text: str) -> str:
        if not text:
            return ""
        
        # Email pattern that supports Unicode characters
        email_pattern = r'\b[\w._%+-]+@[\w.-]+\.[A-Za-z]{2,}\b'
        matches = re.findall(email_pattern, text, re.UNICODE)
        
        return matches[0] if matches else ""