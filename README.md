## Features

- **Pluggable Architecture**: Easy to extend with new parsers and extractors
- **Multiple File Formats**: PDF and Word Document (.docx) support
- **Field-Specific Strategies**: LLM-based and regex-based extraction
- **Production Ready**: Comprehensive error handling, logging, and testing

## Requirements

- Python 3.8+
- Google Gemini API key (free tier available)

## Installation

1. Clone the repository
2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   # Or create a .env file with GEMINI_API_KEY=your_api_key_here
   ```

## Quick Start

### Command Line Usage
```bash
# Edit run_parser.py to set your input and output paths
python run_parser.py
```

### Programmatic Usage
```python
from resume_parser import (
    ResumeParserFramework,
    PDFParser,
    WordParser,
    NameExtractor,
    EmailExtractor,
    SkillsExtractor,
)

# Initialize framework
framework = ResumeParserFramework(
    parsers={
        ".pdf": PDFParser(),
        ".docx": WordParser(),
    },
    extractors={
        "name": NameExtractor(),      # LLM-based
        "email": EmailExtractor(),     # Regex-based
        "skills": SkillsExtractor(),   # LLM-based
    }
)

# Parse resume
result = framework.parse_resume("resume.pdf")
print(result.to_json())
```

## Architecture

### Core Components

- **FileParser** (Abstract Base Class)
  - `PDFParser` - PDF file parsing
  - `WordParser` - Word document parsing

- **Field Extractors**
  - `NameExtractor` - LLM-based name extraction using Google Gemini
  - `EmailExtractor` - Regex-based email extraction
  - `SkillsExtractor` - LLM-based comprehensive skills extraction using Google Gemini

- **ResumeData** - Data class encapsulating extracted fields
- **ResumeParserFramework** - Main framework providing `parse_resume()` method

## Output Format

```json
{
  "name": "string",
  "email": "string",
  "skills": ["skill1", "skill2", "skill3"]
}
```

## Usage

Simply update the file paths in `run_parser.py` and run:
```python
python run_parser.py
```

## Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

## API Key Setup

1. Copy `.env.example` to `.env`
2. Add your API key to the `.env` file