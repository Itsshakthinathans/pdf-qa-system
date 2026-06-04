import fitz


def extract_text(pdf_path):
    pages = []

    pdf_document = fitz.open(pdf_path)

    for page in pdf_document:
        text = page.get_text()
        if text.strip():
            pages.append({
                "text": text,
                "page_number": page.number + 1
            })

    pdf_document.close()

    return pages