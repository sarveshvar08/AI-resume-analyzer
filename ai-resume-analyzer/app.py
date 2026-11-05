import streamlit as st
import fitz
from resume_parser import extract_resume_text
from analyzer import analyze_resume

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

        with st.spinner("Analyzing your resume..."):

            resume_text = extract_resume_text(resume)

            if not resume_text:
                st.error("Could not extract resume text.")

            else:

                results = analyze_resume(
                    resume_text,
                    job_description
                )

                st.success("Analysis completed!")

                # Display match percentage
                st.subheader("Resume Match Analysis")

                score = results["match_percentage"]

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Resume Match",
                        f"{score}%"
                    )

                with col2:
                    st.metric(
                        "Matching Terms",
                        len(results["matching_terms"])
                    )

                st.progress(score / 100)

                # Matching terms
                st.subheader("Matching Keywords")

                st.write(
                    results["matching_terms"]
                    if results["matching_terms"]
                    else "No matching terms found."
                )

                # Missing terms
                st.subheader("Potentially Missing Keywords")

                st.write(
                    results["missing_terms"]
                    if results["missing_terms"]
                    else "No missing terms found."
                )