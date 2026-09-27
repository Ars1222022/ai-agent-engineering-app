from agents import Agent, Runner
from provider_config import get_run_config


agent = Agent(
    name="CourseAssistant",
    instructions=(
        "You are a helpful assistant for AI Developer students. "
        "Answer clearly and briefly."
    ),
)


result = Runner.run_sync(
    agent,
    "Explain what an AI agent is in three sentences.",
    run_config=get_run_config(),
)

print(result.final_output)
