FROM python:3.9-slim

USER root:root

ENV PYTHONUNBUFFERED TRUE

RUN apt-get update && apt-get upgrade --yes

RUN apt install -y wget \
    git \
    g++ \
    libsndfile1-dev \
    default-jre \
    libsndfile1 \
    libsndfile1-dev \
    gcc \
    python-dev \
    pkg-config \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    libavfilter-dev \
    vim \
    curl \
    build-essential \
    ffmpeg



COPY scripts scripts

COPY app.sh .
RUN chmod 777 app.sh
RUN chmod +x app.sh


RUN pip install --upgrade --force-reinstall pip
RUN pip install --upgrade pip setuptools wheel


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install --force-reinstall https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz


RUN \
    echo 'alias python="/usr/local/bin/python3"' >> /root/.bashrc && \
    echo 'alias pip="/usr/local/bin/pip3"' >> /root/.bashrc


SHELL ["/bin/bash", "-c", "source /root/.bashrc"]
CMD ["./app.sh"]
