
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

from backend.app.config import settings


class ImplementationPlan(BaseModel):
    summary: str = Field(description="Short summary of the proposed fix")
    steps: list[str] = Field(
        description="Three to five actionable implementation steps"
    )
    testing: list[str] = Field(
        description="Tests needed to verify the fix"
    )


def create_plan(issue: dict) -> dict:
    if not settings.groq_api_key:
        raise ValueError("GROQ_API_KEY is missing from .env")

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.2,
        groq_api_key=settings.groq_api_key,
    )

    structured_llm = llm.with_structured_output(ImplementationPlan)

    prompt = f"""
You are a senior software engineer planning a code fix.

Analyze this GitHub issue and propose a practical implementation plan.

Issue title: {issue.get("title", "")}
Issue description: {issue.get("body", "")}

Requirements:
- Provide a concise summary.
- Include 3 to 5 actionable implementation steps.
- Include relevant tests.
- Do not invent repository details.
- Do not write or modify code.
"""

    result = structured_llm.invoke(prompt)
    return result.model_dump()
