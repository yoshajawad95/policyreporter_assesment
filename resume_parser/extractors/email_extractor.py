"""Email extraction using regex."""

import re


class EmailExtractor:
    """Extract email addresses using regex patterns."""
    
    def extract(self, text: str) -> str:
        if not text:
            return ""
        
        # Simple email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        
        return matches[0] if matches else ""