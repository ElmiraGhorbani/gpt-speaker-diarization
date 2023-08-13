import os
import subprocess
import uuid


def get_project_root():
    """
    Get the root directory of the project.

    :return: Absolute path to the project root directory.
    """
    # Get the absolute path of the current file
    current_path = os.path.abspath(__file__)
    # Return the parent directory (project root)
    return os.path.dirname(os.path.dirname(current_path))


def get_file_size_in_mb(file_bytes):
    """
    Calculate the size of a file in megabytes.

    :param file_bytes: Bytes of the file's content.
    :return: File size in megabytes.
    """
    size_in_mb = os.path.getsize(file_bytes) / (1024 * 1024)
    return size_in_mb


def write_audio(audio_bytes, filename):
    """
    Write audio bytes to a temporary file, convert it to a specific format, and return the saved path.

    :param audio_bytes: Bytes containing audio data.
    :param filename: Original filename with extension.
    :return: Path to the saved audio file.
    """
    root_path = get_project_root()
    temp_wav_path = f"{root_path}/resources/audios/{filename}"
    save_path = f"{root_path}/resources/audios/{str(uuid.uuid4())}.mp3"
    with open(temp_wav_path, 'wb') as f:
        f.write(audio_bytes)
    subprocess.run(["ffmpeg", "-i", temp_wav_path, "-ar",
                    "16000", "-ac", "1", "-y", save_path])
    os.remove(temp_wav_path)
    return save_path
