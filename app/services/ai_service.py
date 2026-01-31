import json
import re
from app.core.gemini_client import model
from app.schemas.ai import AIAnalysis


SYSTEM_PROMPT = """
You are a task analysis assistant.

Return ONLY valid JSON.
No explanations.
No markdown.

Schema:
{
  "title": string,
  "priority": "High" | "Medium" | "Low",
  "category": "Work" | "Personal" | "Learning" | "Health" | "Other",
  "estimated_minutes": number,
  "subtasks": string[]
}
"""


def _extract_json(text: str) -> str:
    """
    Gemini may wrap JSON in ```json ... ```
    This safely extracts the JSON block.
    """
    text = text.strip()

    # Case 1: wrapped in ```json
    if text.startswith("```"):
        text = re.sub(r"^```json\s*|^```\s*|\s*```$", "", text, flags=re.IGNORECASE).strip()

    return text


def analyze_task(text: str) -> AIAnalysis:
    response = model.generate_content(
        [
            SYSTEM_PROMPT,
            f"Task: {text}",
        ]
    )

    raw = response.text or ""
    cleaned = _extract_json(raw)

    try:
        data = json.loads(cleaned)
        return AIAnalysis(**data)
    except Exception as e:
        raise ValueError(
            f"Gemini response parsing failed.\nRAW:\n{raw}\n\nCLEANED:\n{cleaned}"
        ) from e
