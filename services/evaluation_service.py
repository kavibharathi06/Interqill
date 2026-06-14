from typing import List, Dict, Any
from evaluation.answer_evaluator import AnswerEvaluator

class EvaluationService:
    def __init__(self):
        """Initializes the service and loads the answer evaluator."""
        self.evaluator = AnswerEvaluator()

    def evaluate_response(self, candidate_answer: str, expected_answer: str) -> Dict[str, Any]:
        """Evaluates a single answer using the NLP evaluator."""
        return self.evaluator.evaluate_answer(candidate_answer, expected_answer)

    def aggregate_results(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregates individual question evaluations into a comprehensive final report.
        
        Args:
            responses (List[Dict[str, Any]]): List of dicts, each containing:
                - 'skill': str
                - 'question': str
                - 'expected_answer': str
                - 'answer': str
                - 'evaluation': Dict (from evaluate_answer)
                
        Returns:
            Dict[str, Any]: Final report summary.
        """
        if not responses:
            return {
                "overall_score": 0.0,
                "technical_score": 0.0,
                "communication_score": 0.0,
                "skill_scores": {},
                "weak_areas": [],
                "strong_areas": [],
                "recommendations": [],
                "achievements": [],
                "responses": []
            }

        total_questions = len(responses)
        sum_tech = 0.0
        sum_comm = 0.0
        sum_final = 0.0

        # Group by skill
        skill_groups = {}
        for resp in responses:
            skill = resp["skill"]
            eval_res = resp["evaluation"]
            
            sum_tech += eval_res["technical_score"]
            sum_comm += eval_res["communication_score"]
            sum_final += eval_res["final_score"]

            if skill not in skill_groups:
                skill_groups[skill] = []
            skill_groups[skill].append(eval_res["final_score"])

        # Calculate averages
        avg_tech = sum_tech / total_questions
        avg_comm = sum_comm / total_questions
        avg_final = sum_final / total_questions

        # Calculate skill-by-skill averages
        skill_scores = {}
        weak_areas = []
        strong_areas = []
        for skill, scores in skill_groups.items():
            avg_skill_score = sum(scores) / len(scores)
            skill_scores[skill] = round(avg_skill_score, 1)
            
            if avg_skill_score < 70.0:
                weak_areas.append(skill)
            else:
                strong_areas.append(skill)

        # Generate achievements
        achievements = self._generate_achievements(responses, avg_tech, avg_comm)

        # Generate recommendations and gap analysis
        recommendations = self._generate_recommendations(weak_areas, responses)

        return {
            "overall_score": round(avg_final, 1),
            "technical_score": round(avg_tech, 1),
            "communication_score": round(avg_comm, 1),
            "skill_scores": skill_scores,
            "weak_areas": weak_areas,
            "strong_areas": strong_areas,
            "recommendations": recommendations,
            "achievements": achievements,
            "responses": responses
        }

    def _generate_achievements(self, responses: List[Dict[str, Any]], avg_tech: float, avg_comm: float) -> List[Dict[str, str]]:
        achievements = []
        
        # 1. Technical excellence
        if avg_tech >= 85.0:
            achievements.append({
                "title": "Technical Maestro",
                "desc": "Demonstrated exceptionally deep technical understanding with rich, keyword-accurate answers.",
                "icon": "🏆"
            })
            
        # 2. Communication excellence
        if avg_comm >= 85.0:
            achievements.append({
                "title": "Slick Communicator",
                "desc": "Answers were highly articulate, grammatically complete, and lexically rich.",
                "icon": "💬"
            })
            
        # 3. Conciseness / Length
        avg_len_score = sum(r["evaluation"]["length_score"] for r in responses) / len(responses)
        if avg_len_score >= 90.0:
            achievements.append({
                "title": "Precision Speaker",
                "desc": "Answers were well-structured and optimal in length—no fluff, pure substance.",
                "icon": "🎯"
            })
            
        # 4. Completion
        if len(responses) >= 6:
            achievements.append({
                "title": "Interview Marathoner",
                "desc": "Completed a comprehensive multiskill technical review session.",
                "icon": "🏃‍♂️"
            })

        # Add fallback basic achievement
        if not achievements:
            achievements.append({
                "title": "Platform Starter",
                "desc": "Completed your first self-guided practice session.",
                "icon": "✨"
            })
            
        return achievements

    def _generate_recommendations(self, weak_areas: List[str], responses: List[Dict[str, Any]]) -> List[str]:
        recommendations = []
        
        if not weak_areas:
            recommendations.append("Excellent performance! Continue practicing at higher difficulty levels to stay sharp.")
            return recommendations

        for skill in weak_areas:
            recommendations.append(
                f"Revise core theoretical concepts for **{skill}**. Re-study the expected terms you missed during practice."
            )
            
        # Check for specific grammar/communication suggestions
        low_grammar = any(r["evaluation"]["grammar_score"] < 80 for r in responses)
        if low_grammar:
            recommendations.append(
                "Focus on sentence structure: start answers with capital letters, end with periods, and use active verbs."
            )
            
        return recommendations
