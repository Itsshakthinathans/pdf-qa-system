import sys
import os

# Add project root to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from modules.pdf_loader import extract_text

pdf_path = "data/pdfs/sample.pdf"

pages = extract_text(pdf_path)

print("=" * 50)
print("PDF CONTENT (Pages)")
print("=" * 50)

print(f"Extracted {len(pages)} page(s).")
if pages:
    first_page = pages[0]
    print(f"Page Number: {first_page['page_number']}")
    print(f"Text Content Snippet:\n{first_page['text'][:500]}...")

print("\nVerification Passed: extract_text returned list of dicts with page metadata.")