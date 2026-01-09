"""Name extraction using LLM."""

import os
import json
import google.generativeai as genai


class NameExtractor:
    """Extract candidate name using Gemini LLM."""
    
    EXTRACTION_PROMPT = """
Extract the candidate's name from this resume and return ONLY valid JSON in this exact format:

{{"name": "candidate_full_name"}}

Rules:
- Return ONLY JSON, no other text or explanation
- Use "Unknown" if no clear name is found
- Do not include titles (Mr., Mrs., Dr., etc.)
- Do not include contact information
- If multiple names appear, return the one most likely to be the candidate's name

Resume text:
{text}
"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(os.getenv("GEMINI_MODEL_NAME", "gemini-pro"))
    
    def extract(self, text: str) -> str:
        if not text:
            return "Unknown"
            
        try:
            prompt = self.EXTRACTION_PROMPT.format(text=text[:2000])
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                return "Unknown"
            
            # Clean response
            response_text = response.text.strip()
            if response_text.startswith("```"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            
            # Parse JSON
            json_data = json.loads(response_text)
            return json_data.get("name", "Unknown") if isinstance(json_data, dict) else "Unknown"
            
        except Exception:
            return "Unknown"