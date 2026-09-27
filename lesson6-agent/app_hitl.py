"""
Lektion 6 — Human-in-the-loop med interruptions och resume.
"""

import asyncio

from agents import Agent, Runner, function_tool
from provider_config import get_run_config


@function_tool(needs_approval=True)
def send_email(recipient: str, message: str) -> str:
    """Send an email."""
    return f"Email sent to {recipient}: {message}"


agent = Agent(
    name="EmailAssistant",
    instructions=(
        "You can send emails, but sending an email "
        "always requires human approval."
    ),
    tools=[send_email],
)


async def main():
    run_config = get_run_config()
    result = await Runner.run(
        agent,
        "Send an email to test@example.com saying Hello.",
        run_config=run_config,
    )

    while result.interruptions:
        print("\n APPROVAL REQUIRED")
        for interruption in result.interruptions:
            print(f"Tool: {interruption.tool_name}")
            print(f"Arguments: {interruption.arguments}")

            answer = input("\nApprove? (y/n): ").strip().lower()

            if answer == "y":
                result.state.approve(interruption)
            else:
                result.state.reject(interruption)

        result = await Runner.run(agent, result.state, run_config=run_config)

    print("\nResult:")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
