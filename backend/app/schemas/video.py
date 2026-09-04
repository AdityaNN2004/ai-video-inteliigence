from pydantic import BaseModel


class VideoMetadata(BaseModel):
    duration: float
    width: int
    height: int
    fps: float
    video_codec: str
    video_bitrate: int | None
    has_audio: bool
    audio_codec: str | None
    audio_sample_rate: int | None
    audio_channels: int | None


class VideoResponse(BaseModel):
    video_id: str
    filename: str
    status: str
    metadata: VideoMetadata


class VideoDetailResponse(BaseModel):
    video_id: str
    filename: str
    status: str
    language: str | None
    transcript: str | None
    processed_at: str | None
    metadata: VideoMetadata