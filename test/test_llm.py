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

from modules.llm import generate_answer

question = """
Explain Artificial Intelligence in simple terms.
"""

answer = generate_answer(question)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print("=" * 50)
print(answer)