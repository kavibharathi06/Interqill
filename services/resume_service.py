import os
import re
from typing import Dict, Any, List
from resume.extract_text import extract_text_from_pdf
from resume.skill_extract import extract_skills_from_text, get_skill_gap_recommendations

class ResumeService:
    def __init__(self):
        pass

    def process_resume(self, pdf_file) -> Dict[str, Any]:
        """
        Extracts text, parses contact info, and extracts skills from a resume.
        
        Args:
            pdf_file: File path, file-like object, or bytes.
            
        Returns:
            Dict[str, Any]: Extracted metadata, core skills, other skills, and recommendations.
        """
        raw_text = extract_text_from_pdf(pdf_file)
        if not raw_text:
            return {
                "name": "Unknown Candidate",
                "email": "Not Found",
                "phone": "Not Found",
                "skills": [],
                "other_skills": [],
                "recommendations": {},
                "raw_text": ""
            }

        # Extract name, email, and phone using rule-based regex
        email = self._extract_email(raw_text)
        phone = self._extract_phone(raw_text)
        name = self._extract_name(raw_text)

        # Extract skills
        skills_dict = extract_skills_from_text(raw_text)
        core_skills = skills_dict.get("core", [])
        other_skills = skills_dict.get("other", [])

        # Get recommendations / gaps based on industry associations
        recommendations = get_skill_gap_recommendations(core_skills)

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "skills": core_skills,
            "other_skills": other_skills,
            "recommendations": recommendations,
            "raw_text": raw_text
        }

    def _extract_email(self, text: str) -> str:
        pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        match = re.search(pattern, text)
        return match.group(0) if match else "Not Found"

    def _extract_phone(self, text: str) -> str:
        # Match standard phone numbers (e.g. +1-234-567-8900, 234-567-8900, +91 99999 99999)
        pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        match = re.search(pattern, text)
        return match.group(0) if match else "Not Found"

    def _extract_name(self, text: str) -> str:
        # Classical NLP rule: name is often in the first two non-empty lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if not lines:
            return "Unknown Candidate"
            
        for line in lines[:3]:
            # Clean name format validation: usually 2-3 words, no numbers, no special symbols
            words = line.split()
            if 2 <= len(words) <= 4 and all(w.isalpha() for w in words):
                # Avoid matching sections like "Resume", "Curriculum Vitae", "Page 1"
                if line.lower() not in ["resume", "curriculum vitae", "contact info", "summary"]:
                    return line
                    
        return "Candidate Profile"
