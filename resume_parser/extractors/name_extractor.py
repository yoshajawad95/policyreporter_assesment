"""Name extraction using LLM."""

import os
import json
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)


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
            logger.error("GEMINI_API_KEY not found in environment")
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        logger.debug("Configuring Gemini API for name extraction")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(os.getenv("GEMINI_MODEL_NAME", "gemini-pro"))
    
    def extract(self, text: str) -> str:
        if not text:
            logger.warning("Empty text provided to name extractor")
            return "Unknown"
            
        try:
            prompt = self.EXTRACTION_PROMPT.format(text=text[:2000])
            logger.debug("Sending name extraction request to Gemini API")
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                logger.warning("Empty response from Gemini API for name extraction")
                return "Unknown"
            
            # Clean response
            response_text = response.text.strip()
            if response_text.startswith("```"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            
            # Parse JSON
            json_data = json.loads(response_text)
            extracted_name = json_data.get("name", "Unknown") if isinstance(json_data, dict) else "Unknown"
            
            if extracted_name != "Unknown":
                logger.info(f"Successfully extracted name: {extracted_name}")
            else:
                logger.warning("Could not extract valid name from response")
            
            return extracted_name
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response from Gemini API: {e}")
            return "Unknown"
        except Exception as e:
            logger.error(f"Name extraction failed: {e}")
            return "Unknown"