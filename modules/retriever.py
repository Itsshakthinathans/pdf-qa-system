import numpy as np

def retrieve_chunks(
        question_embedding,
        index,
        chunks,
        top_k=2
):

    distances, indices = index.search(
        np.array([question_embedding]).astype("float32"),
        top_k
    )

    results = []

    for idx in indices[0]:
        results.append(chunks[idx])

    return results