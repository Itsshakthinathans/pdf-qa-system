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

text = extract_text(pdf_path)

print("=" * 50)
print("PDF CONTENT")
print("=" * 50)

print(text[:1000])

print("\nTotal Characters:", len(text))