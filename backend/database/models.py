"""
Database models for the RAG Assistant application.

This module defines SQLAlchemy ORM models for vacancies, resumes, and policies.
"""

from sqlalchemy import Column, Integer, String, Text, Float, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Vacancy(Base):
    """Vacancy model for storing job postings."""

    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String)
    location = Column(String, default="Remote")
    url = Column(String, nullable=True)
    source = Column(String, default="manual")
    description = Column(Text)
    required_skills = Column(JSON, default=list)
    experience_required = Column(Integer, default=0)
    salary = Column(Float, nullable=True)

class Resume(Base):
    """Resume model for storing candidate information."""

    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    file_path = Column(String)
    experience = Column(Text)
    skills = Column(JSON, default=list)
    experience_years = Column(Integer, default=0)
    education = Column(Text)
    projects = Column(Text)


class CorporatePolicy(Base):
    """Corporate policy model for storing company policies."""

    __tablename__ = 'corporate_policies'

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String)
    policy_document = Column(Text)