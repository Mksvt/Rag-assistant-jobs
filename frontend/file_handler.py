"""
File handler module for processing uploaded files.

This module provides functions to handle file uploads from the frontend.
"""

import streamlit as st

def handle_uploaded_file(uploaded_file):
    """Process the uploaded file."""
    st.sidebar.success("File uploaded successfully!")
    # Here you would typically process the uploaded resume
    # For example, save it to a directory or extract its content
    with open(f"uploaded_files/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.info(f"Saved file: {uploaded_file.name}")
