from typing import List, Dict, Any, Optional
from questions.question_generator import QuestionGenerator

class QuestionService:
    def __init__(self, questions_csv_path: str = "data/questions.csv"):
        """Initializes the service and loads the question generator."""
        self.generator = QuestionGenerator(questions_csv_path)

    def prepare_interview_questions(self, skills: List[str], resume_text: str = "", questions_per_skill: int = 2) -> List[Dict[str, Any]]:
        """
        Retrieves, ranks, and flattens a list of questions to ask the candidate.
        
        Args:
            skills (List[str]): Extracted skills.
            resume_text (str): Resume text for relevance ranking.
            questions_per_skill (int): Number of questions to pull for each skill.
            
        Returns:
            List[Dict[str, Any]]: Ordered list of question dicts.
        """
        # If the candidate has no detected skills, select a default set of programming skills
        if not skills:
            skills = ["Python", "SQL", "JavaScript"]

        grouped_questions = self.generator.get_questions_for_skills(
            skills=skills,
            resume_text=resume_text,
            limit_per_skill=questions_per_skill
        )

        flat_questions = []
        # We alternate or group them nicely. Grouping by skill is clean so candidates complete one category at a time
        for skill in skills:
            if skill in grouped_questions:
                for q in grouped_questions[skill]:
                    flat_questions.append(q)

        return flat_questions
