import json

from openai import OpenAI

from app.config import OPENROUTER_API_KEY, LLM_MODEL


def generate_video_summary(transcript: str) -> dict:

    if not transcript or not transcript.strip():
        return {
            "summary": "",
            "key_points": [],
            "topics": []
        }

    if not OPENROUTER_API_KEY:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not configured"
        )

    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )

    prompt = f"""
You are an AI video intelligence assistant.

Analyze the following video transcript.

Return ONLY valid JSON.
Do not use markdown.
Do not use code fences.

Use exactly this structure:

{{
  "summary": "A concise 2-4 sentence overview.",
  "key_points": [
    "Important point 1",
    "Important point 2",
    "Important point 3",
    "Important point 4",
    "Important point 5"
  ],
  "topics": [
    "Important topic 1",
    "Important topic 2",
    "Important topic 3"
  ]
}}

Rules:
- Do not invent information.
- Base everything only on the transcript.
- Keep the summary concise.
- Keep key_points useful and specific.
- Keep topics short.

VIDEO TRANSCRIPT:

{transcript}
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You analyze video transcripts and return "
                    "accurate structured JSON."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("LLM returned an empty response")

    content = content.strip()

    try:
        summary_data = json.loads(content)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"LLM returned invalid JSON: {e}"
        )

    required_fields = {
        "summary",
        "key_points",
        "topics"
    }

    if not required_fields.issubset(summary_data.keys()):
        raise RuntimeError(
            "LLM response is missing required summary fields"
        )

    return summary_data