import os

from agents import OpenAIChatCompletionsModel, RunConfig

from provider_config import get_run_config


def test_provider_defaults_to_openai(monkeypatch):
    monkeypatch.delenv("AGENT_PROVIDER", raising=False)
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    assert get_run_config() is None


def test_groq_provider_uses_configured_model(monkeypatch):
    monkeypatch.setenv("AGENT_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.setenv("GROQ_MODEL", "test-model")

    config = get_run_config()

    assert isinstance(config, RunConfig)
    assert isinstance(config.model, OpenAIChatCompletionsModel)
    assert config.model.model == "test-model"
    assert config.tracing_disabled


def test_groq_key_prompt_stores_key_in_groq_variable(monkeypatch):
    from lab_launcher import ask_for_api_key

    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr("getpass.getpass", lambda _: "test-groq-key")

    assert ask_for_api_key("GROQ_API_KEY", "Groq") == "test-groq-key"
    assert os.getenv("GROQ_API_KEY") == "test-groq-key"
    assert os.getenv("OPENAI_API_KEY") is None