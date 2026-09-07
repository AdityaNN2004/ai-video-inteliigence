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

class VideoSummary(BaseModel):
    summary: str
    key_points: list[str]
    topics: list[str]
class VideoChapter(BaseModel):
    start_time: float
    end_time: float
    title: str
    summary: str
class VideoDetailResponse(BaseModel):

    video_id: str
    filename: str
    status: str
    language: str | None
    transcript: str | None
    summary: str | None
    summary_data: VideoSummary | None
    chapters: list[VideoChapter] | None
    processed_at: str | None
    metadata: VideoMetadata

class VideoQuestionRequest(BaseModel):
    question: str


class VideoQuestionSource(BaseModel):
    start_time: float
    end_time: float
    text: str
    similarity: float


class VideoQuestionResponse(BaseModel):
    video_id: str
    question: str
    answer: str
    sources: list[VideoQuestionSource]