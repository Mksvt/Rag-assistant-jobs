"""
Main entry point for the backend application.

This file initializes and runs the FastAPI application.
"""

import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add project root to sys.path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.routers import vacancies  # pylint: disable=wrong-import-position
from backend.api.endpoints import vacancies as vacancy_crud  # pylint: disable=wrong-import-position

app = FastAPI(
    title="SkillMatch AI - RAG Assistant",
    description="Job matching system with ML and RAG capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# Job matching and search (uses external APIs)
app.include_router(
    vacancies.router,
    prefix="/api/vacancies",
    tags=["Job Matching"]
)

# CRUD operations for database (manual vacancy management)
app.include_router(
    vacancy_crud.router,
    prefix="/api/db",
    tags=["Database CRUD"]
)

@app.get("/")
def read_root():
    """
    Root endpoint for the application.

    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome to the RAG Assistant for the Job Market!"}
