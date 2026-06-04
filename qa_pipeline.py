from modules.retriever import retrieve_chunks
from modules.embeddings import generate_embeddings
from modules.llm import generate_answer

import time


def ask_question(question, chunks, index):

    start = time.time()

    # Pass is_query=True to prep the question for BGE
    question_embedding = generate_embeddings(
        [question],
        is_query=True
    )[0]

    print(
        "Question Embedding Time:",
        round(time.time() - start, 2),
        "seconds"
    )

    start = time.time()

    relevant_chunks = retrieve_chunks(
        question_embedding,
        index,
        chunks,
        top_k=3
    )

    print(
        "Retrieval Time:",
        round(time.time() - start, 2),
        "seconds"
    )

    # Format the context to include page number annotations
    context_parts = []
    unique_pages = set()
    for chunk in relevant_chunks:
        text = chunk["text"]
        pages = chunk["page_numbers"]
        unique_pages.update(pages)
        pages_str = ", ".join(map(str, pages))
        context_parts.append(f"[Source Page(s): {pages_str}]\n{text}")

    context = "\n\n".join(context_parts)
    sorted_pages = sorted(list(unique_pages))
    
    print("Retrieved Chunks:", len(relevant_chunks))
    print("Context Length:", len(context))

    prompt = f"""You are a precise PDF Question Answering Assistant.

Analyze the provided Context (which includes Page Numbers) to answer the user's Question.

CRITICAL INSTRUCTIONS:
1. Base your answer ONLY on the provided Context. Do NOT use any external knowledge.
2. For every fact, claim, or piece of information you retrieve, cite the exact source page(s) using the format [Page X] or [Pages X, Y] inline immediately after the statement (e.g., "...this process takes five minutes [Page 2].").
3. Do NOT make up any citations. Only use the page numbers explicitly stated in the context.
4. If the answer cannot be fully found in the context, or if the context is insufficient, reply exactly:
"The answer is not available in the uploaded PDF."
5. Do NOT say "Based on the context..." or "According to the provided document..." at the beginning. Just answer directly and include the citations.

Context:
{context}

Question:
{question}

Answer:
"""

    start = time.time()

    answer = generate_answer(prompt)

    print(
        "DeepSeek Time:",
        round(time.time() - start, 2),
        "seconds"
    )

    return {
        "answer": answer.strip(),
        "sources": sorted_pages,
        "source_label": f"Pages: {', '.join(map(str, sorted_pages))}" if sorted_pages else "Unknown"
    }


def ask_pdf_question(pdf_path, question):
    """
    End-to-end question answering pipeline for a local PDF file.
    
    Parameters:
        pdf_path (str): Path to the PDF file.
        question (str): User query.
        
    Returns:
        dict: Generated answer dictionary with answer, sources, and source_label.
    """
    from modules.pdf_loader import extract_text
    from modules.chunker import create_chunks
    from modules.vector_store import create_faiss_index

    # 1. Extract text from PDF
    text = extract_text(pdf_path)
    
    # 2. Chunk text
    chunks = create_chunks(text)
    
    # 3. Generate embeddings (extract texts from dict list)
    chunk_texts = [c["text"] for c in chunks]
    embeddings = generate_embeddings(chunk_texts)
    
    # 4. Index embeddings with FAISS
    index = create_faiss_index(embeddings)
    
    # 5. Ask question
    return ask_question(question, chunks, index)
