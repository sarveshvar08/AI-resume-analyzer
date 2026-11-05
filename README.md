# AI Resume Analyzer

An intelligent resume analysis application that evaluates resumes against job descriptions, identifies skill gaps, analyzes resume structure, and generates actionable improvement suggestions.

Built using Python and Streamlit, this project aims to help job seekers understand how well their resumes align with specific job requirements.

## Overview

AI Resume Analyzer allows users to upload their resumes in PDF format and compare them against a target job description.

The application extracts resume content, calculates textual similarity, identifies relevant skills, detects missing keywords, evaluates resume structure, and generates a downloadable PDF analysis report.

## Features

### 1. Resume Upload and Text Extraction
- Upload resumes in PDF format.
- Extract text from multi-page PDFs.
- Clean extracted text for further processing.
- Support scanned PDFs through OCR.

### 2. Resume Match Analysis
- Compare resumes with job descriptions.
- Calculate textual similarity using TF-IDF.
- Apply cosine similarity to generate a match percentage.
- Identify matching and potentially missing keywords.

### 3. Skill Analysis
- Automatically identify technical skills.
- Organize skills into categories.
- Recognize common skill aliases.
- Compare resume skills against job requirements.
- Calculate skill coverage percentage.
- Highlight missing skills.

### 4. Resume Structure Analysis
Detect important resume sections:
- Professional Summary
- Education
- Experience
- Projects
- Skills
- Certifications
- Achievements

### 5. Resume Improvement Suggestions
Generate recommendations based on:
- Missing resume sections.
- Missing job-related skills.
- Use of action verbs.
- Resume length.
- Measurable achievements.
- Contact information.

### 6. Candidate Profile Extraction
Extract structured information such as:
- Candidate name (heuristic detection).
- Email address.
- Phone number.
- Education details.
- Graduation years.
- Experience duration.
- Technical skills.

### 7. PDF Analysis Report
Generate downloadable reports containing:
- Resume match percentage.
- Keyword analysis.
- Skill analysis.
- Missing skills.
- Resume structure.
- Improvement suggestions.

### 8. Dashboard Interface
- Streamlit-based dashboard.
- Resume analysis overview.
- Progress indicators.
- Organized analysis tabs.
- PDF report download.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| PyMuPDF | PDF text extraction |
| Scikit-learn | TF-IDF and cosine similarity |
| Pytesseract | OCR integration |
| Tesseract OCR | Text recognition from scanned documents |
| Pillow | Image processing |
| Regular Expressions | Skill and information extraction |
| ReportLab | PDF report generation |
| Pandas | Data handling |

## Project Architecture

```text
ai-resume-analyzer/
│
├── app.py
│
├── resume_parser.py
├── analyzer.py
├── skill_extractor.py
├── section_detector.py
├── improvement_suggestions.py
├── report_generator.py
├── profile_extractor.py
│
├── requirements.txt
├── README.md
├── .gitignore
│
└── .venv/
```

### Module Description

| File | Responsibility |
|---|---|
| `app.py` | Main Streamlit application |
| `resume_parser.py` | PDF extraction, OCR and contact extraction |
| `analyzer.py` | Resume-job similarity calculation |
| `skill_extractor.py` | Technical skill identification |
| `section_detector.py` | Resume section detection |
| `improvement_suggestions.py` | Resume improvement recommendations |
| `report_generator.py` | PDF report generation |
| `profile_extractor.py` | Structured candidate profile extraction |

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git
- Tesseract OCR
- A GitHub account (for deployment)

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
```

Navigate into the project directory:

```bash
cd ai-resume-analyzer
```

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Tesseract OCR

Install the Tesseract OCR engine separately.

On Windows, download and install Tesseract OCR, then configure its executable path if it is not available through PATH.

For Linux-based deployment, install the system package:

```bash
sudo apt-get install tesseract-ocr
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

Default local address:

```text
http://localhost:8501
```

## How to Use

1. Open the AI Resume Analyzer application.
2. Upload your resume in PDF format.
3. Paste the target job description.
4. Click **Analyze Resume**.
5. Review the resume match percentage.
6. Explore matching and missing keywords.
7. Check skill coverage and missing skills.
8. Review resume structure.
9. Read the improvement suggestions.
10. Download the PDF analysis report.

## How It Works

### Resume Text Extraction

PyMuPDF extracts text from PDF documents.

For scanned PDFs, the application uses Tesseract OCR to recognize text from page images.

### TF-IDF

Term Frequency-Inverse Document Frequency converts resume and job-description text into numerical vectors.

It gives greater importance to terms that are relatively distinctive within the analyzed documents.

### Cosine Similarity

Cosine similarity measures the similarity between the resume and job-description vectors.

The result is converted into a percentage:

```python
match_percentage = cosine_similarity * 100
```

This percentage represents textual similarity, not an official ATS score.

### Skill Extraction

A predefined skill dictionary and regular expressions identify technical skills and their aliases.

Detected skills are categorized and compared against the job description.

### Resume Structure Detection

Rule-based heading detection identifies common resume sections.

### Improvement Suggestions

A rule-based recommendation engine evaluates basic resume characteristics and provides suggestions.

## Deployment

The application can be deployed using Streamlit Community Cloud.

1. Push the project to GitHub.
2. Sign in to Streamlit Community Cloud using GitHub.
3. Select the repository.
4. Choose `main` as the branch.
5. Set `app.py` as the main application file.
6. Deploy the application.

For Linux-based OCR deployment, include the following in `packages.txt`:

```text
tesseract-ocr
```

Make sure the Tesseract executable configuration supports the deployment environment.

## Current Limitations

- The match percentage is based on textual similarity, not a certified ATS evaluation.
- Skill extraction depends on a predefined dictionary.
- Semantic equivalence between different descriptions is not fully supported.
- Resume section detection uses rule-based heading recognition.
- Candidate name and education extraction are heuristic and may not work with every resume format.
- OCR accuracy depends on document quality.
- Contact information extraction may occasionally produce false positives.
- The application does not predict hiring decisions.

## Future Improvements

- Semantic similarity using sentence embeddings.
- More comprehensive skill recognition.
- Improved candidate name and education extraction.
- Better handling of complex PDF layouts.
- Advanced resume recommendations.
- Improved OCR accuracy and multilingual support.
- Persistent analysis history.
- User authentication and database integration.
- Enhanced dashboard visualizations.

## Privacy and Security

Resumes may contain personal information such as names, email addresses, phone numbers, and employment history.

Users should upload documents only to trusted deployments.

The current application is designed for analysis during a session and does not intentionally provide permanent resume storage. However, uploaded files and processing data may be handled by the hosting platform. Review the hosting provider's privacy and retention policies before using real personal documents.

## Learning Outcomes

This project demonstrates practical implementation of:

- Python application development.
- PDF processing.
- Optical Character Recognition.
- Natural Language Processing fundamentals.
- Text vectorization.
- Cosine similarity.
- Regular expressions.
- Rule-based information extraction.
- Streamlit application development.
- PDF generation.
- Git and GitHub workflows.
- Cloud deployment.

## License

This project is available under the MIT License.

You can add a `LICENSE` file to the repository to formally apply this license.

---

**AI Resume Analyzer**

Built with Python and Streamlit.