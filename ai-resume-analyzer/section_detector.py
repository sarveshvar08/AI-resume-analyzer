import re

SECTION_KEYWORDS = {
    "Summary": [
        "summary",
        "professional summary",
        "profile",
        "career objective",
        "objective"
    ],

    "Education": [
        "education",
        "academic background",
        "educational qualifications"
    ],

    "Experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "internship"
    ],

    "Projects": [
        "projects",
        "personal projects",
        "academic projects",
        "key projects"
    ],

    "Skills": [
        "skills",
        "technical skills",
        "core competencies",
        "technical expertise"
    ],

    "Certifications": [
        "certifications",
        "certificates",
        "licenses"
    ],

    "Achievements": [
        "achievements",
        "awards",
        "honors",
        "accomplishments"
    ]
}


def detect_sections(text):

    detected_sections = []

    lines = text.splitlines()

    for line in lines:

        heading = line.strip().lower()

        heading = re.sub(r"[^a-z\s]", "", heading)
        heading = " ".join(heading.split())

        for section, keywords in SECTION_KEYWORDS.items():

            if heading in keywords and section not in detected_sections:

                detected_sections.append(section)

    return detected_sections