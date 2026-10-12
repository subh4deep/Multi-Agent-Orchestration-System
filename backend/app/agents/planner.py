
from langchain_groq import ChatGroq
from backend.app.config import settings


def create_plan(issue: dict) -> list[str]:
    if not settings.groq_api_key:
        raise ValueError("GROQ_API_KEY is missing from .env")

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.2,
        groq_api_key=settings.groq_api_key,
    )

    prompt = f"""
You are a software engineering planner.

Analyze this GitHub issue and create a practical implementation plan.

Issue title: {issue.get("title", "")}
Issue description: {issue.get("body", "")}

Return 3 to 5 numbered steps.
Each step must be a clear, actionable task.
Include testing as one of the steps.
Do not write code or modify files.
"""

    response = llm.invoke(prompt)

    steps = []
    for line in response.content.splitlines():
        line = line.strip()
        if line:
            cleaned = line.lstrip("0123456789.-) ").strip()
            if cleaned:
                steps.append(cleaned)

    if not steps:
        raise ValueError("Planner returned an empty plan")

    return steps
