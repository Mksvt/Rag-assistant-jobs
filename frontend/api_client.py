import requests

def search_vacancies(job_title):
    """Call the backend API to get job recommendations."""
    try:
        response = requests.post("http://localhost:8000/api/vacancies/search", json={"job_title": job_title})
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the backend: {e}")
        return None