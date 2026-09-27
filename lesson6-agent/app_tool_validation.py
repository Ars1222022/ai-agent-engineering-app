"""
Lektion 6 — Tool-level safety validation.
Ofarlig simulering — ingen fil raderas.
"""

from agents import Agent, Runner, function_tool
from provider_config import get_run_config


@function_tool
def delete_file(filename: str) -> str:
    """Delete a file. Only allows deletion of files in demo/."""

    if not filename.startswith("demo/"):
        return f"BLOCKED: Cannot delete {filename}. Only demo/ is allowed."

    return f"SIMULATION: Would delete {filename}"


agent = Agent(
    name="FileAssistant",
    instructions=(
        "You can delete files. Use delete_file when asked."
    ),
    tools=[delete_file],
)


run_config = get_run_config()
result = Runner.run_sync(agent, "Delete demo/test.txt", run_config=run_config)
print(result.final_output)

result = Runner.run_sync(agent, "Delete system/passwd", run_config=run_config)
print(result.final_output)
