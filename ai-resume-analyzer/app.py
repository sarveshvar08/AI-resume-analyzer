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
# Initialize session state

if "show_results" not in st.session_state:
    st.session_state["show_results"] = False

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1 {
    color: #172554;
    font-weight: 750;
}

h2, h3 {
    color: #1e3a8a;
}

.metric-card {
    background-color: white;
    padding: 22px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.header-box {
    background: linear-gradient(120deg, #1e3a8a, #2563eb);
    padding: 30px;
    border-radius: 15px;
    color: white;
    margin-bottom: 25px;
}

.header-box h1 {
    color: white;
}

.header-box p {
    color: #dbeafe;
    font-size: 16px;
}

div[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
}

.stButton button {
    border-radius: 8px;
    font-weight: 600;
}

.stDownloadButton button {
    border-radius: 8px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="header-box">
    <h1>AI Resume Analyzer</h1>
    <p>
        Analyze your resume, identify skill gaps,
        and improve your job application.
    </p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# INPUT SECTION
# ==========================================

st.subheader("Start Your Analysis")

col1, col2 = st.columns(2)

with col1:

    resume = st.file_uploader(
    "Upload your resume",
    type=["pdf"],
    help="Maximum file size: 5 MB."
)

if resume is not None and resume.size > 5 * 1024 * 1024:
    st.error("File is too large. Maximum allowed size is 5 MB.")
    resume = None

with col2:

    job_description = st.text_area(
        "Job Description",
        height=150,
        placeholder="Paste the job description here..."
    )


col1, col2 = st.columns(2)

with col1:
    analyze_button = st.button(
        "Analyze Resume",
        type="primary",
        use_container_width=True
    )

with col2:
    clear_button = st.button(
        "Clear Analysis",
        use_container_width=True
    )

if analyze_button:
    st.session_state["show_results"] = True

if clear_button:
    st.session_state["show_results"] = False
    st.rerun()


# ==========================================
# ANALYSIS
# ==========================================

if analyze_button:

    if resume is None:

        st.error("Please upload your resume.")

    elif not job_description.strip():

        st.error("Please enter a job description.")

    else:

        with st.spinner("Analyzing your resume..."):

            resume_text = extract_resume_text(resume)

            if not resume_text:

                st.error(
                    "Unable to extract text. "
                    "Please upload a valid text-based PDF."
                )

            else:

                # Resume similarity analysis

                results = analyze_resume(
                    resume_text,
                    job_description
                )

                score = results["match_percentage"]

                # Skill extraction

                resume_skills = extract_skills(resume_text)
                job_skills = extract_skills(job_description)

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

                matched_skills = (
                    set(resume_skill_list)
                    & set(job_skill_list)
                )

                missing_skills = sorted(
                    set(job_skill_list)
                    - set(resume_skill_list)
                )

                if job_skill_list:

                    skill_coverage = (
                        len(matched_skills)
                        / len(set(job_skill_list))
                    ) * 100

                else:

                    skill_coverage = 0

                # Section detection

                detected_sections = detect_sections(resume_text)

                all_sections = [
                    "Summary",
                    "Education",
                    "Experience",
                    "Projects",
                    "Skills",
                    "Certifications",
                    "Achievements"
                ]

                # Improvement suggestions

                suggestions = generate_suggestions(
                    resume_text,
                    detected_sections,
                    missing_skills
                )

                st.success("Analysis completed successfully!")

                st.divider()


                # ==================================
                # DASHBOARD METRICS
                # ==================================

                st.header("Analysis Overview")

                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    st.metric(
                        "Resume Match",
                        f"{score}%"
                    )

                with col2:

                    st.metric(
                        "Skill Coverage",
                        f"{skill_coverage:.1f}%"
                    )

                with col3:

                    st.metric(
                        "Matching Skills",
                        len(matched_skills)
                    )

                with col4:

                    st.metric(
                        "Missing Skills",
                        len(missing_skills)
                    )


                # ==================================
                # PROGRESS VISUALIZATION
                # ==================================

                col1, col2 = st.columns(2)

                with col1:

                    st.subheader("Resume Match")

                    st.progress(
                        max(0.0, min(score / 100, 1.0))
                    )

                    st.caption(
                        "Text similarity between resume and job description."
                    )

                with col2:

                    st.subheader("Skill Coverage")

                    st.progress(
                        skill_coverage / 100
                    )

                    st.caption(
                        "Percentage of detected job skills found in your resume."
                    )


                st.divider()


                # ==================================
                # ANALYSIS TABS
                # ==================================

                tab1, tab2, tab3, tab4 = st.tabs([
                    "Keyword Analysis",
                    "Skill Analysis",
                    "Resume Structure",
                    "Suggestions"
                ])


                # ==================================
                # TAB 1: KEYWORDS
                # ==================================

                with tab1:

                    st.subheader("Matching Keywords")

                    if results["matching_terms"]:

                        st.success(
                            ", ".join(results["matching_terms"])
                        )

                    else:

                        st.info("No matching keywords found.")

                    st.subheader("Potentially Missing Keywords")

                    if results["missing_terms"]:

                        st.warning(
                            ", ".join(results["missing_terms"])
                        )

                    else:

                        st.success("No missing keywords detected.")


                # ==================================
                # TAB 2: SKILLS
                # ==================================

                with tab2:

                    col1, col2 = st.columns(2)

                    with col1:

                        st.subheader("Resume Skills")

                        for category, skills in resume_skills.items():

                            if skills:

                                with st.expander(category, expanded=True):

                                    for skill in skills:

                                        st.write(f"✓ {skill}")

                    with col2:

                        st.subheader("Job Requirements")

                        for category, skills in job_skills.items():

                            if skills:

                                with st.expander(category, expanded=True):

                                    for skill in skills:

                                        if skill in matched_skills:

                                            st.write(f"✓ {skill}")

                                        else:

                                            st.write(f"✗ {skill}")

                    st.divider()

                    st.subheader("Missing Skills")

                    if missing_skills:

                        st.warning(
                            ", ".join(missing_skills)
                        )

                    elif job_skill_list:

                        st.success(
                            "All detected required skills are present."
                        )

                    else:

                        st.info(
                            "No recognizable skills found in the job description."
                        )


                # ==================================
                # TAB 3: RESUME STRUCTURE
                # ==================================

                with tab3:

                    st.subheader("Resume Section Detection")

                    for section in all_sections:

                        if section in detected_sections:

                            st.success(
                                f"✓ {section} section detected"
                            )

                        else:

                            st.warning(
                                f"✗ {section} section missing"
                            )


                # ==================================
                # TAB 4: SUGGESTIONS
                # ==================================

                with tab4:

                    st.subheader("Improvement Recommendations")

                    for index, suggestion in enumerate(
                        suggestions,
                        start=1
                    ):

                        st.info(
                            f"{index}. {suggestion}"
                        )


                # ==================================
                # PDF REPORT DOWNLOAD
                # ==================================

                st.divider()

                st.header("Download Analysis Report")

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
                    label="Download PDF Report",
                    data=pdf_report,
                    file_name="AI_Resume_Analysis_Report.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#64748b;">
        <p><b>AI Resume Analyzer</b></p>
        <p>Built with Python, Streamlit and Scikit-learn.</p>
        <p>Resume analysis is indicative and not an official ATS assessment.</p>
    </div>
    """,
    unsafe_allow_html=True
)