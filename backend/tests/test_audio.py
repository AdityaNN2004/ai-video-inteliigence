from pathlib import Path
from app.services.audio_processor import extract_audio


video_path = Path("uploads/a68ad6da-ed8c-4659-8939-63d585c571ef.mp4")
audio_path = Path("processed/fing_dark_web.wav")

audio_path.parent.mkdir(parents=True, exist_ok=True)

success = extract_audio(video_path, audio_path)

if success:
    print(f"Audio extracted successfully: {audio_path}")
else:
    print("Audio extraction failed.")