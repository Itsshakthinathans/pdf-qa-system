import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "deepseek-r1:7b"


def generate_answer(prompt):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload
    )

    result = response.json()

    return result["response"]