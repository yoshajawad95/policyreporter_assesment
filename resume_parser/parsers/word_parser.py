"""Word document parser implementation."""

import os
from docx import Document


class WordParser:
    """Parser for Word documents using python-docx."""
    
    def parse(self, file_path: str) -> str:
        """Extract text from a Word document."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        doc = Document(file_path)
        text_content = []
        
        # Extract from paragraphs
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_content.append(paragraph.text.strip())
        
        # Extract from tables
        for table in doc.tables:
            for row in table.rows:
                row_text = []
                for cell in row.cells:
                    if cell.text.strip():
                        row_text.append(cell.text.strip())
                if row_text:
                    text_content.append(" | ".join(row_text))
        
        if not text_content:
            raise ValueError("No text content could be extracted from Word document")
        
        return "\n".join(text_content)