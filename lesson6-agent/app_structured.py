from pydantic import BaseModel
from agents import Agent, Runner
from provider_config import get_run_config


class CourseAnswer(BaseModel):
    topic: str
    answer: str
    confidence: float


agent = Agent(
    name="StructuredCourseAssistant",
    instructions=(
        "Answer questions about AI development. "
        "Return the answer using the required structured format."
    ),
    output_type=CourseAnswer,
)


result = Runner.run_sync(
    agent,
    "What is function calling?",
    run_config=get_run_config(),
)

answer = result.final_output

print("Topic:", answer.topic)
print("Answer:", answer.answer)
print("Confidence:", answer.confidence)
print("Type:", type(answer))
