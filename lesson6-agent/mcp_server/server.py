"""
Lektion 6 — Minimal MCP-server.
FastMCP anvands endast som ett enkelt Python-verktyg.
MCP-konceptet ar standarden; FastMCP ar implementationen.
"""

from fastmcp import FastMCP


mcp = FastMCP("Course MCP Server")


@mcp.tool
def get_course_info(topic: str) -> str:
    """Return information about the AI Developer course."""
    course = {
        "python": "Python anvands for programmering, AI och automation.",
        "agents": "AI-agenter kan anvanda verktyg for att utfora uppgifter.",
        "rag": "RAG kombinerar informationssokning med en sprakmodell.",
    }
    return course.get(topic.lower(), "Ingen information hittades.")


@mcp.tool
def calculate_sum(a: float, b: float) -> float:
    """Calculate the sum of two numbers."""
    return a + b


if __name__ == "__main__":
    mcp.run()
