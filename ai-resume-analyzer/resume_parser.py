import fitz
import re
import os
import pytesseract
import unicodedata

from PIL import Image
from io import BytesIO


# ==========================================
# TESSERACT CONFIGURATION
# ==========================================

TESSERACT_PATH = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# ==========================================
# TEXT CLEANING
# ==========================================

def clean_text(text):

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove control characters but preserve Unicode text
    text = "".join(
        char for char in text
        if char in "\n\t" or unicodedata.category(char) != "Cc"
    )

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ==========================================
# OCR FUNCTION
# ==========================================

def extract_text_using_ocr(page):

    try:

        # Render PDF page into an image
        pixmap = page.get_pixmap(
            matrix=fitz.Matrix(2, 2),
            alpha=False
        )

        image_bytes = pixmap.tobytes("png")

        image = Image.open(
            BytesIO(image_bytes)
        )

        # Recognize text using Tesseract
        extracted_text = pytesseract.image_to_string(
            image,
            lang="eng",
            config="--psm 6"
        )

        return extracted_text.strip()

    except Exception as error:

        print("OCR extraction error:", error)

        return None


# ==========================================
# PDF TEXT EXTRACTION
# ==========================================

def extract_resume_text(pdf_file):

    try:

        pdf_bytes = pdf_file.getvalue()

        extracted_pages = []

        with fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        ) as document:

            for page_number, page in enumerate(
                document,
                start=1
            ):

                # First try normal text extraction
                page_text = page.get_text(
                    "text",
                    sort=True
                )

                # If very little text exists, use OCR
                if len(page_text.strip()) < 40:

                    print(
                        f"Page {page_number}: Using OCR"
                    )

                    ocr_text = extract_text_using_ocr(page)

                    if ocr_text:
                        page_text = ocr_text

                extracted_pages.append(page_text)

        # Combine all pages
        extracted_text = "\n".join(extracted_pages)

        # Clean extracted text
        extracted_text = clean_text(extracted_text)

        if not extracted_text:
            return None

        return extracted_text

    except Exception as error:

        print("PDF extraction error:", error)

        return None


# ==========================================
# EMAIL EXTRACTION
# ==========================================

def extract_email(text):

    email_pattern = (
        r"[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}"
    )

    emails = re.findall(
        email_pattern,
        text
    )

    return list(set(emails))


# ==========================================
# PHONE NUMBER EXTRACTION
# ==========================================

def extract_phone_numbers(text):

    phone_pattern = (
        r"(?<!\d)"
        r"(?:\+?\d{1,3}[\s.-]?)?"
        r"(?:\d[\s.-]?){9,12}"
        r"(?!\d)"
    )

    numbers = re.findall(
        phone_pattern,
        text
    )

    valid_numbers = []

    for number in numbers:

        digits = re.sub(
            r"\D",
            "",
            number
        )

        if 10 <= len(digits) <= 13:

            if digits not in valid_numbers:
                valid_numbers.append(digits)

    return valid_numbers


# ==========================================
# CONTACT INFORMATION
# ==========================================

def extract_contact_info(text):

    return {
        "emails": extract_email(text),
        "phone_numbers": extract_phone_numbers(text)
    }