import re

from resume_parser import extract_contact_info
from skill_extractor import extract_skills
from section_detector import detect_sections


# ==========================================
# DEGREE DATABASE
# ==========================================

DEGREE_KEYWORDS = [
    "Bachelor of Technology",
    "B.Tech",
    "B.E.",
    "Bachelor of Engineering",
    "Bachelor of Science",
    "B.Sc",
    "BCA",
    "Master of Technology",
    "M.Tech",
    "M.E.",
    "Master of Science",
    "M.Sc",
    "MCA",
    "MBA",
    "Ph.D",
    "PhD",
    "Diploma"
]


# ==========================================
# NAME EXTRACTION
# ==========================================

def extract_name(text):

    lines = text.splitlines()

    ignored_words = [
        "resume",
        "curriculum vitae",
        "profile",
        "summary",
        "education",
        "experience",
        "projects",
        "skills",
        "objective"
    ]

    for line in lines[:10]:

        line = line.strip()

        if not line:
            continue

        if any(word in line.lower() for word in ignored_words):
            continue

        if re.search(r"[@\d]|https?://|www\.", line, re.IGNORECASE):
            continue

        words = line.split()

        if 2 <= len(words) <= 4:

            if all(
                re.fullmatch(r"[A-Za-z][A-Za-z'-]*", word)
                for word in words
            ):

                return line

    return "Not detected"


# ==========================================
# EDUCATION EXTRACTION
# ==========================================

def extract_education(text):

    education = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        for degree in DEGREE_KEYWORDS:

            if re.search(
                re.escape(degree),
                line,
                re.IGNORECASE
            ):

                if line not in education:
                    education.append(line)

                break

    return education


# ==========================================
# GRADUATION YEAR EXTRACTION
# ==========================================

def extract_graduation_years(text):

    year_pattern = r"\b(?:19|20)\d{2}\b"

    years = re.findall(
        year_pattern,
        text
    )

    return sorted(set(years))


# ==========================================
# EXPERIENCE DURATION EXTRACTION
# ==========================================

def extract_experience_duration(text):

    patterns = [
        r"\b\d+(?:\.\d+)?\+?\s*(?:years?|yrs?)\b",
        r"\b\d+\s*(?:months?|mos?)\b"
    ]

    durations = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        durations.extend(matches)

    return list(set(durations))


# ==========================================
# EXPERIENCE SECTION EXTRACTION
# ==========================================

def extract_experience_details(text):

    lines = text.splitlines()

    experience_lines = []

    inside_experience = False

    experience_headings = [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "internship"
    ]

    other_headings = [
        "education",
        "projects",
        "skills",
        "certifications",
        "achievements",
        "summary",
        "objective"
    ]

    for line in lines:

        cleaned_line = line.strip()

        heading = re.sub(
            r"[^a-z\s]",
            "",
            cleaned_line.lower()
        )

        heading = " ".join(heading.split())

        if heading in experience_headings:

            inside_experience = True
            continue

        if heading in other_headings:

            inside_experience = False
            continue

        if inside_experience and cleaned_line:

            experience_lines.append(cleaned_line)

    return experience_lines[:20]


# ==========================================
# COMPLETE CANDIDATE PROFILE
# ==========================================

def extract_candidate_profile(text):

    contact_info = extract_contact_info(text)

    profile = {

        "name": extract_name(text),

        "emails": contact_info["emails"],

        "phone_numbers": contact_info["phone_numbers"],

        "education": extract_education(text),

        "graduation_years": extract_graduation_years(text),

        "experience_duration": extract_experience_duration(text),

        "experience_details": extract_experience_details(text),

        "skills": extract_skills(text),

        "sections": detect_sections(text)

    }

    return profile