"""
File handler module for processing uploaded files.

This module provides functions to handle file uploads from the frontend.
"""

import os
import streamlit as st

def handle_uploaded_file(uploaded_file):
    """Process the uploaded file."""
    st.sidebar.success("File uploaded successfully!")

    # Create uploaded_files directory if it doesn't exist
    upload_dir = "uploaded_files"
    os.makedirs(upload_dir, exist_ok=True)

    # Save the uploaded file
    file_path = os.path.join(upload_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.sidebar.info(f"Saved file: {uploaded_file.name}")
