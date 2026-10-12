
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

    structured_llm = llm.with_structured_output(
        ImplementationPlan,
        method="json_schema",
    )

    
    repository_files = issue.get("repository_files", {})

    file_context = "\n\n".join(
        f"File: {path}\n{content[:5000]}"
        for path, content in list(repository_files.items())[:10]
    )

    prompt = f"""
You are a senior software engineer planning a code fix.

GitHub issue title: {issue.get("title", "")}
GitHub issue description: {issue.get("body", "")}

Repository source code:
{file_context or "No repository source files were provided."}

Create a practical implementation plan based on the available code.
Do not invent files or functions.
Include 3 to 5 actionable steps and relevant tests.
Do not write or modify code.
"""


    result = structured_llm.invoke(prompt)
    return result.model_dump()
