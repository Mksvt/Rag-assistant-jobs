"""
Frontend application for the RAG Assistant.

This module defines the Streamlit-based user interface for interacting with the RAG Assistant.
"""

import streamlit as st
import requests
from api_client import search_vacancies
from file_handler import handle_uploaded_file

API_BASE_URL = "http://localhost:8000"


def main():
    """
    Main function for the Streamlit application.

    This function defines the layout and functionality of the user interface.
    """
    st.set_page_config(
        page_title="SkillMatch AI",
        page_icon="🎯",
        layout="wide"
    )

    st.title("🎯 SkillMatch AI - Job Market Assistant")

    # Створюємо вкладки
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Job Search",
        "📊 Manage Vacancies",
        "📈 Statistics",
        "🧪 API Test"
    ])

    with tab1:
        job_search_tab()

    with tab2:
        manage_vacancies_tab()

    with tab3:
        statistics_tab()

    with tab4:
        api_test_tab()


def job_search_tab():
    """Вкладка пошуку вакансій з matching."""
    st.header("Job Search & Matching")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📄 Upload Resume")
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF or DOCX)",
            type=["pdf", "docx"]
        )

        if uploaded_file is not None:
            handle_uploaded_file(uploaded_file)
            st.success(f"✅ Resume uploaded: {uploaded_file.name}")

    with col2:
        st.subheader("🔍 Search Jobs")
        job_title = st.text_input("Job Title/Field", placeholder="e.g., Python Developer")

        if st.button("🔎 Search Jobs", use_container_width=True):
            if job_title:
                with st.spinner("Searching for job opportunities..."):
                    recommendations = search_vacancies(job_title)

                if recommendations:
                    st.write(f"### Found {len(recommendations)} Job Opportunities:")
                    st.write("---")

                    for idx, job in enumerate(recommendations, 1):
                        with st.expander(
                            f"#{idx}: {job['title']} at {job['company']} - "
                            f"Match: {job['chance']}%"
                        ):
                            st.write(f"**Company:** {job['company']}")
                            st.write(f"**Location:** {job.get('location', 'N/A')}")
                            st.write(f"**Match Score:** {job['chance']}%")
                            st.write(f"**Source:** {job.get('source', 'N/A')}")

                            if job.get('url'):
                                st.markdown(f"[🔗 View Job Posting]({job['url']})")

                    st.success(f"✅ Successfully matched {len(recommendations)} jobs!")
                else:
                    st.warning("No job recommendations found. Try a different search term.")
            else:
                st.warning("Please enter a job title.")


def manage_vacancies_tab():
    """Вкладка управління вакансіями в базі даних."""
    st.header("Manage Vacancies Database")

    # Підвкладки для різних операцій
    subtab1, subtab2, subtab3 = st.tabs(["📋 View All", "➕ Add New", "✏️ Edit/Delete"])

    with subtab1:
        st.subheader("All Vacancies in Database")
        if st.button("🔄 Refresh List"):
            try:
                response = requests.get(f"{API_BASE_URL}/api/db/vacancies", timeout=10)
                if response.status_code == 200:
                    vacancies = response.json()
                    if vacancies:
                        for vac in vacancies:
                            with st.expander(f"{vac['title']} - {vac['company']}"):
                                st.write(f"**ID:** {vac['id']}")
                                st.write(f"**Location:** {vac.get('location', 'N/A')}")
                                st.write(f"**Skills:** {', '.join(vac.get('required_skills', []))}")
                                st.write(f"**Experience:** {vac.get('experience_required', 0)} years")
                                st.write(f"**Salary:** ${vac.get('salary', 0)}")
                                st.write(f"**Description:** {vac.get('description', 'N/A')}")
                    else:
                        st.info("No vacancies in database yet.")
                else:
                    st.error("Failed to fetch vacancies")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")

    with subtab2:
        st.subheader("Add New Vacancy")
        with st.form("add_vacancy_form"):
            title = st.text_input("Job Title*")
            company = st.text_input("Company*")
            location = st.text_input("Location", value="Remote")
            url = st.text_input("URL (optional)")
            description = st.text_area("Description*")
            skills_input = st.text_input(
                "Required Skills (comma-separated)*",
                placeholder="python, django, postgresql"
            )
            experience = st.number_input("Years of Experience", min_value=0, value=0)
            salary = st.number_input("Salary (optional)", min_value=0.0, value=0.0)

            submitted = st.form_submit_button("➕ Add Vacancy")

            if submitted:
                if title and company and description and skills_input:
                    skills = [s.strip() for s in skills_input.split(",")]
                    vacancy_data = {
                        "title": title,
                        "company": company,
                        "location": location,
                        "url": url if url else None,
                        "source": "manual",
                        "description": description,
                        "required_skills": skills,
                        "experience_required": experience,
                        "salary": salary if salary > 0 else None
                    }

                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/api/db/vacancies",
                            json=vacancy_data,
                            timeout=10
                        )
                        if response.status_code == 201:
                            st.success("✅ Vacancy added successfully!")
                        else:
                            st.error(f"Error: {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection error: {e}")
                else:
                    st.warning("Please fill all required fields (marked with *)")

    with subtab3:
        st.subheader("Edit or Delete Vacancy")
        vacancy_id = st.number_input("Enter Vacancy ID", min_value=1, step=1)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🗑️ Delete Vacancy", use_container_width=True):
                try:
                    response = requests.delete(
                        f"{API_BASE_URL}/api/db/vacancies/{vacancy_id}",
                        timeout=10
                    )
                    if response.status_code == 204:
                        st.success("✅ Vacancy deleted successfully!")
                    elif response.status_code == 404:
                        st.error("Vacancy not found")
                    else:
                        st.error(f"Error: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {e}")

        with col2:
            if st.button("📄 Load Vacancy Data", use_container_width=True):
                try:
                    response = requests.get(
                        f"{API_BASE_URL}/api/db/vacancies/{vacancy_id}",
                        timeout=10
                    )
                    if response.status_code == 200:
                        vac = response.json()
                        st.session_state['edit_vacancy'] = vac
                        st.success("Vacancy loaded!")
                    else:
                        st.error("Vacancy not found")
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {e}")

        if 'edit_vacancy' in st.session_state:
            vac = st.session_state['edit_vacancy']
            st.write("---")
            st.write(f"**Editing:** {vac['title']}")

            with st.form("edit_vacancy_form"):
                new_title = st.text_input("Title", value=vac['title'])
                new_salary = st.number_input(
                    "Salary",
                    min_value=0.0,
                    value=float(vac.get('salary', 0))
                )

                if st.form_submit_button("💾 Update Vacancy"):
                    update_data = {
                        "title": new_title,
                        "salary": new_salary if new_salary > 0 else None
                    }

                    try:
                        response = requests.put(
                            f"{API_BASE_URL}/api/db/vacancies/{vac['id']}",
                            json=update_data,
                            timeout=10
                        )
                        if response.status_code == 200:
                            st.success("✅ Vacancy updated successfully!")
                            del st.session_state['edit_vacancy']
                        else:
                            st.error(f"Error: {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection error: {e}")


def statistics_tab():
    """Вкладка статистики."""
    st.header("📈 Statistics & Analytics")

    try:
        response = requests.get(f"{API_BASE_URL}/api/db/vacancies?limit=1000", timeout=10)
        if response.status_code == 200:
            vacancies = response.json()

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Vacancies", len(vacancies))

            with col2:
                avg_exp = sum(v.get('experience_required', 0) for v in vacancies) / len(vacancies) if vacancies else 0
                st.metric("Avg Experience Required", f"{avg_exp:.1f} years")

            with col3:
                salaries = [v.get('salary', 0) for v in vacancies if v.get('salary')]
                avg_salary = sum(salaries) / len(salaries) if salaries else 0
                st.metric("Avg Salary", f"${avg_salary:.0f}")

            # Топ компанії
            st.subheader("Top Companies")
            companies = {}
            for v in vacancies:
                company = v.get('company', 'Unknown')
                companies[company] = companies.get(company, 0) + 1

            sorted_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:5]
            for company, count in sorted_companies:
                st.write(f"- **{company}**: {count} vacancies")

        else:
            st.error("Failed to fetch statistics")
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")


def api_test_tab():
    """Вкладка тестування API."""
    st.header("🧪 API Testing")

    st.subheader("Test API Endpoints")

    endpoint = st.selectbox(
        "Select Endpoint",
        [
            "GET /api/db/vacancies",
            "POST /api/vacancies/search",
            "GET /api/db/vacancies/{id}"
        ]
    )

    if endpoint == "GET /api/db/vacancies":
        if st.button("Send Request"):
            try:
                response = requests.get(f"{API_BASE_URL}/api/db/vacancies", timeout=10)
                st.write(f"**Status Code:** {response.status_code}")
                st.json(response.json())
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")

    elif endpoint == "POST /api/vacancies/search":
        job_title = st.text_input("Job Title", value="Python Developer")
        if st.button("Send Request"):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/api/vacancies/search",
                    json={"job_title": job_title},
                    timeout=10
                )
                st.write(f"**Status Code:** {response.status_code}")
                st.json(response.json())
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")

    elif endpoint == "GET /api/db/vacancies/{id}":
        vacancy_id = st.number_input("Vacancy ID", min_value=1, value=1)
        if st.button("Send Request"):
            try:
                response = requests.get(
                    f"{API_BASE_URL}/api/db/vacancies/{vacancy_id}",
                    timeout=10
                )
                st.write(f"**Status Code:** {response.status_code}")
                st.json(response.json())
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")

    st.write("---")
    st.subheader("API Documentation")
    st.markdown("""
    - **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
    - **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
    """)


if __name__ == "__main__":
    main()
