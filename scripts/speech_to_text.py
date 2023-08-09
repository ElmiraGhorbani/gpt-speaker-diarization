import os

import openai

openai.api_key = os.environ.get(
    "OPENAI_API_KEY", ""
)


class Whisper:
    """
    this class is a wrapper for the OpenAI  whisper API and returns the chatbot response
    """

    def __init__(self, model_name="whisper-1"):
        """
        this function initializes the chatbot
        """
        self.model_name = model_name

    def transcribe(self, audio_file):
        """
        this function is a wrapper for the OpenAI API and returns the audio file transcript
        """
        response = openai.Audio.transcribe_raw(
            self.model_name, audio_file, filename="test.wav")
        return response
