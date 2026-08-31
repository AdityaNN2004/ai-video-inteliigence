from app.database import engine,Base
from app.models.video import Video

Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully!")