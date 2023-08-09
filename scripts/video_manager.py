import os
import subprocess
import yt_dlp as youtube_dl

class VideoDownloader:
    def __init__(self, output_path, audio_output_path):
        """
        Initialize the VideoDownloader class.

        Args:
            output_path (str): The directory where downloaded videos will be saved.
            audio_output_path (str): The directory where audio files will be saved.
        """
        self.output_path = output_path
        self.audio_output_path = audio_output_path
        self.ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
            'extractor_lazy': True,  # Bypass uploader ID extraction
        }

    def download_video(self, video_url):
        """
        Download a video from the provided URL and convert to audio.

        Args:
            video_url (str): The URL of the video to be downloaded and converted.
        """
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_path = os.path.join(self.output_path, ydl.prepare_filename(info_dict))

            # Check if the downloaded file is a video
            mime_type = subprocess.check_output(["file", "-b", "--mime-type", video_path]).decode("utf-8").strip()
            if mime_type.startswith("video/"):
                # Get the video file name without the extension
                video_name_no_extension = os.path.splitext(os.path.basename(video_path))[0]

                # Run ffmpeg command to convert the video to audio
                audio_output_path = os.path.join(self.audio_output_path, f"{video_name_no_extension}.wav")
                subprocess.run(["ffmpeg", "-i", video_path, "-ar", "16000", "-ac", "1", audio_output_path])

                print(f"Converted {video_name_no_extension}.wav")

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=96daW-XQpmE"
    output_path = "/path/to/videos/folder"
    audio_output_path = "/path/to/audios/folder"
    
    # Create instances of the VideoDownloader class
    downloader = VideoDownloader(output_path, audio_output_path)
    
    # Download the video and convert to audio using the provided URL
    downloader.download_video(video_url)
    
    print("Conversion complete!")
