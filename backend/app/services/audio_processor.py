import subprocess
from pathlib import Path


def extract_audio(video_path: Path, output_path: Path) -> bool:
    """
    Extract audio from a video file and save it as WAV.
    """

    command = [
        "ffmpeg",
        "-i", str(video_path),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        "-y",
        str(output_path)
    ]

    try:
        subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )

        return True

    except subprocess.CalledProcessError as e:
        print(f"Audio extraction failed: {e.stderr}")
        return False

    except FileNotFoundError:
        print("FFmpeg was not found in PATH.")
        return False