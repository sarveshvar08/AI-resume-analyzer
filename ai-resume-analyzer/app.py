import streamlit as st
import fitz
from resume_parser import extract_resume_text
from analyzer import analyze_resume
from skill_extractor import extract_skills

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

# Extract skills from resume and job description
resume_skills = extract_skills(resume_text)
job_skills = extract_skills(job_description)

# Flatten category-wise skills into lists
resume_skill_list = [
    skill
    for skills in resume_skills.values()
    for skill in skills
]

job_skill_list = [
    skill
    for skills in job_skills.values()
    for skill in skills
]

# Identify missing skills
missing_skills = [
    skill
    for skill in job_skill_list
    if skill not in resume_skill_list
]

# Calculate skill coverage
if job_skill_list:
    matched_skills = set(resume_skill_list) & set(job_skill_list)

    skill_coverage = (
        len(matched_skills) / len(set(job_skill_list))
    ) * 100
else:
    skill_coverage = 0

st.divider()

st.header("Resume Skill Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Resume Skills", len(resume_skill_list))

with col2:
    st.metric("Required Skills", len(job_skill_list))

with col3:
    st.metric("Skill Coverage", f"{skill_coverage:.1f}%")

st.subheader("Skills Found in Resume")

for category, skills in resume_skills.items():
    if skills:
        st.write(f"**{category}:** {', '.join(skills)}")

st.subheader("Skills Required by Job")

for category, skills in job_skills.items():
    if skills:
        st.write(f"**{category}:** {', '.join(skills)}")

st.subheader("Missing Skills")

if missing_skills:
    st.warning(", ".join(missing_skills))
else:
    st.success("All detected required skills are present!")