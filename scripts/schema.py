from pydantic  import BaseModel

class Request(BaseModel):
    prompt : str = """Perform speaker diarization on the given text to identify and extract conversations involving multiple speakers. Present the dialogue in the following structured format:
    Speaker 1:
    Speaker 2:
    Speaker 3:
    ..."""