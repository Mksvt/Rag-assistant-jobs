"""
Frontend application for the RAG Assistant.

This module defines the Streamlit-based user interface for interacting with the RAG Assistant.
"""

import streamlit as st
from api_client import search_vacancies
from file_handler import handle_uploaded_file

def main():
    """
    Main function for the Streamlit application.

    This function defines the layout and functionality of the user interface.
    """
    st.title("RAG Assistant for Job Market")

    # Sidebar for file upload
    st.sidebar.header("Upload Resume")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "docx"])

    if uploaded_file is not None:
        handle_uploaded_file(uploaded_file)

    # Sidebar for job search
    st.sidebar.header("Job Search")
    job_title = st.sidebar.text_input("Enter desired job title/field")

    if st.sidebar.button("Search"):
        if job_title:
            recommendations = search_vacancies(job_title)
            if recommendations:
                st.write("### Recommended Jobs:")
                for job in recommendations:
                    st.write(f"- {job['title']} at {job['company']} (Chance: {job['chance']}%)")
            else:
                st.error("Error fetching job recommendations.")
        else:
            st.warning("Please enter a job title.")

if __name__ == "__main__":
    main()
