"""Skills extraction using LLM with adaptive section detection."""

import os
import json
import logging
from typing import List
import google.generativeai as genai

logger = logging.getLogger(__name__)


class SkillsExtractor:
    """Extract skills using LLM from entire resume document."""
    
    EXTRACTION_PROMPT = """
You are an intelligent resume parser. Analyze this entire resume to extract all skills, competencies, tools, technologies, and abilities mentioned throughout the document.

Your task:
Scan the ENTIRE resume (all sections) and extract any skills, tools, technologies, or competencies mentioned anywhere in the document.

Return ONLY valid JSON in this exact format:
{{"skills": ["skill1", "skill2", "skill3", ...]}}

EXTRACTION GUIDELINES:

COMPREHENSIVE SCANNING:
- Extract skills from ALL sections: skills section, work experience, education, projects, certifications, etc.
- Include technical skills (programming languages, software, tools)
- Include soft skills (communication, leadership, management)
- Include domain-specific skills and methodologies
- Include certifications and qualifications that represent skills

INTELLIGENT EXTRACTION:
- Extract the core skill/ability terms
- Remove descriptive words like "strong", "excellent", "experience in", "ability to"
- Extract both general skills and specific tools/technologies mentioned
- Use lowercase and normalize similar terms
- If a skill is mentioned multiple times, include it only once

WHAT TO INCLUDE:
- Programming languages and frameworks
- Software applications and tools
- Technical methodologies and practices
- Industry-specific skills
- Soft skills and competencies
- Relevant certifications and qualifications

WHAT TO EXCLUDE:
- Job titles and company names
- Educational degrees (unless they represent specific skills)
- Years of experience or proficiency levels
- Personal information (names, addresses, etc.)

Extract skills from anywhere they appear in the resume - don't limit to just dedicated skills sections.

Resume text:
{text}
"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY not found in environment")
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        logger.debug("Configuring Gemini API for skills extraction")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(os.getenv("GEMINI_MODEL_NAME", "gemini-pro"))
    
    def extract(self, text: str) -> List[str]:
        if not text:
            logger.warning("Empty text provided to skills extractor")
            return []
            
        try:
            prompt = self.EXTRACTION_PROMPT.format(text=text[:6000])
            logger.debug("Sending skills extraction request to Gemini API")
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                logger.warning("Empty response from Gemini API for skills extraction")
                return []
            
            # Clean response
            response_text = response.text.strip()
            if response_text.startswith("```"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            
            # Parse JSON
            json_data = json.loads(response_text)
            
            if isinstance(json_data, dict) and "skills" in json_data:
                skills_list = json_data["skills"]
                if isinstance(skills_list, list):
                    # Clean and validate skills
                    cleaned_skills = []
                    for skill in skills_list:
                        if isinstance(skill, str) and skill.strip():
                            cleaned_skill = skill.strip().lower()
                            if (cleaned_skill not in cleaned_skills and 
                                len(cleaned_skill) > 1 and 
                                len(cleaned_skill) < 50):
                                cleaned_skills.append(cleaned_skill)
                    
                    logger.info(f"Successfully extracted {len(cleaned_skills)} skills")
                    return sorted(cleaned_skills)
                else:
                    logger.warning("Skills data is not a list in API response")
            else:
                logger.warning("Missing 'skills' key in API response")
            
            return []
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response from Gemini API: {e}")
            return []
        except Exception as e:
            logger.error(f"Skills extraction failed: {e}")
            return []