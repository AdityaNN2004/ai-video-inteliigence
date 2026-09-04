from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.videos import router as video_router
# from backend.app.database import router as video_db
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"message":"Hello from FastAPI Server"}
    
app.include_router(video_router)
# app.include_router(video_db)