from modules.retriever import retrieve_chunks
from modules.embeddings import generate_embeddings
from modules.llm import generate_answer

import time


def ask_question(question, chunks, index):

    start = time.time()

    question_embedding = generate_embeddings(
        [question]
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

    context = "\n\n".join(
        relevant_chunks
    )

    prompt = f"""
You are a PDF Question Answering Assistant.

Use ONLY the information provided in the context.

If the answer is not available in the context,
reply:
"The answer is not available in the uploaded PDF."

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

    return answer


def ask_pdf_question(pdf_path, question):
    """
    End-to-end question answering pipeline for a local PDF file.
    
    Parameters:
        pdf_path (str): Path to the PDF file.
        question (str): User query.
        
    Returns:
        str: Generated answer from LLM.
    """
    from modules.pdf_loader import extract_text
    from modules.chunker import create_chunks
    from modules.vector_store import create_faiss_index

    # 1. Extract text from PDF
    text = extract_text(pdf_path)
    
    # 2. Chunk text
    chunks = create_chunks(text)
    
    # 3. Generate embeddings
    embeddings = generate_embeddings(chunks)
    
    # 4. Index embeddings with FAISS
    index = create_faiss_index(embeddings)
    
    # 5. Ask question
    return ask_question(question, chunks, index)