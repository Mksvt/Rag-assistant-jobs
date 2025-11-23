"""
API endpoints for vacancy CRUD operations.

This module provides database-based endpoints for managing vacancies.
Note: For job matching use /api/vacancies/search from backend.routers.vacancies
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.database.models import Vacancy
from backend.schemas.database_models import (
    VacancyCreate,
    VacancyUpdate,
    VacancyInDB
)

router = APIRouter()


@router.get("/vacancies", response_model=List[VacancyInDB])
def get_all_vacancies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all vacancies from database.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session

    Returns:
        List of vacancies
    """
    vacancies = db.query(Vacancy).offset(skip).limit(limit).all()
    return vacancies


@router.get("/vacancies/{vacancy_id}", response_model=VacancyInDB)
def get_vacancy(vacancy_id: int, db: Session = Depends(get_db)):
    """
    Get a specific vacancy by ID.

    Args:
        vacancy_id: ID of the vacancy
        db: Database session

    Returns:
        Vacancy object

    Raises:
        HTTPException: If vacancy not found
    """
    vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if vacancy is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return vacancy


@router.post("/vacancies", response_model=VacancyInDB, status_code=201)
def create_vacancy(vacancy: VacancyCreate, db: Session = Depends(get_db)):
    """
    Create a new vacancy.

    Args:
        vacancy: Vacancy data
        db: Database session

    Returns:
        Created vacancy
    """
    db_vacancy = Vacancy(**vacancy.model_dump())
    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy


@router.put("/vacancies/{vacancy_id}", response_model=VacancyInDB)
def update_vacancy(
    vacancy_id: int,
    vacancy: VacancyUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing vacancy.

    Args:
        vacancy_id: ID of the vacancy to update
        vacancy: Updated vacancy data
        db: Database session

    Returns:
        Updated vacancy

    Raises:
        HTTPException: If vacancy not found
    """
    db_vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if db_vacancy is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    # Update only provided fields
    update_data = vacancy.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_vacancy, key, value)

    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy


@router.delete("/vacancies/{vacancy_id}", status_code=204)
def delete_vacancy(vacancy_id: int, db: Session = Depends(get_db)):
    """
    Delete a vacancy.

    Args:
        vacancy_id: ID of the vacancy to delete
        db: Database session

    Raises:
        HTTPException: If vacancy not found
    """
    db_vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if db_vacancy is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")

    db.delete(db_vacancy)
    db.commit()
    return None