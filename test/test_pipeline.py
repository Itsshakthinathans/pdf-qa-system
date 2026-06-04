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

from qa_pipeline import ask_pdf_question

pdf_path = "data/pdfs/sample.pdf"

question = "What is reinforcement learning?"

result = ask_pdf_question(
    pdf_path,
    question
)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print("=" * 50)
print(result["answer"])

print("\nSOURCES:")
print("=" * 50)
print(result["source_label"])