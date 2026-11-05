import streamlit as st
import fitz
from resume_parser import extract_resume_text

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Application title
st.title("AI Resume Analyzer")
st.write("Analyze your resume against a job description.")

st.divider()

# Two-column layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload Resume")
    resume = st.file_uploader(
        "Upload your resume (PDF)",
        type=["pdf"]
    )

with col2:
    st.subheader("Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="Enter the job requirements..."
    )

st.divider()

# Analyze button
if st.button("Analyze Resume", use_container_width=True):

    if resume is None:
        st.error("Please upload your resume.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:
        with st.spinner("Extracting resume text..."):

            resume_text = extract_resume_text(resume)

        if resume_text:

            st.success("Resume text extracted successfully!")

            with st.expander("View Extracted Resume Text"):
                st.text(resume_text)

        else:
            st.error(
                "Could not extract text. "
                "Your PDF may be scanned or image-based."
            )
