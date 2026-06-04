import streamlit as st
import tempfile

from modules.pdf_loader import extract_text
from modules.chunker import create_chunks
from modules.embeddings import generate_embeddings
from modules.vector_store import create_faiss_index

from qa_pipeline import ask_question

st.set_page_config(
    page_title="PDF QA System",
    layout="wide"
)

st.title("📄 PDF Question Answering System")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    # Process PDF only once
    if (
        "index" not in st.session_state
        or
        st.session_state.get("pdf_name") != uploaded_file.name
    ):

        with st.spinner(
            "Processing PDF..."
        ):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_file.write(
                    uploaded_file.read()
                )

                pdf_path = temp_file.name

            text = extract_text(
                pdf_path
            )

            chunks = create_chunks(
                text
            )

            chunk_texts = [c["text"] for c in chunks]
            embeddings = generate_embeddings(
                chunk_texts
            )

            index = create_faiss_index(
                embeddings
            )

            st.session_state.chunks = chunks
            st.session_state.index = index
            st.session_state.pdf_name = uploaded_file.name

        st.success(
            "PDF processed successfully!"
        )

    question = st.text_input(
        "Enter your question:"
    )

    if st.button("Ask"):

        if question:

            with st.spinner(
                "Generating answer..."
            ):

                result = ask_question(
                    question,
                    st.session_state.chunks,
                    st.session_state.index
                )

            st.subheader(
                "Answer"
            )

            st.write(
                result["answer"]
            )

            st.divider()
            st.caption(
                f"**Sources Referenced:** {result['source_label']}"
            )

        else:

            st.warning(
                "Please enter a question."
            )