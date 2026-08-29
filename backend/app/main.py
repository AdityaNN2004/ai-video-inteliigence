from fastapi import FastAPI
from app.api.videos import router as video_router
app = FastAPI()

@app.get("/")
def read_root():
    return {"message":"Hello from FastAPI Server"}

app.include_router(video_router)