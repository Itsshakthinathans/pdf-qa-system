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
from modules.retriever import retrieve_chunks

pdf_path = "data/pdfs/sample.pdf"

pages = extract_text(pdf_path)

chunks = create_chunks(pages)

chunk_texts = [c["text"] for c in chunks]
embeddings = generate_embeddings(chunk_texts)

index = create_faiss_index(embeddings)

question = "What are the advantages of AI?"

question_embedding = generate_embeddings(
    [question],
    is_query=True
)[0]

results = retrieve_chunks(
    question_embedding,
    index,
    chunks
)

print("\nQuestion:")
print(question)

print("\nRetrieved Chunks:")
print("=" * 50)

for i, chunk in enumerate(results):
    print(f"\nResult {i+1}")
    print("-" * 50)
    print(f"Source Pages: {chunk['page_numbers']}")
    print(chunk['text'])