import os
import subprocess
import sys
from importlib.util import find_spec
from pathlib import Path

import requests
from dotenv import load_dotenv


PROJECT_DIR = Path(__file__).resolve().parent
load_dotenv(PROJECT_DIR / ".env")

OPENAI_DEMOS = {
    "1": ("Basic agent", "app.py"),
    "2": ("Agent with tools", "app_tool.py"),
    "3": ("Structured output", "app_structured.py"),
    "4": ("Human approval", "app_hitl.py"),
    "5": ("Tool validation", "app_tool_validation.py"),
    "6": ("Input guardrail", "app_input_guardrail.py"),
    "7": ("MCP client and server", "app_mcp_client.py"),
}

GROQ_DEMOS = {
    "1": OPENAI_DEMOS["1"],
    "2": OPENAI_DEMOS["2"],
    "3": OPENAI_DEMOS["7"],
}

LOCAL_DEMOS = {
    "1": ("LM Studio connection test", "app_local.py"),
    "2": ("Keyword retrieval / RAG demo", "app_rag_demo.py"),
}
PLACEHOLDER_KEYS = {"your_openai_api_key_here", "your_key_here", "sk-..."}
REQUIRED_MODULES = {
    "agents": "openai-agents",
    "openai": "openai",
    "fastmcp": "fastmcp",
    "pytest": "pytest",
    "dotenv": "python-dotenv",
    "requests": "requests",
}


def banner():
    print("\n=== Lesson 6 — AI Agent Engineering ===")
    print("Start here to check setup, run tests, and launch lesson examples.")


def ask_for_api_key(variable, provider):
    key = os.getenv(variable)
    if key and key.strip() and key.strip().lower() not in PLACEHOLDER_KEYS:
        return key

    print(f"No {provider} key was found in the environment or .env file.")
    print("Paste it here when asked. Input is hidden and only kept for this session.")
    try:
        from getpass import getpass

        answer = getpass(f"{provider} API key (Enter to cancel): ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return None

    if answer:
        os.environ[variable] = answer
        return answer
    return None


def choose_from_demos(demos):
    while True:
        for number, (label, _) in demos.items():
            print(f"{number}) {label}")
        print("0) Back")
        choice = input("Choose an example: ").strip()
        if choice == "0":
            return None
        if choice in demos:
            return demos[choice][1]
        print("Please choose one of the listed numbers.")


def run_script(script):
    path = PROJECT_DIR / script
    if not path.is_file():
        print(f"MISSING: {script}. Restore it from the project files before running this example.")
        return

    print(f"\nStarting {script}...\n")
    result = subprocess.run([sys.executable, str(path)], cwd=PROJECT_DIR, check=False)
    if result.returncode:
        print(f"The example stopped with error code {result.returncode}. Read the message above.")


def missing_packages():
    return [
        package
        for module, package in REQUIRED_MODULES.items()
        if find_spec(module) is None
    ]


def explain_missing_packages(packages):
    if not packages:
        return
    print(f"Missing packages: {', '.join(packages)}")
    print("Install into this project's venv with start-lesson6.ps1 (Windows) or start-lesson6.sh (macOS/Linux).")
    print("If Windows reports a path-length error, choose Docker in the start script.")


def check_setup():
    print("\n=== Project check ===")
    print(f"Python: {sys.version.split()[0]} ({sys.executable})")

    missing = missing_packages()
    missing_set = set(missing)
    for module, package in REQUIRED_MODULES.items():
        print(f"{'MISSING' if package in missing_set else 'OK'} package: {package}")

    required_files = [
        "app.py", "app_tool.py", "app_structured.py", "app_hitl.py",
        "app_tool_validation.py", "app_input_guardrail.py", "app_mcp_client.py",
        "app_local.py", "app_rag_demo.py", "provider_config.py",
        "mcp_server/server.py", "knowledge/course_notes.txt",
    ]
    for relative_path in required_files:
        status = "OK" if (PROJECT_DIR / relative_path).is_file() else "MISSING"
        print(f"{status} file: {relative_path}")

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if api_key and api_key.lower() not in PLACEHOLDER_KEYS:
        print("OK OpenAI API key is configured (value hidden)")
    else:
        print("NOT CONFIGURED OpenAI key; only needed for OpenAI examples")

    groq_key = os.getenv("GROQ_API_KEY", "").strip()
    if groq_key and groq_key.lower() not in PLACEHOLDER_KEYS:
        print("OK Groq API key is configured (value hidden)")
    else:
        print("NOT CONFIGURED Groq key; optional alternative for selected agent examples")

    base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1").rstrip("/")
    try:
        response = requests.get(f"{base_url}/models", timeout=3)
        response.raise_for_status()
        models = response.json().get("data", [])
        if models:
            print(f"OK LM Studio reachable at {base_url}; model: {models[0].get('id', 'unknown')}")
        else:
            print(f"REACHABLE but no model is loaded at {base_url}")
    except (requests.RequestException, ValueError):
        print(f"NOT REACHABLE LM Studio at {base_url}")
        print("For local-model examples: start LM Studio, load a model, then start its server.")

    if missing:
        explain_missing_packages(missing)
        return False
    return True


def run_tests():
    missing = missing_packages()
    if missing:
        print("Tests were not run because this Python environment is incomplete.")
        explain_missing_packages(missing)
        return None

    print("\nRunning project tests...\n")
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q"], cwd=PROJECT_DIR, check=False
    ).returncode == 0


def cloud_menu():
    missing = missing_packages()
    if missing:
        explain_missing_packages(missing)
        return

    print("\nChoose a cloud API:")
    print("1) OpenAI: course default; needs an OpenAI key and may incur usage charges.")
    print("2) Groq: optional compatible API; needs a Groq key and model ID.")
    print("0) Back")
    provider_choice = input("Choose provider: ").strip()

    if provider_choice == "1":
        if not ask_for_api_key("OPENAI_API_KEY", "OpenAI"):
            print("No key provided; nothing was run.")
            return
        os.environ["AGENT_PROVIDER"] = "openai"
        demos = OPENAI_DEMOS
    elif provider_choice == "2":
        if not ask_for_api_key("GROQ_API_KEY", "Groq"):
            print("No key provided; nothing was run.")
            return
        default_model = os.getenv("GROQ_MODEL", "").strip()
        prompt = f"Groq model ID from the model catalog [{default_model}]: "
        model = input(prompt).strip() or default_model
        if not model:
            print("A Groq model ID is required. See https://console.groq.com/docs/models.")
            return
        os.environ["GROQ_MODEL"] = model
        os.environ["AGENT_PROVIDER"] = "groq"
        demos = GROQ_DEMOS
        print("Groq menu includes basic agent, tools, and MCP; support for other features varies by model.")
    elif provider_choice == "0":
        return
    else:
        print("Choose 0, 1, or 2.")
        return

    script = choose_from_demos(demos)
    if script:
        run_script(script)


def local_menu():
    if find_spec("openai") is None:
        explain_missing_packages(["openai"])
        return

    base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1").rstrip("/")
    try:
        response = requests.get(f"{base_url}/models", timeout=3)
        response.raise_for_status()
        models = response.json().get("data", [])
    except (requests.RequestException, ValueError):
        print(f"Cannot reach LM Studio at {base_url}.")
        print("Start LM Studio, load a model, and start its local server, then retry.")
        return

    if not models:
        print(f"LM Studio is reachable at {base_url}, but no model is loaded.")
        return

    print(f"Connected to LM Studio model: {models[0].get('id', 'unknown')}")
    script = choose_from_demos(LOCAL_DEMOS)
    if script:
        run_script(script)


def main():
    banner()
    while True:
        print("\n1) Check setup: packages, files, API-key status, and LM Studio connection.")
        print("2) Run offline tests: checks project code/config; no model calls or API charges.")
        print("3) Cloud agent examples: choose OpenAI or Groq; requires a key.")
        print("4) LM Studio examples: run a local model; requires a loaded model server.")
        print("0) Exit the lesson menu.")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            check_setup()
        elif choice == "2":
            passed = run_tests()
            if passed is not None:
                print("All tests passed." if passed else "Some tests failed; see output above.")
        elif choice == "3":
            cloud_menu()
        elif choice == "4":
            local_menu()
        elif choice == "0":
            print("Goodbye.")
            return
        else:
            print("Please choose 0, 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()