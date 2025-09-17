from fastapi import APIRouter, HTTPException
from typing import List
from ..models import Vacancy
from ..database.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/vacancies", response_model=List[Vacancy])
def get_vacancies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    vacancies = db.query(Vacancy).offset(skip).limit(limit).all()
    return vacancies

@router.post("/vacancies", response_model=Vacancy)
def create_vacancy(vacancy: Vacancy, db: Session = Depends(get_db)):
    db.add(vacancy)
    db.commit()
    db.refresh(vacancy)
    return vacancy

@router.put("/vacancies/{vacancy_id}", response_model=Vacancy)
def update_vacancy(vacancy_id: int, vacancy: Vacancy, db: Session = Depends(get_db)):
    db_vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if db_vacancy is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    for key, value in vacancy.dict().items():
        setattr(db_vacancy, key, value)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy

@router.delete("/vacancies/{vacancy_id}")
def delete_vacancy(vacancy_id: int, db: Session = Depends(get_db)):
    db_vacancy = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if db_vacancy is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    db.delete(db_vacancy)
    db.commit()
    return {"detail": "Vacancy deleted"}