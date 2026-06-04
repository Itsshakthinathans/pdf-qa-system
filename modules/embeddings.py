from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

def generate_embeddings(chunks, is_query=False):
    if isinstance(chunks, str):
        processed = f"Represent this sentence for searching relevant passages: {chunks}" if is_query else chunks
    else:
        processed = [f"Represent this sentence for searching relevant passages: {c}" for c in chunks] if is_query else chunks

    embeddings = model.encode(processed, normalize_embeddings=True)
    return embeddings