import pytest
from backend.models.resume_classifier import ResumeClassifier
from backend.models.skill_extractor import SkillExtractor

def test_resume_classifier():
    classifier = ResumeClassifier()
    resume = "Experienced Python developer with skills in Django and Flask."
    vacancy = "Looking for a Python Developer with experience in Django."
    
    result = classifier.classify(resume, vacancy)
    assert result is True  # Assuming the classifier returns True for a match

def test_skill_extractor():
    extractor = SkillExtractor()
    resume = "Skilled in Python, JavaScript, and React."
    
    skills = extractor.extract_skills(resume)
    expected_skills = {"Python", "JavaScript", "React"}
    
    assert skills == expected_skills  # Check if the extracted skills match the expected ones