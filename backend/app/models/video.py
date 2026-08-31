from sqlalchemy import Column,String,Float,Integer,Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base

class Video(Base):
    __tablename__ = "videos"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    filename= Column(String,nullable=False)
    duration=Column(Float,nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    fps = Column(Float, nullable=False)

    video_codec = Column(String, nullable=False)
    video_bitrate = Column(Integer, nullable=True)

    has_audio = Column(Boolean, nullable=False)

    audio_codec = Column(String, nullable=True)
    audio_sample_rate = Column(Integer, nullable=True)
    audio_channels = Column(Integer, nullable=True)

    status = Column(String, nullable=False, default="uploaded")