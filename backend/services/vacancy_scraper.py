"""
Vacancy scraper service for fetching real job postings from various sources.

This module provides functionality to scrape vacancies from job boards and APIs.
"""

import requests
from typing import List, Dict, Optional
import json
from pathlib import Path


class VacancyScraper:
    """Scraper for fetching job vacancies from multiple sources."""

    def __init__(self):
        """Initialize the vacancy scraper."""
        self.cache_dir = Path(__file__).parent.parent.parent / "data" / "vacancy_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "vacancies.json"

    def fetch_from_arbeitnow(self, job_title: Optional[str] = None) -> List[Dict]:
        """
        Fetch vacancies from Arbeitnow API (free, no auth required).

        Args:
            job_title: Optional job title to search for

        Returns:
            List of vacancy dictionaries
        """
        try:
            url = "https://www.arbeitnow.com/api/job-board-api"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            vacancies = []

            for job in data.get("data", []):
                # Extract skills from tags
                skills = [tag.lower() for tag in job.get("tags", [])]

                vacancy = {
                    "title": job.get("title", ""),
                    "company": job.get("company_name", "Unknown Company"),
                    "description": job.get("description", ""),
                    "location": job.get("location", "Remote"),
                    "url": job.get("url", ""),
                    "required_skills": skills,
                    "experience_required": self._extract_experience(
                        job.get("description", "")
                    ),
                    "source": "arbeitnow"
                }

                # Filter by job title if provided
                if job_title:
                    if job_title.lower() in vacancy["title"].lower():
                        vacancies.append(vacancy)
                else:
                    vacancies.append(vacancy)

            return vacancies

        except requests.exceptions.RequestException as e:
            print(f"Error fetching from Arbeitnow: {e}")
            return []

    def fetch_from_remotive(self, job_title: Optional[str] = None) -> List[Dict]:
        """
        Fetch vacancies from Remotive API (free remote jobs).

        Args:
            job_title: Optional job title to search for

        Returns:
            List of vacancy dictionaries
        """
        try:
            url = "https://remotive.com/api/remote-jobs"
            params = {}
            if job_title:
                params["search"] = job_title

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            vacancies = []

            for job in data.get("jobs", [])[:50]:  # Limit to 50 jobs
                # Extract skills from description
                description = job.get("description", "")
                skills = self._extract_skills_from_text(description)

                vacancy = {
                    "title": job.get("title", ""),
                    "company": job.get("company_name", "Unknown Company"),
                    "description": description,
                    "location": job.get("candidate_required_location", "Remote"),
                    "url": job.get("url", ""),
                    "required_skills": skills,
                    "experience_required": self._extract_experience(description),
                    "source": "remotive"
                }

                vacancies.append(vacancy)

            return vacancies

        except requests.exceptions.RequestException as e:
            print(f"Error fetching from Remotive: {e}")
            return []

    def fetch_all_vacancies(self, job_title: Optional[str] = None) -> List[Dict]:
        """
        Fetch vacancies from all available sources.

        Args:
            job_title: Optional job title to search for

        Returns:
            Combined list of vacancies from all sources
        """
        all_vacancies = []

        # Fetch from all sources
        all_vacancies.extend(self.fetch_from_arbeitnow(job_title))
        all_vacancies.extend(self.fetch_from_remotive(job_title))

        # Cache the results
        self._cache_vacancies(all_vacancies)

        return all_vacancies

    def get_cached_vacancies(self) -> List[Dict]:
        """
        Get vacancies from cache.

        Returns:
            List of cached vacancies, empty list if cache doesn't exist
        """
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error reading cache: {e}")

        return []

    def _cache_vacancies(self, vacancies: List[Dict]) -> None:
        """Save vacancies to cache file."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(vacancies, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error writing cache: {e}")

    def _extract_skills_from_text(self, text: str) -> List[str]:
        """
        Extract common tech skills from job description text.

        Args:
            text: Job description text

        Returns:
            List of extracted skills
        """
        common_skills = [
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c',
            'ruby', 'php', 'go', 'golang', 'rust', 'swift', 'kotlin', 'scala',
            'r', 'matlab', 'perl', 'shell', 'bash', 'powershell', 'vba',
            'objective-c', 'dart', 'elixir', 'haskell', 'lua', 'groovy',
            
            # Web Frontend
            'react', 'angular', 'vue', 'vue.js', 'svelte', 'next.js', 'nuxt.js',
            'html', 'html5', 'css', 'css3', 'sass', 'scss', 'less', 'tailwind',
            'bootstrap', 'material-ui', 'chakra ui', 'jquery', 'webpack',
            'vite', 'babel', 'responsive design', 'ui/ux', 'figma', 'sketch',
            
            # Backend & Frameworks
            'node.js', 'express', 'django', 'flask', 'fastapi', 'spring',
            'spring boot', '.net', 'asp.net', 'laravel', 'symfony', 'rails',
            'ruby on rails', 'gin', 'echo', 'nest.js', 'koa', 'strapi',
            
            # Databases
            'sql', 'nosql', 'postgresql', 'mysql', 'mongodb', 'redis',
            'cassandra', 'elasticsearch', 'oracle', 'sql server', 'mariadb',
            'dynamodb', 'firebase', 'couchdb', 'neo4j', 'influxdb', 'sqlite',
            
            # DevOps & Cloud
            'docker', 'kubernetes', 'k8s', 'aws', 'azure', 'gcp',
            'google cloud', 'heroku', 'digital ocean', 'terraform', 'ansible',
            'jenkins', 'gitlab ci', 'github actions', 'circleci', 'travis ci',
            'ci/cd', 'devops', 'linux', 'unix', 'nginx', 'apache',
            
            # Data Science & ML
            'machine learning', 'deep learning', 'tensorflow', 'pytorch',
            'keras', 'scikit-learn', 'pandas', 'numpy', 'scipy', 'matplotlib',
            'seaborn', 'plotly', 'data analysis', 'data science', 'statistics',
            'nlp', 'computer vision', 'opencv', 'spacy', 'nltk', 'transformers',
            'bert', 'gpt', 'neural networks', 'cnn', 'rnn', 'lstm',
            
            # Mobile Development
            'android', 'ios', 'react native', 'flutter', 'xamarin',
            'ionic', 'cordova', 'swift ui', 'jetpack compose',
            
            # Version Control & Tools
            'git', 'github', 'gitlab', 'bitbucket', 'svn', 'mercurial',
            
            # Testing
            'unit testing', 'integration testing', 'pytest', 'jest', 'mocha',
            'selenium', 'cypress', 'junit', 'testng', 'jasmine', 'karma',
            
            # APIs & Architecture
            'rest api', 'restful', 'graphql', 'soap', 'grpc', 'websocket',
            'microservices', 'monolith', 'event-driven', 'serverless',
            'lambda', 'api gateway', 'message queue', 'rabbitmq', 'kafka',
            
            # Methodologies & Practices
            'agile', 'scrum', 'kanban', 'waterfall', 'tdd', 'bdd', 'ci/cd',
            'pair programming', 'code review', 'design patterns', 'solid',
            
            # Project Management & Collaboration
            'jira', 'confluence', 'trello', 'asana', 'slack', 'teams',
            'notion', 'monday.com',
            
            # Security
            'oauth', 'jwt', 'ssl', 'tls', 'encryption', 'security',
            'penetration testing', 'owasp',
            
            # Other Technologies
            'blockchain', 'ethereum', 'solidity', 'web3', 'smart contracts',
            'iot', 'edge computing', 'big data', 'hadoop', 'spark',
            'etl', 'data warehouse', 'power bi', 'tableau', 'looker',
            
            # Soft Skills
            'communication', 'leadership', 'teamwork', 'problem solving',
            'critical thinking', 'time management', 'adaptability',
            
            # HR & Recruitment Skills
            'recruitment', 'talent acquisition', 'sourcing', 'interviewing',
            'onboarding', 'hr management', 'applicant tracking', 'ats',
            'linkedin recruiter', 'boolean search', 'candidate screening',
            'employer branding', 'crm', 'zoho', 'hubspot', 'greenhouse',
            'workday', 'bamboohr', 'performance management',
            
            # Business & Management
            'project management', 'product management', 'business analysis',
            'stakeholder management', 'budget management', 'strategic planning',
            'kpi', 'roi', 'excel', 'powerpoint', 'word', 'google sheets',
            'salesforce', 'erp', 'sap', 'crm systems'
        ]

        text_lower = text.lower()
        found_skills = []

        for skill in common_skills:
            if skill in text_lower:
                found_skills.append(skill)

        return list(set(found_skills))

    def _extract_experience(self, text: str) -> int:
        """
        Extract required years of experience from text.

        Args:
            text: Job description text

        Returns:
            Number of years of experience required
        """
        import re

        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?experience',
            r'experience[:\s]+(\d+)\+?\s*(?:years?|yrs?)',
            r'(\d+)\+?\s*(?:years?|yrs?)\s+in',
        ]

        text_lower = text.lower()
        years = []

        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            years.extend([int(match) for match in matches])

        return max(years) if years else 0
