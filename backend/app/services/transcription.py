import whisper
from pathlib import Path

model = whisper.load_model("base")
def transcribe_audio(audio_path:Path)->dict:
    """Transcribe an audio fle using whisper"""
    try:
        result=model.transcribe(
            str(audio_path),
            fp16=False
        )
        return {
            "text":result["text"].strip(),
            "language":result.get("language"),
            "segments":result.get("segments",[])
        }
    except Exception as e:
        print(f"Transcription failed: {e}")
        return{
            "text":"",
            "language":None,
            "segments":[]
        }