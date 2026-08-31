# from typing import Annotated
from fastapi import APIRouter, UploadFile ,File, HTTPException,status
import shutil
import uuid
from pathlib import Path
from app.services.video_processor import get_video_metadata
from app.schemas.video import VideoResponse

from sqlalchemy.orm import Session
from fastapi import Depends

from app.database import get_db
from app.models.video import Video

router = APIRouter()

CURR_DIR = Path(__file__).resolve().parent
# print(f"CD:{CURR_DIR}")

UPLOAD_DIR = CURR_DIR.parent.parent / "uploads"

ALLOWED_EXTENSIONS = {".mp4"}

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
# print(f"upload dir:{UPLOAD_DIR}")

@router.post("/api/videos/upload")
async def upload_video_file(file: UploadFile = File(...),db: Session = Depends(get_db)) -> VideoResponse:
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
        
# @router.get("/api/videos/{video_id}")
# async def get_video_by_id(video_id:uuid.uuid4):
    