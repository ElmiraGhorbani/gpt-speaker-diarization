import os

import auditok
import openai
import soundfile as sf
from openai_decorator import retry_on_openai_errors

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

    def vad_audiotok(self, audio_content):
        """
        voice activity detection (audiotok package)

        :type audio_content: bytes
        :param audio_content: PyAv content

        :return: chunks contain speech
        """
        audio_regions = auditok.split(
            audio_content,
            sr=16000,
            ch=1,
            sw=2,
            min_dur=0.5,     # minimum duration of a valid audio event in seconds
            max_dur=30,       # maximum duration of an event
            max_silence=0.3,  # maximum duration of tolerated continuous silence within an event
            energy_threshold=30  # threshold of detection
        )
        return audio_regions

    def audio_process(self, wav_path):
        with open(wav_path, 'rb') as f:
            wav_bytes = f.read()
        wav, sr = sf.read(wav_path)
        audio_regions = self.vad_audiotok(wav_bytes)
        wav_segments = []
        for r in audio_regions:
            start = r.meta.start
            end = r.meta.end
            segment = wav[int(start * 16000):int(end * 16000)]
            wav_segments.append(segment)
        return wav_segments

    @retry_on_openai_errors(max_retry=7)
    def transcribe(self, audio_file):
        # Save audio bytes as a temporary WAV file
        root_path = ""
        temp_wav_path = f"{root_path}/temp_audio.wav"
        with sf.SoundFile(temp_wav_path, 'wb', samplerate=16000, channels=1) as f:
            f.write(audio_file)

        auf = open(temp_wav_path, 'rb')
        # Transcribe using OpenAI API
        response = openai.Audio.transcribe_raw(
            self.model_name, auf, filename=temp_wav_path)

        # Clean up temporary file
        os.remove(temp_wav_path)

        return response['text']


if __name__ == "__main__":
    wh = Whisper()
    with open("./audios/0_edited.wav", "rb") as f:
        audio_content = f.read()
    print(type(audio_content))
    segments = wh.audio_process(
        "./audios/0_edited.wav")
