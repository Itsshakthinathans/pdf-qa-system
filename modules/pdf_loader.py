import fitz


def extract_text(pdf_path):
    text = ""

    pdf_document = fitz.open(pdf_path)

    for page in pdf_document:
        text += page.get_text()

    pdf_document.close()

    return text