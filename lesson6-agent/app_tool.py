from agents import Agent, Runner
from tools.course_tools import get_course_info, calculate_sum
from provider_config import get_run_config


agent = Agent(
    name="CourseAssistant",
    instructions=(
        "Answer questions about the AI Developer course. "
        "Use course information tool when appropriate. "
        "Use the calculator for math."
    ),
    tools=[get_course_info, calculate_sum],
)


questions = [
    "What does this course say about RAG?",
    "Calculate 27.5 + 14.2",
    "What does this course say about databases?",
]

run_config = get_run_config()
for question in questions:
    result = Runner.run_sync(agent, question, run_config=run_config)
    print(f"\nQ: {question}")
    print(f"A: {result.final_output}")
