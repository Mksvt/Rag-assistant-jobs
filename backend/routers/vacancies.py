"""
Router for handling vacancy-related endpoints.

This module defines the API endpoints for searching and retrieving vacancies.
"""

from fastapi import APIRouter, HTTPException
from backend.schemas.vacancies import VacancyRequest, VacancyResponse
from backend.services.vacancies import get_vacancies

router = APIRouter()

@router.post("/search", response_model=list[VacancyResponse])
def search_vacancies(request: VacancyRequest):
    """
    Search for vacancies based on the provided job title.

    Args:
        request (VacancyRequest): The request containing the job title to search for.

    Returns:
        list[VacancyResponse]: A list of matching vacancies.

    Raises:
        HTTPException: If an error occurs during the search.
    """
    try:
        return get_vacancies(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))