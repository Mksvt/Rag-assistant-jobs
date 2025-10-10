from pydantic import BaseModel

class VacancyRequest(BaseModel):
    job_title: str

class VacancyResponse(BaseModel):
    title: str
    company: str
    chance: float