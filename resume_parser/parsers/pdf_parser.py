"""PDF file parser implementation."""

import pdfplumber
import os


class PDFParser:
    """Parser for PDF files using pdfplumber."""
    
    def parse(self, file_path: str) -> str:
        """Extract text from a PDF file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        text_content = []
        
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
        
        if not text_content:
            raise ValueError("No text content could be extracted from PDF")
        
        return "\n\n".join(text_content)