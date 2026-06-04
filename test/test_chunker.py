import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.pdf_loader import extract_text
from modules.chunker import create_chunks

pdf_path = "data/pdfs/sample.pdf"

text = extract_text(pdf_path)

chunks = create_chunks(text)

print("=" * 50)
print("TOTAL CHUNKS:", len(chunks))
print("=" * 50)

for i, chunk in enumerate(chunks):
    print(f"\nCHUNK {i + 1}")
    print("-" * 50)
    print(chunk)