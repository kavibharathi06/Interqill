import unittest
import sys
import os

# Adjust paths to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resume.preprocess import preprocess_text, get_normalized_text
from resume.skill_extract import extract_skills_from_text, load_real_world_skills
from evaluation.answer_evaluator import AnswerEvaluator
from questions.question_generator import QuestionGenerator

class TestNLP(unittest.TestCase):
    def setUp(self):
        # Initialize components
        self.evaluator = AnswerEvaluator()
        self.generator = QuestionGenerator()

    def test_text_preprocessing(self):
        """Tests that text preprocessing cleans, tokenizes, and lemmatizes correctly."""
        text = "This is a simple TEST sentence for Python programming!"
        tokens = preprocess_text(text)
        
        # Verify tokens
        self.assertIn("simple", tokens)
        self.assertIn("test", tokens)
        self.assertIn("python", tokens)
        
        # Stop words like "this", "is", "a", "for" should be removed
        self.assertNotIn("this", tokens)
        self.assertNotIn("is", tokens)
        
        normalized = get_normalized_text(text)
        self.assertTrue(isinstance(normalized, str))
        self.assertIn("simple test sentence python programming", normalized)

    def test_skill_extraction(self):
        """Tests that skills are extracted correctly using dictionary matching."""
        resume = "Experienced software engineer with knowledge of Python, Django, React, and SQL database systems."
        skills = extract_skills_from_text(resume)
        
        core_skills = skills["core"]
        
        # Verify matched skills
        self.assertIn("Python", core_skills)
        self.assertIn("Django", core_skills)
        self.assertIn("React", core_skills)
        self.assertIn("SQL", core_skills)
        
        # Verify that unmatched skills are not returned
        self.assertNotIn("TensorFlow", core_skills)

    def test_answer_evaluator(self):
        """Tests that technical and communication scoring work correctly."""
        expected = "Lists are mutable and defined with square brackets, while tuples are immutable and defined with parentheses."
        
        # 1. Close/Exact match answer
        good_answer = "Lists are mutable sequences using square brackets, whereas tuples are immutable using parentheses."
        good_result = self.evaluator.evaluate_answer(good_answer, expected)
        
        # 2. Poor answer
        bad_answer = "Python has variables and functions."
        bad_result = self.evaluator.evaluate_answer(bad_answer, expected)
        
        # Good answer should score significantly higher than the bad answer
        self.assertGreater(good_result["technical_score"], bad_result["technical_score"])
        self.assertGreater(good_result["final_score"], bad_result["final_score"])
        
        # Communication scores should evaluate properly
        self.assertTrue(0.0 <= good_result["communication_score"] <= 100.0)
        self.assertTrue(good_result["grammar_score"] > 0)

    def test_question_generator(self):
        """Tests that questions are retrieved and ranked correctly."""
        skills = ["Python", "SQL"]
        questions = self.generator.get_questions_for_skills(skills, resume_text="Django Python developer")
        
        # Check that we retrieved questions
        self.assertIn("Python", questions)
        self.assertIn("SQL", questions)
        
        # Verify columns of generated questions
        python_qs = questions["Python"]
        self.assertGreater(len(python_qs), 0)
        
        first_q = python_qs[0]
        self.assertIn("skill", first_q)
        self.assertIn("question", first_q)
        self.assertIn("expected_answer", first_q)
        self.assertIn("difficulty", first_q)

if __name__ == "__main__":
    unittest.main()
