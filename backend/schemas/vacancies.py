"""
Schemas for vacancy-related data.

This module defines the Pydantic models for validating vacancy-related requests and responses.
"""

from pydantic import BaseModel

class VacancyRequest(BaseModel):
    """
    Schema for a vacancy search request.

    Attributes:
        job_title (str): The job title to search for.
    """
    job_title: str

class VacancyResponse(BaseModel):
    """
    Schema for a vacancy search response.

    Attributes:
        title (str): The title of the job vacancy.
        company (str): The company offering the job.
        chance (float): The calculated chance of matching the job.
    """
    title: str
    company: str
    chance: float
