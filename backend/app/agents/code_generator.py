import json
from langchain_groq import ChatGroq

from backend.app.config import settings


def generate_patch(issue: dict, plan: dict) -> str:
    if not settings.groq_api_key:
        raise ValueError("GROQ_API_KEY is missing from .env")

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.1,
        groq_api_key=settings.groq_api_key,
    )

    repository_files = issue.get("repository_files", {})

    file_context = "\n\n".join(
        f"File: {path}\n{content[:8000]}"
        for path, content in list(repository_files.items())[:10]
    )
    previous_feedback = json.dumps(
        issue.get("previous_attempt_feedback", {}),
        indent=2,
    )
    prompt = f"""
You are a careful software engineer fixing a GitHub issue.
Previous attempt feedback:
{previous_feedback}

If previous feedback is available, fix the reported validation errors,
patch application errors, or test failures. Do not repeat the same failed
approach. Return a complete corrected unified diff patch.

ISSUE TITLE:
{issue.get("title", "")}

ISSUE DESCRIPTION:
{issue.get("body", "")}

IMPLEMENTATION PLAN:
{plan}

REPOSITORY FILES:
{file_context}

Generate a unified diff patch that addresses the issue.

Rules:
- Modify only files provided in the repository context.
- Follow the implementation plan where appropriate.
- Use valid unified diff format.
- Include the correct file paths in diff headers.
- Do not invent existing code or unrelated requirements.
- Do not wrap the patch in Markdown code fences.
- If the issue cannot be safely fixed with the available context,
  explain the limitation instead of inventing a patch.
- Do not execute commands or modify the repository directly.
"""

    response = llm.invoke(prompt)

    return response.content
