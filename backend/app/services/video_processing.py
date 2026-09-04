from datetime import datetime
from pathlib import Path

from app.database import SessionLocal
from app.models.video import Video
from app.services.audio_processor import extract_audio
from app.services.transcription import transcribe_audio
from app.models.transcript_segment import TranscriptSegment
from app.services.embedding import generate_embedding

def process_video(video_id,video_path: Path) -> None:
    """
    Process a video in the background.

    A new database session is created specifically
    for the background task.
    """

    db = SessionLocal()

    try:
        # Get a fresh Video object
        video = db.get(Video, video_id)

        if video is None:
            print(f"Video {video_id} not found.")
            return

        # 1. Mark as processing
        video.status = "processing"
        db.commit()

        # 2. Create processed directory
        processed_dir = video_path.parent.parent / "processed"
        processed_dir.mkdir(parents=True, exist_ok=True)

        # 3. Extract audio
        audio_path = processed_dir / f"{video_path.stem}.wav"

        audio_success = extract_audio(
            video_path,
            audio_path
        )

        if not audio_success:
            raise RuntimeError("Audio extraction failed")

        # 4. Transcribe
        result = transcribe_audio(audio_path)
        
        # 5. Save transcript
        video.transcript = result["text"]
        video.language = result["language"]
        for segment in result["segments"]:
            text = segment["text"].strip()

            if not text:
                continue

            embedding = generate_embedding(text)

            transcript_segment = TranscriptSegment(
                video_id=video.id,
                start_time=segment["start"],
                end_time=segment["end"],
                text=text,
                embedding=embedding
            )

            db.add(transcript_segment)
        
        video.processed_at = datetime.now()

        # 6. Mark completed
        video.status = "completed"

        db.commit()

        print(f"Video {video_id} processed successfully.")

    except Exception as e:
        db.rollback()

        # Try to mark the video as failed
        video = db.get(Video, video_id)

        if video is not None:
            video.status = "failed"
            db.commit()

        print(f"Video processing failed: {e}")

    finally:
        db.close()