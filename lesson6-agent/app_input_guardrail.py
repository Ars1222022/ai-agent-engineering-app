"""
Lektion 6 — Agents SDK input guardrail.
Demonstrerar hur en blockerande guardrail kopplas till en Agent.
"""

import asyncio

from pydantic import BaseModel

from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
)
from agents.decorators import input_guardrail
from provider_config import get_run_config


class GuardrailCheck(BaseModel):
    is_safe: bool
    reason: str


@input_guardrail(run_in_parallel=False)
async def safety_check(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input_text: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    """Blockera uppenbart skadliga forfragningar innan agenten startar."""

    if isinstance(input_text, str):
        text = input_text
    else:
        text = str(input_text)

    dangerous_keywords = [
        "delete all",
        "rm -rf",
        "drop database",
    ]

    is_safe = not any(
        keyword in text.lower()
        for keyword in dangerous_keywords
    )

    return GuardrailFunctionOutput(
        output_info=GuardrailCheck(
            is_safe=is_safe,
            reason="Blocked by safety guardrail" if not is_safe else "OK",
        ),
        tripwire_triggered=not is_safe,
    )


agent = Agent(
    name="GuardedAssistant",
    instructions="Answer questions clearly and briefly.",
    input_guardrails=[safety_check],
)


async def main():
    run_config = get_run_config()
    result = await Runner.run(agent, "What is Python?", run_config=run_config)
    print("Safe:", result.final_output)

    try:
        result = await Runner.run(agent, "delete all files", run_config=run_config)
        print("Unexpected:", result.final_output)

    except InputGuardrailTripwireTriggered:
        print("BLOCKED: Input guardrail triggered.")


if __name__ == "__main__":
    asyncio.run(main())
