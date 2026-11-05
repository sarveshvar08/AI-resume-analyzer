import re

SKILL_CATEGORIES = {
    "Programming Languages": [
        "Python",
        "Java",
        "JavaScript",
        "C++"
    ],

    "Web Development": [
        "HTML",
        "CSS",
        "React",
        "Node.js",
        "Streamlit",
        "FastAPI"
    ],

    "Databases": [
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "Firebase"
    ],

    "AI & Machine Learning": [
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "TensorFlow",
        "PyTorch",
        "Scikit-learn"
    ],

    "Tools & Platforms": [
        "Git",
        "GitHub",
        "Docker",
        "Linux",
        "AWS",
        "Azure"
    ]
}


def extract_skills(text):

    detected_skills = {}

    for category, skills in SKILL_CATEGORIES.items():

        found_skills = []

        for skill in skills:

            pattern = (
                r"(?<![A-Za-z0-9_])"
                + re.escape(skill)
                + r"(?![A-Za-z0-9_])"
            )

            if re.search(pattern, text, re.IGNORECASE):
                found_skills.append(skill)

        detected_skills[category] = found_skills

    return detected_skills