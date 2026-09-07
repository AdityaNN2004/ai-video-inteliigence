from openai import OpenAI
from sqlalchemy.orm import Session

from app.config import OPENROUTER_API_KEY, LLM_MODEL
from app.models.transcript_segment import TranscriptSegment
from app.services.search import semantic_search


def answer_video_question(
    video_id,
    question: str,
    db: Session,
    limit: int = 5
) -> dict:

    if not OPENROUTER_API_KEY:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not configured"
        )

    # ---------------------------------------------------------
    # 1. Semantic retrieval
    # ---------------------------------------------------------

    candidates = semantic_search(
        query=question,
        db=db,
        limit=max(limit * 5, 15)
    )

    candidates = [
        result
        for result in candidates
        if str(result[1].id) == str(video_id)
    ]

    if not candidates:
        return {
            "answer": (
                "I could not find relevant information "
                "in this video."
            ),
            "sources": []
        }

    # ---------------------------------------------------------
    # 2. Similarity filtering
    # ---------------------------------------------------------

    MIN_SIMILARITY = 0.45

    candidates = [
        result
        for result in candidates
        if float(result[2]) >= MIN_SIMILARITY
    ]

    if not candidates:
        return {
            "answer": (
                "The information needed to answer this question "
                "is not available in the video."
            ),
            "sources": []
        }

    # ---------------------------------------------------------
    # 3. Select diverse matching sources
    # ---------------------------------------------------------

    candidates.sort(
        key=lambda result: float(result[2]),
        reverse=True
    )

    selected = []

    MIN_TIME_DISTANCE = 10.0

    for candidate in candidates:

        segment, video, score = candidate

        too_close = False

        for existing in selected:

            existing_segment = existing[0]

            if abs(
                segment.start_time -
                existing_segment.start_time
            ) < MIN_TIME_DISTANCE:
                too_close = True
                break

        if too_close:
            continue

        selected.append(candidate)

        if len(selected) >= limit:
            break

    results = selected

    if not results:
        return {
            "answer": (
                "The information needed to answer this question "
                "is not available in the video."
            ),
            "sources": []
        }

    # ---------------------------------------------------------
    # 4. Expand context around matching segments
    # ---------------------------------------------------------

    CONTEXT_WINDOW = 20.0

    context_segments = {}

    for segment, video, score in results:

        nearby_segments = (
            db.query(TranscriptSegment)
            .filter(
                TranscriptSegment.video_id == video_id,
                TranscriptSegment.start_time >=
                    max(0, segment.start_time - CONTEXT_WINDOW),
                TranscriptSegment.start_time <=
                    segment.start_time + CONTEXT_WINDOW
            )
            .order_by(TranscriptSegment.start_time)
            .all()
        )

        for nearby in nearby_segments:
            context_segments[nearby.id] = nearby

    context_segments = sorted(
        context_segments.values(),
        key=lambda item: item.start_time
    )

    # ---------------------------------------------------------
    # 5. Build expanded transcript context
    # ---------------------------------------------------------

    context_parts = []

    for segment in context_segments:

        context_parts.append(
            f"[{segment.start_time:.2f}s - "
            f"{segment.end_time:.2f}s] "
            f"{segment.text}"
        )

    context = "\n".join(context_parts)

    # ---------------------------------------------------------
    # 6. Ask grounded LLM
    # ---------------------------------------------------------

    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )

    prompt = f"""
You are an AI assistant answering questions about a video.

Answer the user's question using ONLY the provided transcript.

STRICT RULES:

1. Use only information explicitly supported by the transcript.
2. Do not use outside knowledge.
3. Do not guess.
4. Do not infer unsupported facts.
5. If the transcript does not contain enough information,
   say that the information is not available in the video.
6. Keep the answer concise and useful.
7. Do not mention retrieval, embeddings, similarity, or chunks.
8. Do not fabricate timestamps.

The transcript below contains relevant passages together with
nearby transcript context. Use the surrounding context when
necessary to understand incomplete sentences.

TRANSCRIPT:

{context}

USER QUESTION:

{question}
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a grounded video Q&A assistant. "
                    "Answer only from the supplied transcript."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    answer = response.choices[0].message.content

    if not answer:
        raise RuntimeError(
            "LLM returned an empty answer"
        )

    # ---------------------------------------------------------
    # 7. Return only the actual semantic matches as sources
    # ---------------------------------------------------------

    sources = [
        {
            "start_time": segment.start_time,
            "end_time": segment.end_time,
            "text": segment.text,
            "similarity": float(score)
        }
        for segment, video, score in results
    ]

    return {
        "answer": answer.strip(),
        "sources": sources
    }