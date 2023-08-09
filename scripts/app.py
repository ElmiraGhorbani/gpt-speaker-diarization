import logging


from fastapi import FastAPI, UploadFile, File
from typing import Any



from .speech_to_text import Whisper


whisper_api = Whisper()


tags_metadata = [
    {
        "name": "whisper_api",
        "description": "Operations with the whisper API. click on the `Try it out` button to test the API.",
    }
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
