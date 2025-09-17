# RAG Assistant for Job Market

## Project Overview

The RAG Assistant is a system designed to help users find job vacancies that match their resumes and improve their chances of successful interviews. It combines Retrieval-Augmented Generation (RAG) with Machine Learning techniques for classification and recommendations.

## Features

- **RAG Module**: 
  - Indexing job vacancies from platforms like LinkedIn, Djinni, and Indeed.
  - Incorporating corporate policies in various document formats (PDF, DOCX).
  - Vector indexing for efficient search and retrieval.
  - Providing user responses in a conversational format with job data.

- **Machine Learning Module**:
  - Analyzing candidate resumes in text and PDF formats.
  - Extracting key skills and experiences using Named Entity Recognition (NER) and embeddings.
  - Classifying resumes to match job vacancies using algorithms like Logistic Regression, XGBoost, or Transformers.
  - Predicting interview chances through binary classification or scoring.

- **User Functionality**:
  - Uploading resumes.
  - Entering desired job titles or industries.
  - Receiving job recommendations with explanations.
  - Analytics on skills to improve for better job prospects.

## Architecture

- **Frontend**: Built with Streamlit for rapid prototyping or React for a more robust application.
- **Backend**: Developed using FastAPI or Flask.
- **RAG**: Utilizes FAISS for vector search and LangChain/LlamaIndex for integration with large language models (LLMs).
- **Machine Learning**: Implemented with libraries like sklearn, XGBoost, and HuggingFace Transformers.
- **Database**: PostgreSQL for storing job vacancies and resumes, with MinIO/S3 for document storage.
- **LLM**: Options include OpenAI GPT-4, LLaMA 3, or Mistral for local deployment.

## Data Structure

- **Job Vacancies**: 
  - Sourced from APIs or stored in CSV files.
  - Fields include title, company, tech stack, requirements, salary, and description.
  
- **Resumes**: 
  - Stored in PDF and DOCX formats.
  - Fields include name, experience, tech stack, education, and projects.
  
- **Corporate Policies**: 
  - Stored in PDF/DOCX formats detailing HR rules and company requirements.

## ML Models

1. **NER / Skill Extraction**: 
   - Utilizes HuggingFace models for extracting skills from resumes and job vacancies.
   
2. **Resume to Job Classification**: 
   - Models such as Logistic Regression, XGBoost, or BERT for assessing match quality.
   
3. **Interview Chance Scoring**: 
   - Provides a probability score (0-100%) for interview likelihood.

## User Flow Example

1. User uploads a resume (PDF).
2. The system extracts skills and forms a vector representation.
3. User inputs a job title, e.g., "Junior Python Developer".
4. RAG retrieves relevant job vacancies from the database.
5. The ML model ranks vacancies based on match quality.
6. Response example:
   ```
   Best job matches for you:
   1. Python Developer @ XYZ (85% chance)
   2. Data Analyst @ ABC (72% chance)
   Recommendation: Add experience with Docker to improve your chances.
   ```

## Future Enhancements

- Dashboard for visual analytics on in-demand skills.
- Automatic job vacancy updates via API.
- Recommendations for courses/resources to address skill gaps.

## Technologies Used

- **Python**: FastAPI, Streamlit, LangChain, FAISS, sklearn, HuggingFace.
- **Database**: PostgreSQL with FAISS.
- **UI**: Streamlit or React.
- **LLM**: GPT-4 or LLaMA3.

## Getting Started

To set up the project, clone the repository and install the required dependencies listed in `requirements.txt`. Follow the instructions in the respective sections for backend and frontend setup.

## License

This project is licensed under the MIT License.