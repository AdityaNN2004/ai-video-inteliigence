from pathlib import Path
import sys
import subprocess
import json

def parse_fps(fps_str: str) -> float:
    """Safely converts fraction strings like '30/1' or '24000/1001' to float."""
    try:
        if not fps_str:
            return 0.0
        if "/" in fps_str:
            num, denom = fps_str.split("/")
            if float(denom) > 0:
                return round(float(num) / float(denom), 2)
        return float(fps_str)
    except (ValueError, ZeroDivisionError, AttributeError):
        return 0.0

def get_video_metadata(file_path:Path)-> dict | None:
    cmd = [
        "ffprobe", 
        "-v", "error", 
        "-print_format", "json", 
        "-show_format", 
        "-show_streams", 
        str(file_path)
    ]
    
        
    # hasAudio=-1
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        probe = json.loads(result.stdout)
        video_stream = next((s for s in probe["streams"] if s["codec_type"] == "video"),None)
        audio_stream = next((s for s in probe["streams"] if s["codec_type"] == "audio"),None)
        if not video_stream:
            raise ValueError("No video stream found in file")
        metadata = {
            "duration": float(probe.get("format", {}).get("duration", 0)),
            "width": int(video_stream.get("width", 0)),
            "height": int(video_stream.get("height", 0)),
            "fps": parse_fps(video_stream.get("avg_frame_rate", "0/0")),
            "video_codec": video_stream.get("codec_name", "unknown"),
            "video_bitrate": int(video_stream.get("bit_rate", 0)) if video_stream.get("bit_rate") else None,
            "has_audio": audio_stream is not None,
            "audio_codec": audio_stream.get("codec_name", None) if audio_stream else None,
            "audio_sample_rate": int(audio_stream.get("sample_rate", 0)) if audio_stream else None,
            "audio_channels": int(audio_stream.get("channels", 0)) if audio_stream else None
        }
        return metadata
    except subprocess.CalledProcessError as e:
        print(f"FFprobe execution failed: {e.stderr}", file=sys.stderr)
        return None
    except FileNotFoundError:
        print("Error: ffprobe.exe could not be found in your Windows PATH system variables.", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print("Error: Failed to parse ffprobe output as valid JSON.", file=sys.stderr)
        return None
    