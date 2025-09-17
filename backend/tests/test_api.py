from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_get_vacancies():
    response = client.get("/api/vacancies/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_vacancy():
    vacancy_data = {
        "title": "Software Engineer",
        "company": "Tech Company",
        "stack": ["Python", "FastAPI"],
        "requirements": "Experience with Python and FastAPI",
        "salary": 60000,
        "description": "Looking for a Software Engineer."
    }
    response = client.post("/api/vacancies/", json=vacancy_data)
    assert response.status_code == 201
    assert response.json()["title"] == vacancy_data["title"]

def test_update_vacancy():
    vacancy_data = {
        "title": "Software Engineer",
        "company": "Tech Company",
        "stack": ["Python", "FastAPI"],
        "requirements": "Experience with Python and FastAPI",
        "salary": 60000,
        "description": "Looking for a Software Engineer."
    }
    response = client.post("/api/vacancies/", json=vacancy_data)
    vacancy_id = response.json()["id"]

    updated_data = {
        "title": "Senior Software Engineer",
        "company": "Tech Company",
        "stack": ["Python", "FastAPI", "Docker"],
        "requirements": "Experience with Python, FastAPI, and Docker",
        "salary": 80000,
        "description": "Looking for a Senior Software Engineer."
    }
    response = client.put(f"/api/vacancies/{vacancy_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["title"] == updated_data["title"]

def test_delete_vacancy():
    vacancy_data = {
        "title": "Software Engineer",
        "company": "Tech Company",
        "stack": ["Python", "FastAPI"],
        "requirements": "Experience with Python and FastAPI",
        "salary": 60000,
        "description": "Looking for a Software Engineer."
    }
    response = client.post("/api/vacancies/", json=vacancy_data)
    vacancy_id = response.json()["id"]

    response = client.delete(f"/api/vacancies/{vacancy_id}")
    assert response.status_code == 204

    response = client.get(f"/api/vacancies/{vacancy_id}")
    assert response.status_code == 404