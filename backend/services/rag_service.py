"""
RAG (Retrieval-Augmented Generation) service for job matching.

This module provides semantic search and ranking functionality for vacancies.
"""

from typing import List, Dict, Any
from fastapi import HTTPException
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class RAGService:
    def __init__(self):
        self.vacancies = []
        self.vectorizer = TfidfVectorizer()

    def load_vacancies(self, vacancies_data: List[Dict[str, Any]]):
        self.vacancies = vacancies_data
        self.vectorizer.fit([vacancy['description'] for vacancy in self.vacancies])

    def index_vacancies(self):
        if not self.vacancies:
            raise HTTPException(status_code=404, detail="No vacancies available to index.")
        return self.vectorizer.transform([vacancy['description'] for vacancy in self.vacancies])

    def query_vacancies(self, user_query: str, top_n: int = 5) -> List[Dict[str, Any]]:
        if not self.vacancies:
            raise HTTPException(status_code=404, detail="No vacancies available to query.")
        
        query_vector = self.vectorizer.transform([user_query])
        vacancy_vectors = self.index_vacancies()
        similarities = cosine_similarity(query_vector, vacancy_vectors).flatten()
        
        top_indices = np.argsort(similarities)[-top_n:][::-1]
        return [self.vacancies[i] for i in top_indices]

    def get_vacancy_details(self, vacancy_id: str) -> Dict[str, Any]:
        for vacancy in self.vacancies:
            if vacancy['id'] == vacancy_id:
                return vacancy
        raise HTTPException(status_code=404, detail="Vacancy not found.")