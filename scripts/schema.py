from pydantic  import BaseModel

class Request(BaseModel):
    prompt : str = """Identify and extract dialogue involving a therapist and multiple children/teens from the provided text. Present the conversation in the following format:

        Therapist:
        Child 1:
        Child 2:
        ...."""
