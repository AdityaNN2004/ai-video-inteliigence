from pathlib import Path

from app.services.transcription import transcribe_audio


audio_path = Path("processed/fing_dark_web.wav")

result = transcribe_audio(audio_path)

print("\n========== TRANSCRIPTION ==========")
print("Language:", result["language"])
print("Text:", result["text"])

print("\n========== SEGMENTS ==========")

for segment in result["segments"]:
    print(
        f"[{segment['start']:.2f}s - {segment['end']:.2f}s] "
        f"{segment['text'].strip()}"
    )