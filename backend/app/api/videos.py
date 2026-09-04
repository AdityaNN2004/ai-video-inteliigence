# from typing import Annotated
from fastapi import (APIRouter,UploadFile,File,HTTPException,status,Depends,Query,BackgroundTasks)
from datetime import datetime
import shutil
import uuid
from pathlib import Path
from app.services.video_processor import get_video_metadata
from app.schemas.video import VideoResponse
from app.schemas.video import VideoDetailResponse
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends

from app.models.transcript_segment import TranscriptSegment
from app.services.video_processing import process_video
from app.database import get_db
from app.models.video import Video

router = APIRouter()

CURR_DIR = Path(__file__).resolve().parent
# print(f"CD:{CURR_DIR}")

UPLOAD_DIR = CURR_DIR.parent.parent / "uploads"

ALLOWED_EXTENSIONS = {".mp4",".mkv"}

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
# print(f"upload dir:{UPLOAD_DIR}")

@router.post("/api/videos/upload")
async def upload_video_file(background_tasks: BackgroundTasks,file: UploadFile = File(...),db: Session = Depends(get_db)) -> VideoResponse:
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file extensions '{file_extension}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    video_id = uuid.uuid4()
    unique_file = f"{video_id}{file_extension}"
    file_path = UPLOAD_DIR / unique_file
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file,buffer)
        metadata =  get_video_metadata(file_path)
        if metadata is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"Metadata extraction failed while processing {file.filename}"
            )
        video = Video(
                        id=video_id,
                        filename=file.filename,

                        duration=metadata["duration"],
                        width=metadata["width"],
                        height=metadata["height"],
                        fps=metadata["fps"],

                        video_codec=metadata["video_codec"],
                        video_bitrate=metadata["video_bitrate"],

                        has_audio=metadata["has_audio"],

                        audio_codec=metadata["audio_codec"],
                        audio_sample_rate=metadata["audio_sample_rate"],
                        audio_channels=metadata["audio_channels"],

                        status="uploaded"
                    )

        db.add(video)
        db.commit()
        db.refresh(video)
        background_tasks.add_task(
            process_video,
            video.id,
            file_path,
        )
        return VideoResponse(
            video_id=str(video.id),
            filename=video.filename,
            status=video.status,
            metadata=metadata
        )
    except HTTPException :
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file {str(e)}"
        )
    finally:
        await file.close()
@router.get("/api/videos/{video_id}/transcript")
async def get_video_transcript(
    video_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    video = db.get(Video, video_id)

    if video is None or video.is_deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Video with id {video_id} not found"
        )

    segments = (
        db.query(TranscriptSegment)
        .filter(TranscriptSegment.video_id == video_id)
        .order_by(TranscriptSegment.start_time)
        .all()
    )

    return {
        "video_id": str(video.id),
        "filename": video.filename,
        "language": video.language,
        "status": video.status,
        "segments": [
            {
                "start_time": segment.start_time,
                "end_time": segment.end_time,
                "text": segment.text
            }
            for segment in segments
        ]
    }
@router.get("/api/videos/{video_id}")
async def get_video_by_id(
    video_id: uuid.UUID,
    db: Session = Depends(get_db)
) -> VideoResponse:

    video = db.get(Video, video_id)

    if video is None:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Video with id {video_id} not found"
        )

    return VideoResponse(
        video_id=str(video.id),
        filename=video.filename,
        status=video.status,
        metadata={
            "duration": video.duration,
            "width": video.width,
            "height": video.height,
            "fps": video.fps,
            "video_codec": video.video_codec,
            "video_bitrate": video.video_bitrate,
            "has_audio": video.has_audio,
            "audio_codec": video.audio_codec,
            "audio_sample_rate": video.audio_sample_rate,
            "audio_channels": video.audio_channels
        }
    )
@router.get("/api/videos")
async def get_videos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    videos = (
        db.query(Video)
        .filter(Video.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [
        VideoResponse(
            video_id=str(video.id),
            filename=video.filename,
            status=video.status,
            metadata={
                "duration": video.duration,
                "width": video.width,
                "height": video.height,
                "fps": video.fps,
                "video_codec": video.video_codec,
                "video_bitrate": video.video_bitrate,
                "has_audio": video.has_audio,
                "audio_codec": video.audio_codec,
                "audio_sample_rate": video.audio_sample_rate,
                "audio_channels": video.audio_channels,
            }
        )
        for video in videos
    ]

@router.delete("/api/videos/{video_id}")
async def delete_video(video_id:uuid.UUID,db:Session = Depends(get_db))->VideoResponse:
    video = db.get(Video,video_id)
    if video is None:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Video with id {video_id} not found"
            )
    video.status = "deleted"
    video.is_deleted = True
    video.deleted_at = datetime.now()
    db.commit()
    return VideoResponse(
        video_id=str(video_id),
        filename=video.filename,
        status="deleted",
        metadata={
            "duration": video.duration,
            "width": video.width,
            "height": video.height,
            "fps": video.fps,
            "video_codec": video.video_codec,
            "video_bitrate": video.video_bitrate,
            "has_audio": video.has_audio,
            "audio_codec": video.audio_codec,
            "audio_sample_rate": video.audio_sample_rate,
            "audio_channels": video.audio_channels
        }
    )

@router.get("/api/videos/{video_id}/details")
async def get_video_details(
    video_id: uuid.UUID,
    db: Session = Depends(get_db)
) -> VideoDetailResponse:

    video = db.get(Video, video_id)

    if video is None or video.is_deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Video with id {video_id} not found"
        )

    return VideoDetailResponse(
        video_id=str(video.id),
        filename=video.filename,
        status=video.status,
        language=video.language,
        transcript=video.transcript,
        processed_at=(
            video.processed_at.isoformat()
            if video.processed_at
            else None
        ),
        metadata={
            "duration": video.duration,
            "width": video.width,
            "height": video.height,
            "fps": video.fps,
            "video_codec": video.video_codec,
            "video_bitrate": video.video_bitrate,
            "has_audio": video.has_audio,
            "audio_codec": video.audio_codec,
            "audio_sample_rate": video.audio_sample_rate,
            "audio_channels": video.audio_channels,
        }
    )
