from sqlalchemy.orm import Session

from app.models.transcript_segment import TranscriptSegment
from app.models.video import Video
from app.services.embedding import generate_embedding


SIMILARITY_THRESHOLD = 0.35


def semantic_search(
    query: str,
    db: Session,
    limit: int = 10
):
    query_embedding = generate_embedding(query)

    distance = TranscriptSegment.embedding.cosine_distance(
        query_embedding
    )

    similarity = (1 - distance).label("similarity")

    results = (
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
            distance <= (1 - SIMILARITY_THRESHOLD)
        )
        .order_by(distance)
        .limit(limit)
        .all()
    )

    return results