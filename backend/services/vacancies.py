"""
Service layer for vacancy-related logic.

This module contains the business logic for handling vacancy-related operations.
"""

def get_vacancies(request):
    """
    Retrieve a list of vacancies based on the search request.

    Args:
        request (VacancyRequest): The request containing the job title to search for.

    Returns:
        list[dict]: A list of dictionaries representing vacancies.
    """
    # Mock implementation for now
    return [
        {"title": "Python Developer", "company": "XYZ Corp", "chance": 85.0},
        {"title": "Data Analyst", "company": "ABC Inc", "chance": 72.0},
    ]