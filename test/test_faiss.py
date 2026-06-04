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
from modules.vector_store import create_faiss_index

pdf_path = "data/pdfs/sample.pdf"

pages = extract_text(pdf_path)

chunks = create_chunks(pages)

chunk_texts = [c["text"] for c in chunks]
embeddings = generate_embeddings(chunk_texts)

index = create_faiss_index(embeddings)

print("Chunks:", len(chunks))
print("Embeddings:", len(embeddings))
print("Vectors Stored:", index.ntotal)