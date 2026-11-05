import streamlit as st

from resume_parser import extract_resume_text
from analyzer import analyze_resume
from skill_extractor import extract_skills
from improvement_suggestions import generate_suggestions
from section_detector import detect_sections
from report_generator import generate_pdf_report


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# ==========================================
# APPLICATION HEADER
# ==========================================

st.title("AI Resume Analyzer")

st.write(
    "Analyze your resume against a job description "
    "and discover ways to improve it."
)

st.divider()


# ==========================================
# USER INPUT
# ==========================================

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


# ==========================================
# ANALYZE BUTTON
# ==========================================

if st.button("Analyze Resume", use_container_width=True):

    if resume is None:

        st.error("Please upload your resume.")

    elif not job_description.strip():

        st.error("Please enter a job description.")

    else:

        with st.spinner("Analyzing your resume..."):

            # ----------------------------------
            # STEP 1: EXTRACT RESUME TEXT
            # ----------------------------------

            resume_text = extract_resume_text(resume)

            if not resume_text:

                st.error(
                    "Could not extract resume text. "
                    "Please upload a valid text-based PDF."
                )

            else:

                # ----------------------------------
                # STEP 2: RESUME MATCH ANALYSIS
                # ----------------------------------

                results = analyze_resume(
                    resume_text,
                    job_description
                )

                score = results["match_percentage"]

                st.success("Analysis completed!")

                st.divider()

                st.header("1. Resume Match Analysis")

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

                st.progress(
                    max(0.0, min(score / 100, 1.0))
                )

                # Matching keywords

                st.subheader("Matching Keywords")

                st.write(
                    results["matching_terms"]
                    if results["matching_terms"]
                    else "No matching terms found."
                )

                # Missing keywords

                st.subheader("Potentially Missing Keywords")

                st.write(
                    results["missing_terms"]
                    if results["missing_terms"]
                    else "No missing terms found."
                )

                # ----------------------------------
                # STEP 3: SKILL EXTRACTION
                # ----------------------------------

                resume_skills = extract_skills(resume_text)

                job_skills = extract_skills(job_description)

                # Flatten category-wise skills

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

                # Find matching and missing skills

                matched_skills = (
                    set(resume_skill_list)
                    & set(job_skill_list)
                )

                missing_skills = sorted(
                    set(job_skill_list)
                    - set(resume_skill_list)
                )

                # Calculate skill coverage

                if job_skill_list:

                    skill_coverage = (
                        len(matched_skills)
                        / len(set(job_skill_list))
                    ) * 100

                else:

                    skill_coverage = 0

                # ----------------------------------
                # STEP 4: SKILL ANALYSIS DISPLAY
                # ----------------------------------

                st.divider()

                st.header("2. Resume Skill Analysis")

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Resume Skills",
                        len(set(resume_skill_list))
                    )

                with col2:

                    st.metric(
                        "Required Skills",
                        len(set(job_skill_list))
                    )

                with col3:

                    st.metric(
                        "Skill Coverage",
                        f"{skill_coverage:.1f}%"
                    )

                st.progress(skill_coverage / 100)

                # Skills found in resume

                st.subheader("Skills Found in Resume")

                for category, skills in resume_skills.items():

                    if skills:

                        st.write(
                            f"**{category}:** {', '.join(skills)}"
                        )

                # Skills required by job

                st.subheader("Skills Required by Job")

                for category, skills in job_skills.items():

                    if skills:

                        st.write(
                            f"**{category}:** {', '.join(skills)}"
                        )

                # Missing skills

                st.subheader("Missing Skills")

                if missing_skills:

                    st.warning(
                        ", ".join(missing_skills)
                    )

                elif job_skill_list:

                    st.success(
                        "All detected required skills are present!"
                    )

                else:

                    st.info(
                        "No recognizable skills were detected "
                        "in the job description."
                    )

                # ----------------------------------
                # STEP 5: RESUME SECTION DETECTION
                # ----------------------------------

                detected_sections = detect_sections(resume_text)

                st.divider()

                st.header("3. Resume Structure Analysis")

                all_sections = [
                    "Summary",
                    "Education",
                    "Experience",
                    "Projects",
                    "Skills",
                    "Certifications",
                    "Achievements"
                ]

                for section in all_sections:

                    if section in detected_sections:

                        st.success(
                            f"{section} section detected"
                        )

                    else:

                        st.warning(
                            f"{section} section missing"
                        )

                # ----------------------------------
                # STEP 6: IMPROVEMENT SUGGESTIONS
                # ----------------------------------

                suggestions = generate_suggestions(
                    resume_text,
                    detected_sections,
                    missing_skills
                )

                st.divider()

                st.header("4. Resume Improvement Suggestions")

                if suggestions:

                    for index, suggestion in enumerate(
                        suggestions,
                        start=1
                    ):

                        st.info(
                            f"{index}. {suggestion}"
                        )

                else:

                    st.success(
                        "No basic improvement suggestions found."
                    )
                
                # ----------------------------------
                # STEP 7: DOWNLOAD PDF REPORT
                # ----------------------------------

                st.divider()

                st.header("5. Download Your Report")

                pdf_report = generate_pdf_report(
                    score=score,
                    matching_terms=results["matching_terms"],
                    missing_terms=results["missing_terms"],
                    resume_skills=resume_skills,
                    job_skills=job_skills,
                    missing_skills=missing_skills,
                    skill_coverage=skill_coverage,
                    detected_sections=detected_sections,
                    all_sections=all_sections,
                    suggestions=suggestions
                )

                st.download_button(
                    label="Download Analysis Report (PDF)",
                    data=pdf_report,
                    file_name="AI_Resume_Analysis_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "AI Resume Analyzer | Built with Python and Streamlit"
)

st.caption(
    "Note: Match percentages and recommendations are "
    "based on text similarity and rule-based analysis. "
    "They are not official ATS scores."
)