"""PDF file parser implementation."""

import pdfplumber
import os
import logging

logger = logging.getLogger(__name__)


class PDFParser:
    """Parser for PDF files using pdfplumber."""
    
    def parse(self, file_path: str) -> str:
        """Extract text from a PDF file."""
        logger.info(f"Starting PDF parsing for: {file_path}")
        
        if not os.path.exists(file_path):
            logger.error(f"PDF file not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")
        
        text_content = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                logger.debug(f"PDF opened successfully, processing {len(pdf.pages)} pages")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
                        logger.debug(f"Extracted text from page {page_num}")
                    else:
                        logger.warning(f"No text found on page {page_num}")
        
            if not text_content:
                logger.error(f"No text content could be extracted from PDF: {file_path}")
                raise ValueError("No text content could be extracted from PDF")
            
            total_chars = len("\n\n".join(text_content))
            logger.info(f"Successfully extracted {total_chars} characters from {len(text_content)} pages")
            
            return "\n\n".join(text_content)
            
        except Exception as e:
            if "No text content could be extracted" in str(e):
                raise  # Re-raise our custom error
            logger.error(f"Error parsing PDF {file_path}: {e}")
            raise