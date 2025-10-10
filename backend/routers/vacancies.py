from fastapi import APIRouter, HTTPException
from schemas.vacancies import VacancyRequest, VacancyResponse
from services.vacancies import get_vacancies

router = APIRouter()

@router.post("/vacancies/search", response_model=list[VacancyResponse])
def search_vacancies(request: VacancyRequest):
    try:
        return get_vacancies(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))