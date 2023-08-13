# GPT- Speaker Diarization

This project is centered around harnessing the capabilities of advanced AI language models (specifically, gpt-4) to conduct speaker diarization on conversation transcripts, which are sourced from the OpenAI Whisper API. Speaker diarization involves segmenting spoken content into distinct portions belonging to different speakers. This approach simplifies the analysis of conversations by providing clear, structured outputs that highlight the interactions among various speakers.

## Getting started

### How to Run

#### Installation

FFMPEG is needed as prerquisites to install the requirements.

```

# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg

```

```

pip install -r requirements.txt

pip install --force-reinstall https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz

```

***or just run first cell in ./notebook/How_To_Use_LLMs_For_Diarization.ipynb***

### Run with Docker

NOTE: set your OpenAI API key.  (source in docker-compose).


```

docker-compose up -d

```
or

```

docker pull elmira96/gpt-speaker-diarization:v0.1.0

```

```
docker run -d \
    --name client_diarization \
    -e OPENAI_API_KEY=sk-*** \
    -e NUM_WORKERS=4 \
    -v $(pwd)/resources:/resources:rw \
    -p 8012:8000 \
    elmira96/gpt-speaker-diarization:v0.1.0
```
open FastApi swagger, hit try it out.

```
http://0.0.0.0:8012/docs
```