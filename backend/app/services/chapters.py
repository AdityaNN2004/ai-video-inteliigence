import json

from openai import OpenAI

from app.config import OPENROUTER_API_KEY, LLM_MODEL


def generate_video_chapters(
    segments: list[dict],
    duration: float
) -> dict:

    if not segments:
        return {"chapters": []}

    if not OPENROUTER_API_KEY:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not configured"
        )

    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )

    # ---------------------------------------------------------
    # Build timestamped transcript
    # ---------------------------------------------------------

    transcript_parts = []

    for segment in segments:

        text = segment.get("text", "").strip()

        if not text:
            continue

        transcript_parts.append(
            f"[{segment['start']:.2f} - {segment['end']:.2f}] {text}"
        )

    transcript = "\n".join(transcript_parts)

    if not transcript:
        return {"chapters": []}

    # ---------------------------------------------------------
    # Prevent extremely large prompts
    # ---------------------------------------------------------

    MAX_TRANSCRIPT_CHARS = 50000

    if len(transcript) > MAX_TRANSCRIPT_CHARS:
        print(
            f"Chapter transcript is large "
            f"({len(transcript)} characters). "
            f"Truncating to {MAX_TRANSCRIPT_CHARS}."
        )

        transcript = transcript[:MAX_TRANSCRIPT_CHARS]

    # ---------------------------------------------------------
    # Prompt
    # ---------------------------------------------------------

    prompt = f"""
You are an AI video chaptering assistant.

Analyze the timestamped transcript below and divide the video
into meaningful chapters.

Return ONLY valid JSON.

Do not use markdown.
Do not use code fences.
Do not add explanations before or after the JSON.

Use exactly this structure:

{{
  "chapters": [
    {{
      "start_time": 0,
      "title": "Chapter title",
      "summary": "Short description of this chapter."
    }}
  ]
}}

Rules:

- Create 4 to 10 meaningful chapters.
- Chapters should represent major changes in topic or discussion.
- Do not create a chapter for every transcript segment.
- start_time MUST correspond to a timestamp present in the transcript.
- start_time must be in seconds.
- The first chapter should normally start at or near 0.
- Keep titles concise.
- Keep summaries to 1-2 sentences.
- Keep chapters in chronological order.
- Do not invent information.
- Base everything only on the transcript.
- The complete video duration is {duration:.2f} seconds.

TIMESTAMPED TRANSCRIPT:

{transcript}
"""

    # ---------------------------------------------------------
    # LLM request
    # ---------------------------------------------------------

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You create accurate video chapters from "
                    "timestamped transcripts. "
                    "Always return valid JSON."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    # ---------------------------------------------------------
    # Extract response
    # ---------------------------------------------------------

    content = response.choices[0].message.content

    if not content:
        print("\n========== EMPTY CHAPTER RESPONSE ==========")
        print(response)
        print("============================================\n")

        raise RuntimeError(
            "LLM returned an empty chapter response"
        )

    content = content.strip()

    print("\n========== CHAPTER LLM RESPONSE ==========")
    print(content[:3000])
    print("===========================================\n")

    # ---------------------------------------------------------
    # Clean common markdown formatting
    # ---------------------------------------------------------

    if content.startswith("```"):

        lines = content.splitlines()

        # Remove first ``` or ```json
        if lines:
            lines = lines[1:]

        # Remove closing ```
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        content = "\n".join(lines).strip()

    # ---------------------------------------------------------
    # Parse JSON
    # ---------------------------------------------------------

    try:

        data = json.loads(content)

    except json.JSONDecodeError:

        # Sometimes the model adds text around the JSON.
        # Try extracting the JSON object.

        start = content.find("{")
        end = content.rfind("}")

        if start == -1 or end == -1 or start >= end:

            print(
                "\n========== INVALID CHAPTER RESPONSE =========="
            )
            print(content)
            print("===============================================\n")

            raise RuntimeError(
                "LLM returned invalid chapter JSON"
            )

        json_content = content[start:end + 1]

        try:

            data = json.loads(json_content)

        except json.JSONDecodeError as e:

            print(
                "\n========== INVALID CHAPTER RESPONSE =========="
            )
            print(content)
            print("===============================================\n")

            raise RuntimeError(
                f"LLM returned invalid chapter JSON: {e}"
            )

    # ---------------------------------------------------------
    # Validate chapters
    # ---------------------------------------------------------

    chapters = data.get("chapters")

    if not isinstance(chapters, list):

        raise RuntimeError(
            "LLM response does not contain a valid chapters list"
        )

    validated_chapters = []

    for chapter in chapters:

        if not isinstance(chapter, dict):
            continue

        title = chapter.get("title")
        summary = chapter.get("summary")
        start_time = chapter.get("start_time")

        if not title or not summary:
            continue

        try:
            start_time = float(start_time)

        except (TypeError, ValueError):
            continue

        if start_time < 0 or start_time >= duration:
            continue

        validated_chapters.append({
            "start_time": start_time,
            "title": str(title).strip(),
            "summary": str(summary).strip()
        })

    # ---------------------------------------------------------
    # Sort chapters
    # ---------------------------------------------------------

    validated_chapters.sort(
        key=lambda chapter: chapter["start_time"]
    )

    # ---------------------------------------------------------
    # Remove chapters too close together
    # ---------------------------------------------------------

    filtered_chapters = []

    for chapter in validated_chapters:

        if not filtered_chapters:

            filtered_chapters.append(chapter)
            continue

        previous = filtered_chapters[-1]

        if (
            chapter["start_time"]
            - previous["start_time"]
            >= 30
        ):
            filtered_chapters.append(chapter)

    # ---------------------------------------------------------
    # Calculate end_time
    # ---------------------------------------------------------

    for index, chapter in enumerate(filtered_chapters):

        if index + 1 < len(filtered_chapters):

            chapter["end_time"] = (
                filtered_chapters[index + 1]["start_time"]
            )

        else:

            chapter["end_time"] = duration

    return {
        "chapters": filtered_chapters
    }