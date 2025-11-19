"""
API client module for frontend communication with backend.

This module provides functions to interact with the backend API.
"""

import requests

def search_vacancies(job_title):
    """Call the backend API to get job recommendations."""
    try:
        response = requests.post(
            "http://localhost:8000/api/vacancies/search",
            json={"job_title": job_title},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the backend: {e}")
        return None
