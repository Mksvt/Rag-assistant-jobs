from typing import List
import spacy

class SkillExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")  # Load the English NLP model

    def extract_skills(self, resume_text: str) -> List[str]:
        doc = self.nlp(resume_text)
        skills = set()

        # Define a list of common skills (this can be expanded)
        common_skills = {"Python", "Java", "JavaScript", "React", "Node.js", "SQL", "Docker", "Machine Learning", "Data Analysis"}

        for token in doc:
            if token.text in common_skills:
                skills.add(token.text)

        return list(skills)