#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"
VENV_PYTHON="$VENV_DIR/bin/python"
REQUIREMENTS="$PROJECT_DIR/requirements.txt"

if command -v python3 >/dev/null 2>&1; then
    SYSTEM_PYTHON="python3"
elif command -v python >/dev/null 2>&1; then
    SYSTEM_PYTHON="python"
else
    echo "Python 3.11 or newer was not found. Install Python, then run this script again."
    exit 1
fi

cd "$PROJECT_DIR"

prepare_local_environment() {
    if [[ ! -x "$VENV_PYTHON" ]]; then
        if ! "$SYSTEM_PYTHON" -c 'import sys; raise SystemExit(sys.version_info < (3, 11))'; then
            echo "Python 3.11 or newer is required for local mode. Install it, then run this script again."
            return 1
        fi
        echo "Creating the project's virtual environment..."
        "$SYSTEM_PYTHON" -m venv "$VENV_DIR" || return 1
    fi

    if ! "$VENV_PYTHON" -c 'import sys; raise SystemExit(sys.version_info < (3, 11))'; then
        echo "The existing venv uses an unsupported Python version. Rename or remove venv, then retry."
        return 1
    fi

    if ! "$VENV_PYTHON" -c 'import agents, openai, fastmcp, pytest, dotenv, requests' >/dev/null 2>&1; then
        echo "Installing project packages. This can take a few minutes on first run..."
        "$VENV_PYTHON" -m pip install -r "$REQUIREMENTS" || return 1
    fi

    if ! "$VENV_PYTHON" -c 'import agents, openai, fastmcp, pytest, dotenv, requests' >/dev/null 2>&1; then
        echo "The Python environment is still missing packages. Review the installation output above."
        return 1
    fi
}

docker_available() {
    if ! command -v docker >/dev/null 2>&1; then
        echo "Docker was not found. Install and start Docker Desktop (or Docker Engine), then try again."
        return 1
    fi
    if ! docker compose version >/dev/null 2>&1; then
        echo "Docker Compose is unavailable. Update or start Docker, then try again."
        return 1
    fi
}

while true; do
    echo
    echo "=== Lesson 6: AI Agent Engineering ==="
    echo "1) Start the local lesson menu"
    echo "2) Run automated tests"
    echo "3) Build the Docker image"
    echo "4) Start the lesson menu in Docker"
    echo "0) Exit"
    read -r -p "Choose an option: " choice || exit 0

    case "$choice" in
        1)
            if prepare_local_environment; then
                "$VENV_PYTHON" "$PROJECT_DIR/lab_launcher.py"
            else
                echo "Local setup failed. You can try the Docker option instead."
            fi
            ;;
        2)
            if prepare_local_environment; then
                "$VENV_PYTHON" -m pytest -q || echo "Some tests failed; read the output above."
            else
                echo "Local setup failed. You can try the Docker option instead."
            fi
            ;;
        3)
            if docker_available; then
                docker compose build lesson6 || echo "Docker image build failed. Read the output above."
            fi
            ;;
        4)
            if docker_available; then
                docker compose run --build --rm lesson6 || echo "Docker lesson exited with an error. Read the output above."
            fi
            ;;
        0)
            exit 0
            ;;
        *)
            echo "Choose 0, 1, 2, 3, or 4."
            ;;
    esac
done