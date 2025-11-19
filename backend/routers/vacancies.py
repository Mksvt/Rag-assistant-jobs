"""
Router for handling vacancy-related endpoints.

This module defines the API endpoints for searching and retrieving vacancies.
"""

import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException

# Add project root to sys.path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.schemas.vacancies import VacancyRequest, VacancyResponse  # pylint: disable=wrong-import-position
from backend.services.vacancies import get_vacancies  # pylint: disable=wrong-import-position

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
        raise HTTPException(status_code=500, detail=str(e)) from e
