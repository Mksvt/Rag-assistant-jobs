"""
Service layer for vacancy-related logic.

This module contains the business logic for handling vacancy-related operations.
"""

from pathlib import Path
from backend.utils.resume_parser import analyze_resume
from backend.services.vacancy_scraper import VacancyScraper


# Initialize vacancy scraper
vacancy_scraper = VacancyScraper()


def calculate_match_score(resume_data, vacancy):
    """
    Calculate match score between resume and vacancy.

    Args:
        resume_data (dict): Parsed resume data with skills and experience
        vacancy (dict): Vacancy information with requirements

    Returns:
        float: Match score from 0 to 100
    """
    if "error" in resume_data:
        return 0.0

    resume_skills = set(skill.lower() for skill in resume_data.get("skills", []))
    required_skills = set(skill.lower() for skill in vacancy.get("required_skills", []))

    if not required_skills:
        return 0.0

    # Calculate skill match percentage
    matching_skills = resume_skills.intersection(required_skills)
    skill_match_ratio = len(matching_skills) / len(required_skills)
    skill_score = skill_match_ratio * 70  # Skills worth 70% of total score

    # Calculate experience match
    resume_experience = resume_data.get("experience_years", 0)
    required_experience = vacancy.get("experience_required", 0)

    if resume_experience >= required_experience:
        experience_score = 30  # Full 30% if experience requirement met
    else:
        if required_experience > 0:
            experience_score = (resume_experience / required_experience) * 30
        else:
            experience_score = 0

    total_score = skill_score + experience_score
    return round(total_score, 1)


def get_latest_resume():
    """Get the latest uploaded resume from uploaded_files directory."""
    try:
        # Look in frontend's uploaded_files directory
        upload_dir = Path(__file__).parent.parent.parent / "frontend" / "uploaded_files"

        if not upload_dir.exists():
            return None

        # Get all files
        files = list(upload_dir.glob("*"))
        if not files:
            return None

        # Return the most recently modified file
        latest_file = max(files, key=lambda f: f.stat().st_mtime)
        return str(latest_file)
    except (IOError, OSError, ValueError) as e:
        print(f"Error finding resume: {e}")
        return None


def get_vacancies(request):
    """
    Retrieve a list of vacancies based on the search request.

    Args:
        request (VacancyRequest): The request containing the job title to search for.

    Returns:
        list[dict]: A list of dictionaries representing vacancies with match scores.
    """
    # Try to get and analyze the uploaded resume
    resume_path = get_latest_resume()
    resume_data = {}

    if resume_path:
        try:
            resume_data = analyze_resume(resume_path)
        except (IOError, OSError) as e:
            print(f"Error analyzing resume: {e}")
            resume_data = {"skills": [], "experience_years": 0}
    else:
        # No resume uploaded, return low scores
        resume_data = {"skills": [], "experience_years": 0}

    # Get job title query
    job_title_query = (
        request.job_title.lower() if hasattr(request, 'job_title') else None
    )

    # Fetch vacancies from APIs or use cached data
    print("Fetching vacancies from job boards...")
    all_vacancies = vacancy_scraper.fetch_all_vacancies(job_title_query)

    # If API fetch failed, try to use cached data
    if not all_vacancies:
        print("API fetch failed, trying cached data...")
        all_vacancies = vacancy_scraper.get_cached_vacancies()

    if not all_vacancies:
        print("No vacancies available from any source")
        return []

    # Calculate match scores for each vacancy
    results = []
    for vacancy in all_vacancies:
        match_score = calculate_match_score(resume_data, vacancy)
        results.append({
            "title": vacancy["title"],
            "company": vacancy["company"],
            "chance": match_score,
            "location": vacancy.get("location", "N/A"),
            "url": vacancy.get("url", ""),
            "source": vacancy.get("source", "unknown")
        })

    # Sort by match score (highest first)
    results.sort(key=lambda x: x["chance"], reverse=True)

    # Return top 20 results
    return results[:20]
