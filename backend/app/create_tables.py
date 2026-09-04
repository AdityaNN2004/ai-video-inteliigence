from app.database import engine,Base
from app.models.video import Video
from app.models.video import Video
from app.models.transcript_segment import TranscriptSegment
Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully!")