# API Endpoints Documentation

## Огляд

SkillMatch AI надає два типи endpoints:

### 1. Job Matching API (`/api/vacancies`)

Використовує зовнішні API для пошуку вакансій та matching з резюме.

### 2. Database CRUD API (`/api/db`)

Управління вакансіями в локальній базі даних SQLite.

---

## Job Matching Endpoints

### POST `/api/vacancies/search`

Пошук вакансій та matching з завантаженим резюме.

**Request Body:**

```json
{
  "job_title": "Python Developer"
}
```

**Response:**

```json
[
  {
    "title": "Senior Python Developer",
    "company": "Tech Corp",
    "chance": 85.5,
    "location": "Remote",
    "url": "https://...",
    "source": "arbeitnow"
  }
]
```

---

## Database CRUD Endpoints

### GET `/api/db/vacancies`

Отримати всі вакансії з бази даних.

**Query Parameters:**

- `skip` (int, default=0): Скільки записів пропустити
- `limit` (int, default=100): Максимальна кількість записів

**Response:**

```json
[
  {
    "id": 1,
    "title": "Backend Developer",
    "company": "StartupXYZ",
    "location": "Kyiv",
    "url": null,
    "source": "manual",
    "description": "Looking for experienced backend developer...",
    "required_skills": ["python", "django", "postgresql"],
    "experience_required": 3,
    "salary": 3000.0
  }
]
```

---

### GET `/api/db/vacancies/{vacancy_id}`

Отримати конкретну вакансію за ID.

**Response:**

```json
{
  "id": 1,
  "title": "Backend Developer",
  "company": "StartupXYZ",
  ...
}
```

**Error Response (404):**

```json
{
  "detail": "Vacancy not found"
}
```

---

### POST `/api/db/vacancies`

Створити нову вакансію в базі даних.

**Request Body:**

```json
{
  "title": "Frontend Developer",
  "company": "WebAgency",
  "location": "Remote",
  "url": "https://example.com/job",
  "source": "manual",
  "description": "We are looking for a frontend developer with React experience...",
  "required_skills": ["react", "typescript", "css"],
  "experience_required": 2,
  "salary": 2500.0
}
```

**Response (201 Created):**

```json
{
  "id": 2,
  "title": "Frontend Developer",
  ...
}
```

---

### PUT `/api/db/vacancies/{vacancy_id}`

Оновити існуючу вакансію.

**Request Body** (всі поля опціональні):

```json
{
  "title": "Senior Frontend Developer",
  "salary": 3500.0,
  "required_skills": ["react", "typescript", "next.js", "css"]
}
```

**Response:**

```json
{
  "id": 2,
  "title": "Senior Frontend Developer",
  "salary": 3500.0,
  ...
}
```

---

### DELETE `/api/db/vacancies/{vacancy_id}`

Видалити вакансію з бази даних.

**Response:** 204 No Content

**Error Response (404):**

```json
{
  "detail": "Vacancy not found"
}
```

---

## Приклади використання

### Python (requests)

```python
import requests

# Пошук вакансій через API
response = requests.post(
    "http://localhost:8000/api/vacancies/search",
    json={"job_title": "Python Developer"}
)
jobs = response.json()

# Створення вакансії в БД
response = requests.post(
    "http://localhost:8000/api/db/vacancies",
    json={
        "title": "Python Developer",
        "company": "My Company",
        "location": "Lviv",
        "description": "Python developer needed...",
        "required_skills": ["python", "django", "docker"],
        "experience_required": 3,
        "salary": 3000.0
    }
)
new_vacancy = response.json()

# Отримання всіх вакансій
response = requests.get("http://localhost:8000/api/db/vacancies")
all_vacancies = response.json()

# Оновлення вакансії
response = requests.put(
    f"http://localhost:8000/api/db/vacancies/{new_vacancy['id']}",
    json={"salary": 3500.0}
)

# Видалення вакансії
response = requests.delete(
    f"http://localhost:8000/api/db/vacancies/{new_vacancy['id']}"
)
```

### JavaScript (fetch)

```javascript
// Пошук вакансій
const searchJobs = async (jobTitle) => {
  const response = await fetch('http://localhost:8000/api/vacancies/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ job_title: jobTitle }),
  });
  return await response.json();
};

// Створення вакансії
const createVacancy = async (vacancyData) => {
  const response = await fetch('http://localhost:8000/api/db/vacancies', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(vacancyData),
  });
  return await response.json();
};

// Використання
const jobs = await searchJobs('Python Developer');
console.log(jobs);
```

---

## Swagger UI

Інтерактивна документація доступна за адресою:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## База даних

Система використовує SQLite базу даних, яка автоматично створюється при запуску:

- **Шлях**: `data/skillmatch.db`
- **Таблиці**: vacancies, resumes, corporate_policies

База даних створюється автоматично при першому запуску backend сервера.
