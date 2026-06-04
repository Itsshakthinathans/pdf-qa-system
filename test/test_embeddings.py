import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from modules.pdf_loader import extract_text
from modules.chunker import create_chunks
from modules.embeddings import generate_embeddings

pdf_path = "data/pdfs/sample.pdf"

text = extract_text(pdf_path)

chunks = create_chunks(text)

embeddings = generate_embeddings(chunks)

print("Total Chunks:", len(chunks))
print("Total Embeddings:", len(embeddings))

print("\nEmbedding Shape:")
print(embeddings.shape)

print("\nFirst Embedding:")
print(embeddings[0])