"""
Lektion 6 — Minimal RAG-demo.
Enkel keyword retrieval. Riktig RAG kommer i L7.
"""

import os
from pathlib import Path

import requests
from openai import OpenAI


base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")


models_response = requests.get(
    f"{base_url}/models",
    timeout=5,
)
models_response.raise_for_status()

models = models_response.json().get("data", [])
if not models:
    raise RuntimeError("LM Studio kors men ingen modell ar tillganglig.")

model_id = models[0]["id"]

client = OpenAI(
    base_url=base_url,
    api_key="lm-studio"
)


knowledge_file = Path(__file__).resolve().parent / "knowledge" / "course_notes.txt"
with knowledge_file.open("r", encoding="utf-8") as f:
    document = f.read()


def retrieve_relevant_text(query: str, text: str) -> str:
    """Enkel retrieval — hitta rader som innehaller query."""
    lines = text.split("\n")

    relevant_lines = [
        line for line in lines
        if query.lower() in line.lower()
    ]

    return "\n".join(relevant_lines) if relevant_lines else text


query = "RAG"
context = retrieve_relevant_text(query, document)

response = client.chat.completions.create(
    model=model_id,
    messages=[
        {
            "role": "system",
            "content": f"Use this context to answer:\n\n{context}"
        },
        {
            "role": "user",
            "content": f"What is {query}?"
        }
    ]
)

print(response.choices[0].message.content)
