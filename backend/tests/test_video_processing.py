from pathlib import Path

from app.services.video_processing import process_video


video_path = Path(
    "uploads/8fbfa5ab-58a5-4f42-9efc-3f3d67bce1b4.mp4"
)

result = process_video(video_path)

print("\n========== VIDEO PROCESSING ==========")

print("Video:", result["video_path"])
print("Audio:", result["audio_path"])

print("\n========== TRANSCRIPT ==========")

print("Language:", result["transcript"]["language"])
print("Text:", result["transcript"]["text"])

print("\n========== SEGMENTS ==========")

for segment in result["transcript"]["segments"]:
    print(
        f"[{segment['start']:.2f}s - "
        f"{segment['end']:.2f}s] "
        f"{segment['text'].strip()}"
    )