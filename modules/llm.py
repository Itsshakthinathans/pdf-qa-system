import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "deepseek-r1:7b"
# MODEL_NAME = "deepseek-r1:1.5b"

def generate_answer(prompt):
    print("Using Model:", MODEL_NAME)
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.0
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload
    )

    result = response.json()
    # print(result)
    return result["response"]