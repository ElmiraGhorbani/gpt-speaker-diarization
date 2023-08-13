import logging
import time
from typing import Optional

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .text_analysis import AI
from .speech_to_text import Whisper
from .utils import get_file_size_in_mb, write_audio
from .video_manager import VideoDownloader

# Create instances of various services and utilities
downloader = VideoDownloader()  # For downloading YouTube videos
whisper_api = Whisper()          # For speech-to-text conversion
openai_services = AI()           # For AI-powered services

# Define metadata for API tags
tags_metadata = [
    {
        "name": "diarization_api",
        "description": "Operations with the diarization API. Click on the `Try it out` button to test the API with **YouTube video** or **audio file**.",
    },
]

# Initialize the FastAPI app with metadata and description
app = FastAPI(
    title="GPT-Diarization Project",
    description="Conversational Speaker Diarization using AI Language Models",
    version="0.1.0",
    openapi_tags=tags_metadata,
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging settings for the application
logging.basicConfig(level=logging.INFO)


def process_audio(audio_data: bytes, filename: str):
    """
    Process audio data and perform speaker diarization.

    :param audio_data: Audio data in bytes.
    :param filename: Name of the audio file.
    :return: Diarization result containing transcript and dialogue.
    """
    audio_output_path = write_audio(audio_data, filename)
    file_size_mb = get_file_size_in_mb(audio_output_path)
    if file_size_mb > 25:
        wav_segments = whisper_api.audio_process(
            audio_output_path, is_byte=True)
        transcript = []
        for segments in wav_segments:
            transcript.append(whisper_api.transcribe(segments))
            time.sleep(0.006)
        transcript = ''.join(transcript)
    else:
        transcript = whisper_api.transcribe_raw(audio_output_path)
    dialogue = openai_services.extract_dialogue(transcript)
    result = {
        "transcript": transcript,
        "diarization_result": dialogue
    }
    return result


def process_youtube_video(video_id: str):
    """
    Process a YouTube video and perform speaker diarization.

    :param video_id: ID of the YouTube video.
    :return: Diarization result containing transcript and dialogue.
    """
    audio_output_path = downloader.download_video(video_id)
    file_size_mb = get_file_size_in_mb(audio_output_path)

    if file_size_mb > 25:
        wav_segments = whisper_api.audio_process(audio_output_path)
        transcript = []
        for segments in wav_segments:
            transcript.append(whisper_api.transcribe(segments))
            time.sleep(0.006)
        transcript = ''.join(transcript)
    else:
        transcript = whisper_api.transcribe_raw(audio_output_path)

    dialogue = openai_services.extract_dialogue(transcript)
    result = {
        "transcript": transcript,
        "diarization_result": dialogue
    }
    return result


@app.post("/speaker-diarization", tags=["diarization_api"])
async def speaker_diarization(audio_file: UploadFile = File(None), youtube_video_id: Optional[str] = None):
    """
    Endpoint to perform speaker diarization on audio file or YouTube video.

    :param audio_file: Uploaded audio file (if provided).
    :param youtube_video_id: ID of the YouTube video (if provided).
    :return: Diarization result containing transcript and dialogue.
    """
    try:
        if audio_file is not None:
            audio_data = await audio_file.read()
            filename = audio_file.filename
            response = process_audio(audio_data, filename)
        if youtube_video_id:
            response = process_youtube_video(youtube_video_id)

        return response
    except Exception as e:
        logging.error(f'/speaker_diarization:/500, {e}')
