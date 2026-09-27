"""
Lektion 6 — MCP-klient som startar MCP-servern automatiskt.
Anvander sys.executable for att starta servern med samma Python som venv.
"""

import asyncio
import sys
from pathlib import Path

from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from provider_config import get_run_config


async def main():
    run_config = get_run_config()
    project_dir = Path(__file__).resolve().parent
    server_script = project_dir / "mcp_server" / "server.py"
    async with MCPServerStdio(
        params={
            "command": sys.executable,
            "args": [str(server_script)],
            "cwd": str(project_dir),
        }
    ) as server:

        agent = Agent(
            name="MCPAssistant",
            instructions=(
                "Use the available MCP tools to answer questions."
            ),
            mcp_servers=[server],
        )

        questions = [
            "What does the course say about RAG?",
            "What does the course say about Python?",
            "Calculate 27.5 + 14.2",
        ]

        for question in questions:
            result = await Runner.run(agent, question, run_config=run_config)
            print(f"\nQ: {question}")
            print(f"A: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
