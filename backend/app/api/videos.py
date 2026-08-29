# from typing import Annotated
from fastapi import APIRouter, UploadFile ,File, HTTPException,status
import shutil
import uuid
from pathlib import Path
from app.services.video_processor import get_video_metadata
from app.schemas.video import VideoResponse

router = APIRouter()

CURR_DIR = Path(__file__).resolve().parent
# print(f"CD:{CURR_DIR}")

UPLOAD_DIR = CURR_DIR.parent.parent / "uploads"

ALLOWED_EXTENSIONS = {".mp4"}

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
# print(f"upload dir:{UPLOAD_DIR}")

@router.post("/api/videos/upload")
async def upload_video_file(file:UploadFile = File(...))->VideoResponse:
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
        
        return VideoResponse(
                video_id= str(video_id),
                filename=file.filename,
                status="uploaded",
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