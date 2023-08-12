import logging
from typing import Any, Optional

from fastapi import FastAPI, File, UploadFile

from .speech_to_text import Whisper
from .utils import file_to_binary
from .video_manager import VideoDownloader

downloader = VideoDownloader()
whisper_api = Whisper()


tags_metadata = [
    {
        "name": "whisper_api",
        "description": "Operations with the whisper API. click on the `Try it out` button to test the API.",
    },
    {
        "name": "diarization_api",
        "description": "Operations with the diarization API. click on the `Try it out` button to test the API with youtube video or audio file.",
    },
]


chatbot_responses = {
    422: {"description": "the data that API receive is not what it expected."},
    503: {"description": "the OpenAI service is not available."},
    200: {
        "description": "Return audio file's transcript",
        "content": {
            "application/json": {
                "example": {
                    "output": "",
                }
            }
        }
    },
}
app = FastAPI(
    title="GPT-Diarization Project",
    description="Conversational Speaker Diarization using AI Language Models ",
    version="0.1.0",
    openapi_tags=tags_metadata,
)

logging.basicConfig(level=logging.INFO)


def process_audio(audio_data: bytes):
    # Your logic for processing audio goes here
    pass


def process_youtube_video(video_id: str):
    """
    :param:
    """
    audio_output_path = downloader.download_video(video_id)
    audio_binary = file_to_binary(audio_file=audio_output_path)
    wav_segments = whisper_api.audio_process(audio_binary)
    transcript = []
    for segments in wav_segments:
        transcript.append(whisper_api.transcribe(segments))
    transcript = whisper_api.transcribe(audio_binary)["text"]
    pass


@app.post("/asr", tags=["whisper_api"])
async def asr(audio_file: UploadFile = File(...)):
    """
    this function is a wrapper for the Whisper API and returns the transcript of the audio file.

    """
    try:
        audio_file = await audio_file.read()
        transcript = whisper_api.transcribe(audio_file)
        return transcript
    except Exception as e:
        logging.error(f'/asr:/500, {e}')


@app.post("/speaker-diarization", tags=["diarization_api"])
async def speaker_diarization(audio_file: UploadFile = File(None), youtube_video_id: Optional[str] = None):
    try:
        if audio_file is not None:
            audio_data = await audio_file.read()
            process_audio(audio_data)

        if youtube_video_id:
            process_youtube_video(youtube_video_id)

        return {"message": "Processing completed."}
    except Exception as e:
        logging.error(f'/asr:/500, {e}')
