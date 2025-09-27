import streamlit as st
import requests

def main():
    st.title("RAG Assistant for Job Market")
    
    st.sidebar.header("Upload Resume")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "docx"])
    
    if uploaded_file is not None:
        st.sidebar.success("File uploaded successfully!")
        # Here you would typically process the uploaded resume
        
    st.sidebar.header("Job Search")
    job_title = st.sidebar.text_input("Enter desired job title/field")
    
    if st.sidebar.button("Search"):
        if job_title:
            # Call the backend API to get job recommendations
            response = requests.post("http://localhost:8000/api/vacancies/search", json={"job_title": job_title})
            if response.status_code == 200:
                recommendations = response.json()
                st.write("### Recommended Jobs:")
                for job in recommendations:
                    st.write(f"- {job['title']} at {job['company']} (Chance: {job['chance']}%)")
            else:
                st.error("Error fetching job recommendations.")
        else:
            st.warning("Please enter a job title.")

if __name__ == "__main__":
    main()