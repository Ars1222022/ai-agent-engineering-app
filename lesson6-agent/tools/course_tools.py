def get_course_info(topic: str) -> str:
    """Return information about the AI Developer course."""
    course = {
        "python": "Python anvands for programmering, AI och automation.",
        "agents": "AI-agenter kan anvanda verktyg for att utfora uppgifter.",
        "rag": "RAG kombinerar informationssokning med en sprakmodell.",
    }
    return course.get(topic.lower(), "Ingen information hittades.")


def calculate_sum(a: float, b: float) -> float:
    """Calculate the sum of two numbers."""
    return a + b
