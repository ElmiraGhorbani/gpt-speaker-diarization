import os

from tinytag import TinyTag

def get_project_root():
    # Get the absolute path of the current file
    current_path = os.path.abspath(__file__)
    # Return the parent directory (project root)
    return os.path.dirname(os.path.dirname(current_path))

def file_to_binary(audio_file):
    with open(audio_file, 'rb') as f:
        return f.read()

def get_file_duration(audio_file):
    return TinyTag.get(audio_file).duration