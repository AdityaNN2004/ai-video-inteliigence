from sqlalchemy.orm import Session

from app.models.transcript_segment import TranscriptSegment
from app.models.video import Video
from app.services.embedding import generate_embedding


def semantic_search(
    query: str,
    db: Session,
    limit: int = 10,
    similarity_threshold: float = 0.35
):
    query_embedding = generate_embedding(query)

    distance = TranscriptSegment.embedding.cosine_distance(
        query_embedding
    )

    similarity = (1 - distance).label("similarity")

    # Fetch extra candidates so we can remove nearby duplicates
    candidates = (
        db.query(
            TranscriptSegment,
            Video,
            similarity
        )
        .join(
            Video,
            TranscriptSegment.video_id == Video.id
        )
        .filter(
            Video.is_deleted == False,
            TranscriptSegment.embedding.is_not(None),
            distance <= (1 - similarity_threshold)
        )
        .order_by(distance)
        .limit(limit * 5)
        .all()
    )

    selected = []

    for segment, video, score in candidates:

        is_duplicate = False

        for existing_segment, existing_video, existing_score in selected:

            # Only compare segments from the same video
            if existing_video.id != video.id:
                continue

            # Consider nearby timestamps duplicates
            if abs(
                existing_segment.start_time -
                segment.start_time
            ) < 5:

                is_duplicate = True
                break

        if not is_duplicate:
            selected.append(
                (segment, video, score)
            )

        if len(selected) >= limit:
            break

    return selected