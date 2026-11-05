import re


def generate_suggestions(
    resume_text,
    detected_sections,
    missing_skills
):

    suggestions = []

    resume_lower = resume_text.lower()

    # 1. Check important resume sections
    important_sections = [
        "Summary",
        "Education",
        "Experience",
        "Projects",
        "Skills"
    ]

    for section in important_sections:

        if section not in detected_sections:
            suggestions.append(
                f"Consider adding a {section} section to your resume."
            )

    # 2. Check measurable achievements
    numbers = re.findall(r"\b\d+%?\b", resume_text)

    if len(numbers) < 3:
        suggestions.append(
            "Add measurable achievements using numbers, "
            "percentages, or other results."
        )

    # 3. Check action verbs
    action_verbs = [
        "developed",
        "created",
        "implemented",
        "designed",
        "managed",
        "improved",
        "built",
        "optimized"
    ]

    if not any(
        verb in resume_lower
        for verb in action_verbs
    ):
        suggestions.append(
            "Use strong action verbs to describe your work and projects."
        )

    # 4. Check resume length
    word_count = len(resume_text.split())

    if word_count < 150:
        suggestions.append(
            "Your resume appears short. Add relevant details "
            "about your education, projects, and experience."
        )

    elif word_count > 1000:
        suggestions.append(
            "Your resume may be lengthy. Consider removing "
            "unnecessary or repetitive information."
        )

    # 5. Check missing job-related skills
    if missing_skills:

        suggestions.append(
            "Consider highlighting relevant skills you genuinely "
            "possess but have not mentioned: "
            + ", ".join(missing_skills)
        )

    # 6. Check contact information
    email_pattern = r"[\w.+-]+@[\w-]+\.[\w.-]+"

    if not re.search(email_pattern, resume_text):
        suggestions.append(
            "Add a valid professional email address."
        )

    if not suggestions:
        suggestions.append(
            "Your resume passed these basic checks. "
            "Continue tailoring it to each job description."
        )

    return suggestions