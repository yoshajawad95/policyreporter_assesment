"""Simple resume parser runner."""

import sys
import os
from dotenv import load_dotenv

sys.path.insert(0, '.')
load_dotenv()

# Configuration
INPUT_FILE = "path to your input file"
OUTPUT_FILE = "results.json"

def main():
    """Parse resume and save results."""
    from resume_parser import (
        ResumeParserFramework,
        PDFParser,
        WordParser,
        NameExtractor,
        EmailExtractor,
        SkillsExtractor,
    )
    
    # Basic validation
    if not os.path.exists(INPUT_FILE):
        print(f"File not found: {INPUT_FILE}")
        return
    
    if not os.getenv("GEMINI_API_KEY"):
        print("GEMINI_API_KEY not found")
        return
    
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
    result = framework.parse_resume(INPUT_FILE)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(result.to_json())
    
    print(f"Parsed {result.name} - saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()