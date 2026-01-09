"""Simple resume parser runner."""

import sys
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, '.')
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('resume_parser.log')
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Parse resume and save results."""
    # Get input file from user
    input_file = input("Enter resume file path: ").strip()
    
    # Remove quotes if user added them
    if input_file.startswith('"') and input_file.endswith('"'):
        input_file = input_file[1:-1]
    
    # Basic validation
    if not input_file:
        logger.error("No file path provided")
        print("No file path provided")
        return
    
    if not os.path.exists(input_file):
        logger.error(f"File not found: {input_file}")
        print(f"File not found: {input_file}")
        return
    
    # Check file type
    file_ext = Path(input_file).suffix.lower()
    if file_ext not in ['.pdf', '.docx', '.doc']:
        logger.error(f"Unsupported file type: {file_ext}")
        print(f"Unsupported file type: {file_ext}")
        print("Supported formats: .pdf, .docx, .doc")
        return
    
    if not os.getenv("GEMINI_API_KEY"):
        logger.error("GEMINI_API_KEY environment variable not found")
        print("GEMINI_API_KEY not found")
        return
    
    from resume_parser import (
        ResumeParserFramework,
        PDFParser,
        WordParser,
        NameExtractor,
        EmailExtractor,
        SkillsExtractor,
    )
    
    # Initialize framework
    parsers = {
        ".pdf": PDFParser(),
        ".docx": WordParser(),
        ".doc": WordParser(),
    }
    
    extractors = {
        "name": NameExtractor(),
        "email": EmailExtractor(),
        "skills": SkillsExtractor(),
    }
    
    framework = ResumeParserFramework(parsers, extractors)
    
    # Parse and save
    logger.info(f"Starting resume parsing process for: {input_file}")
    try:
        result = framework.parse_resume(input_file)
        
        output_file = "results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.to_json())
        
        logger.info(f"Resume parsing completed successfully. Output saved to: {output_file}")
        print(f"Parsed {result.name} - saved to {output_file}")
        
    except Exception as e:
        logger.error(f"Resume parsing failed: {e}")
        print(f"Error: {e}")
        return

if __name__ == "__main__":
    main()