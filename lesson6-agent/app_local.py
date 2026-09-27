"""
Lektion 6 — Testa LM Studio fran Python i VS Code
"""

import os

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
print(f"Anvander modell: {model_id}")


client = OpenAI(
    base_url=base_url,
    api_key="lm-studio"
)


response = client.chat.completions.create(
    model=model_id,
    messages=[
        {"role": "user", "content": "Explain what an AI agent is in two sentences."}
    ]
)

print(response.choices[0].message.content)
