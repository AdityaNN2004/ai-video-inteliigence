import uuid
from pathlib import Path

from app.database import SessionLocal
from app.models.video import Video
from app.services.video_processing import process_video


db = SessionLocal()

try:
    # Get one existing video that hasn't been processed
    # video = (
    #     db.query(Video)
    #     .filter(
    #         Video.is_deleted == False,
    #         Video.status == "uploaded"
    #     )
    #     .first()
    # )
    
    video = db.get(Video,"a58ed5fa-48d3-4a9c-9aa4-06ac3f3b81cb")
    if video is None:
        print("No unprocessed video found.")
        exit()

    print("================================")
    print("VIDEO")
    print("================================")
    print("ID:", video.id)
    print("Filename:", video.filename)
    print("Status:", video.status)

    # Build actual video path
    video_path = (
        Path(__file__).resolve().parent.parent
        / "uploads"
        / f"{video.id}{Path(video.filename).suffix}"
    )

    print("Video path:", video_path)

    if not video_path.exists():
        print("Video file does not exist.")
        exit()

    # Process video
    process_video(
        video=video,
        video_path=video_path,
        db=db
    )

    # Refresh object from database
    db.refresh(video)

    print("\n================================")
    print("PROCESSING RESULT")
    print("================================")
    print("Status:", video.status)
    print("Language:", video.language)
    print("Processed at:", video.processed_at)

    print("\n================================")
    print("TRANSCRIPT")
    print("================================")
    print(video.transcript)

finally:
    db.close()