import os
import re
import pandas as pd
from typing import Set, List, Dict, Tuple

# Core 24 skills targeted by InterQill
CORE_SKILLS = {
    "Python": ["python", "py"],
    "Java": ["java"],
    "SQL": ["sql", "structured query language"],
    "Machine Learning": ["machine learning", "ml", "supervised learning", "unsupervised learning"],
    "Deep Learning": ["deep learning", "dl", "neural network", "neural networks"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "JavaScript": ["javascript", "js", "es6"],
    "React": ["react", "react.js", "reactjs"],
    "NodeJS": ["node", "nodejs", "node.js"],
    "Django": ["django"],
    "Flask": ["flask"],
    "TensorFlow": ["tensorflow", "tf"],
    "PyTorch": ["pytorch"],
    "NumPy": ["numpy"],
    "Pandas": ["pandas"],
    "Streamlit": ["streamlit"],
    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "NLP": ["nlp", "natural language processing"],
    "MySQL": ["mysql"],
    "MongoDB": ["mongodb", "mongo"],
    "Data Science": ["data science", "ds"],
    "Data Analysis": ["data analysis", "da", "analytics"]
}

# Cache for loaded real-world vocabulary and association mappings
_skills_vocab = None
_association_rules = None

def load_real_world_skills(skills_csv_path="data/skills.csv") -> Tuple[Set[str], Dict[str, List[str]]]:
    """
    Loads the Skill2Vec dataset to build:
    1. A set of valid tech skills in the industry.
    2. An association mapping of which skills commonly co-occur.
    """
    global _skills_vocab, _association_rules
    if _skills_vocab is not None:
        return _skills_vocab, _association_rules
        
    vocab = set()
    associations = {}
    
    # Add our core skills to vocabulary first
    for skill, aliases in CORE_SKILLS.items():
        vocab.add(skill.lower())
        for alias in aliases:
            vocab.add(alias.lower())
            
    if not os.path.exists(skills_csv_path):
        _skills_vocab = vocab
        _association_rules = associations
        return vocab, associations
        
    try:
        # Load a sample/subset of the dataset for speed and efficiency
        df = pd.read_csv(skills_csv_path, low_memory=False, nrows=5000)
        
        # Flatten columns and cells to build vocabulary
        for col in df.columns:
            if not col.startswith('Unnamed:'):
                vocab.add(col.strip().lower())
                
        # Sample associations from the rows
        # For each row, we treat it as a group of associated skills
        for _, row in df.iterrows():
            skills_in_row = [str(val).strip().lower() for val in row.values if pd.notnull(val) and len(str(val)) > 1]
            for sk in skills_in_row:
                if sk not in associations:
                    associations[sk] = {}
                for other_sk in skills_in_row:
                    if other_sk != sk:
                        associations[sk][other_sk] = associations[sk].get(other_sk, 0) + 1
                        
        # Prune associations to keep only the top 5 co-occurring skills
        clean_associations = {}
        for sk, related in associations.items():
            sorted_related = sorted(related.items(), key=lambda x: x[1], reverse=True)[:5]
            clean_associations[sk] = [r[0] for r in sorted_related]
            
        _skills_vocab = vocab
        _association_rules = clean_associations
    except Exception as e:
        print(f"Error loading real-world skills dataset: {e}")
        _skills_vocab = vocab
        _association_rules = associations
        
    return _skills_vocab, _association_rules

def extract_skills_from_text(text: str) -> Dict[str, List[str]]:
    """
    Extracts core and other skills from raw text using rule-based matching.
    
    Args:
        text (str): Raw extracted resume text.
        
    Returns:
        Dict: A dictionary containing:
            - 'core': List of standard 24 core skills matched.
            - 'other': List of other industry skills matched.
    """
    text_lower = text.lower()
    extracted_core = []
    extracted_other = []
    
    # 1. Core skills dictionary matching
    for skill, aliases in CORE_SKILLS.items():
        matched = False
        for alias in aliases:
            # Word boundary matching to avoid matching 'java' in 'javascript' or 'py' in 'copy'
            # Specifying special boundary matching for C++, JS, .NET
            escaped_alias = re.escape(alias)
            # Custom boundary for cases like React.js or node.js
            pattern = rf"\b{escaped_alias}\b"
            if re.search(pattern, text_lower):
                matched = True
                break
        if matched:
            extracted_core.append(skill)
            
    # 2. Extract other skills using real-world vocabulary
    vocab, _ = load_real_world_skills()
    
    # Find words or phrases from the vocabulary that appear in the resume
    # We do a fast regex check or token match. For efficiency, we tokenize the text
    # and check if 1-gram or 2-gram tokens exist in the vocabulary
    words = re.findall(r'[a-zA-Z0-9+#]+', text_lower)
    
    # Check single words
    matched_set = set()
    for word in words:
        if word in vocab and word not in matched_set:
            # Exclude core skills aliases so we don't duplicate
            is_core_alias = False
            for core_aliases in CORE_SKILLS.values():
                if word in core_aliases:
                    is_core_alias = True
                    break
            if not is_core_alias and len(word) > 2:
                matched_set.add(word)
                
    # Check bi-grams (2-word phrases like 'machine learning', 'data analysis')
    for i in range(len(words) - 1):
        bigram = f"{words[i]} {words[i+1]}"
        if bigram in vocab and bigram not in matched_set:
            is_core_alias = False
            for core_aliases in CORE_SKILLS.values():
                if bigram in core_aliases:
                    is_core_alias = True
                    break
            if not is_core_alias:
                matched_set.add(bigram)
                
    extracted_other = sorted(list(matched_set))[:10]  # Limit to top 10 other skills
    
    return {
        "core": sorted(extracted_core),
        "other": extracted_other
    }

def get_skill_gap_recommendations(candidate_skills: List[str]) -> Dict[str, List[str]]:
    """
    Compares candidate skills against the real-world co-occurrence rules.
    If a candidate has 'React', we check what they might be missing based on typical
    industry expectations (e.g. Node.js, JavaScript, HTML, CSS).
    """
    _, associations = load_real_world_skills()
    recommendations = {}
    
    for skill in candidate_skills:
        skill_lower = skill.lower()
        if skill_lower in associations:
            # Get real-world associated skills
            associated = associations[skill_lower]
            # Find which ones the candidate does not have
            missing = []
            for item in associated:
                # Find matching standard core name if possible
                standard_name = item.title()
                for core_name in CORE_SKILLS.keys():
                    if core_name.lower() == item.lower():
                        standard_name = core_name
                        break
                
                # Check if candidate has it
                has_skill = False
                for c_skill in candidate_skills:
                    if c_skill.lower() == item.lower():
                        has_skill = True
                        break
                        
                if not has_skill:
                    missing.append(standard_name)
            
            if missing:
                recommendations[skill] = missing[:3]  # Suggest top 3 missing related skills
                
    return recommendations
