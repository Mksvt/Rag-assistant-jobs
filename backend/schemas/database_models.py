"""
Pydantic schemas for database models.

This module defines the Pydantic models for request/response validation.
"""

from pydantic import BaseModel
from typing import List, Optional


class VacancyBase(BaseModel):
    """Base schema for vacancy."""

    title: str
    company: str
    location: str = "Remote"
    url: Optional[str] = None
    source: str = "manual"
    description: str
    required_skills: List[str] = []
    experience_required: int = 0
    salary: Optional[float] = None


class VacancyCreate(VacancyBase):
    """Schema for creating a vacancy."""


class VacancyUpdate(BaseModel):
    """Schema for updating a vacancy."""

    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[List[str]] = None
    experience_required: Optional[int] = None
    salary: Optional[float] = None


class VacancyInDB(VacancyBase):
    """Schema for vacancy from database."""

    id: int

    class Config:
        """Pydantic config."""

        from_attributes = True


class ResumeBase(BaseModel):
    """Base schema for resume."""

    name: str
    file_path: str
    experience: str
    skills: List[str] = []
    experience_years: int = 0
    education: str = ""
    projects: str = ""


class ResumeCreate(ResumeBase):
    """Schema for creating a resume."""


class ResumeInDB(ResumeBase):
    """Schema for resume from database."""

    id: int

    class Config:
        """Pydantic config."""

        from_attributes = True


class PolicyBase(BaseModel):
    """Base schema for corporate policy."""

    company_name: str
    policy_document: str


class PolicyCreate(PolicyBase):
    """Schema for creating a policy."""


class PolicyInDB(PolicyBase):
    """Schema for policy from database."""

    id: int

    class Config:
        """Pydantic config."""

        from_attributes = True
