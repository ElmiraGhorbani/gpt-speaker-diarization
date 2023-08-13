# GPT-Diarization

This project revolves around leveraging advanced AI language models to perform speaker diarization on conversation transcripts. Speaker diarization involves segmenting spoken content into distinct portions belonging to different speakers. This approach simplifies the analysis of conversations by providing clear, structured outputs that highlight the interactions among various speakers.


## Getting started

### Run NoteBook

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



NOTE: set your OpenAI API key.  (source in docker-compose).


```

docker-compose up -d

```

open FastApi swagger, hit try it out.

```
http://0.0.0.0:8012/docs
```
## TODO
[ ] complete notebook