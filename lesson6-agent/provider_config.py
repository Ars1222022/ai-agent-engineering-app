"""Select an optional OpenAI-compatible model provider for agent examples."""

import os

from agents import OpenAIChatCompletionsModel, RunConfig
from openai import AsyncOpenAI


def get_run_config() -> RunConfig | None:
    """Use Groq when selected; otherwise keep the SDK's normal OpenAI defaults."""
    if os.getenv("AGENT_PROVIDER", "openai").lower() != "groq":
        return None

    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing. Choose Groq again and enter its API key.")

    model_name = os.getenv("GROQ_MODEL", "").strip()
    if not model_name:
        raise RuntimeError("GROQ_MODEL is missing. Choose a currently available model from Groq's model catalog.")

    client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )
    model = OpenAIChatCompletionsModel(
        model=model_name,
        openai_client=client,
    )
    return RunConfig(model=model, tracing_disabled=True)