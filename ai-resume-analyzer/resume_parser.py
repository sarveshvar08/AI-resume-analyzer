import fitz
import re


# ==========================================
# TEXT CLEANING
# ==========================================

def clean_text(text):

    # Normalize line breaks
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove unwanted control characters
    text = re.sub(r"[^\x20-\x7E\n\t]", " ", text)

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ==========================================
# PDF TEXT EXTRACTION
# ==========================================

def extract_resume_text(pdf_file):

    try:

        # Read PDF without depending on file pointer position
        pdf_bytes = pdf_file.getvalue()

        document = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        extracted_pages = []

        # Extract text from every page
        for page_number, page in enumerate(document, start=1):

            page_text = page.get_text(
                "text",
                sort=True
            )

            if page_text.strip():

                extracted_pages.append(
                    page_text
                )

        document.close()

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

    # Normalize and validate candidates
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