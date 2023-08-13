import os
import subprocess

import yt_dlp as youtube_dl

from .utils import get_project_root


class VideoDownloader:
    def __init__(self):
        """
        Initialize the VideoDownloader class.
        """
        self.root_path = get_project_root()
        self.output_path = os.path.join(self.root_path, "resources/videos")
        self.audio_output_path = os.path.join(
            self.root_path, "resources/audios")
        self.ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
            'extractor_lazy': True,
        }

    def download_video(self, video_id):
        """
        Download a video from the provided URL and convert to audio.

        Args:
            video_url (str): The URL of the video to be downloaded and converted.
        """
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            info_dict = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}", download=True)
            video_path = os.path.join(
                self.output_path, ydl.prepare_filename(info_dict))

            # Check if the downloaded file is a video
            mime_type = subprocess.check_output(
                ["file", "-b", "--mime-type", video_path]).decode("utf-8").strip()
            if mime_type.startswith("video/"):
                # Get the video file name without the extension
                video_name_no_extension = os.path.splitext(
                    os.path.basename(video_path))[0]

                # Run ffmpeg command to convert the video to audio
                audio_output_path = os.path.join(
                    self.audio_output_path, f"{video_name_no_extension}.mp3")
                subprocess.run(["ffmpeg", "-i", video_path, "-ar",
                               "16000", "-ac", "1", "-y" ,audio_output_path])

                print(f"Converted {video_name_no_extension}.mp3")
                return audio_output_path


if __name__ == "__main__":
    video_id = "96daW-XQpmE"
    # Create instances of the VideoDownloader class
    downloader = VideoDownloader()

    # Download the video and convert to audio using the provided URL
    audio_output_path = downloader.download_video(video_id)

    print("Conversion complete!")
