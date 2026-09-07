from sqlalchemy import Column,String,Float,Integer,Boolean,Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import DateTime
from datetime import datetime
from app.database import Base
from sqlalchemy.dialects.postgresql import JSONB
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
    
    transcript = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    summary_data = Column(JSONB, nullable=True)
    chapters = Column(JSONB, nullable=True)
    language = Column(String, nullable=True)
    processed_at = Column(DateTime, nullable=True) 

    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime, nullable=True)