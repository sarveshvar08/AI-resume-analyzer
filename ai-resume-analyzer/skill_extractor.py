import re


SKILL_CATEGORIES = {

    "Programming Languages": {
        "Python": ["Python"],
        "Java": ["Java"],
        "JavaScript": ["JavaScript", "JS"],
        "C++": ["C++"]
    },

    "Web Development": {
        "HTML": ["HTML", "HTML5"],
        "CSS": ["CSS", "CSS3"],
        "React": ["React", "React.js"],
        "Node.js": ["Node.js", "NodeJS"],
        "Streamlit": ["Streamlit"],
        "FastAPI": ["FastAPI"]
    },

    "Databases": {
        "SQL": ["SQL"],
        "MySQL": ["MySQL"],
        "PostgreSQL": ["PostgreSQL", "Postgres"],
        "MongoDB": ["MongoDB"],
        "Firebase": ["Firebase"]
    },

    "AI & Machine Learning": {
        "Machine Learning": ["Machine Learning", "ML"],
        "Deep Learning": ["Deep Learning", "DL"],
        "Natural Language Processing": [
            "Natural Language Processing",
            "NLP"
        ],
        "TensorFlow": ["TensorFlow"],
        "PyTorch": ["PyTorch"],
        "Scikit-learn": [
            "Scikit-learn",
            "sklearn",
            "Scikit learn"
        ]
    },

    "Tools & Platforms": {
        "Git": ["Git"],
        "GitHub": ["GitHub"],
        "Docker": ["Docker"],
        "Linux": ["Linux"],
        "Amazon Web Services": ["AWS", "Amazon Web Services"],
        "Azure": ["Azure"]
    }
}


def contains_skill(text, aliases):

    for alias in aliases:

        pattern = (
            r"(?<![A-Za-z0-9_])"
            + re.escape(alias)
            + r"(?![A-Za-z0-9_])"
        )

        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


def extract_skills(text):

    detected_skills = {}

    for category, skills in SKILL_CATEGORIES.items():

        found_skills = []

        for canonical_name, aliases in skills.items():

            if contains_skill(text, aliases):

                found_skills.append(canonical_name)

        detected_skills[category] = found_skills

    return detected_skills