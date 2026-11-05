import fitz


def extract_resume_text(pdf_file):

    try:
        # Open uploaded PDF
        document = fitz.open(stream=pdf_file.read(), filetype="pdf")

        extracted_text = ""

        # Extract text from every page
        for page in document:
            extracted_text += page.get_text()

        document.close()

        return extracted_text.strip()

    except Exception as error:
        print("PDF extraction error:", error)
        return None