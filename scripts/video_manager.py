import yt_dlp as youtube_dl

class VideoDownloader:
    def __init__(self, output_path):
        """
        Initialize the VideoDownloader class.

        Args:
            output_path (str): The directory where downloaded videos will be saved.
        """
        self.output_path = output_path
        self.ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': self.output_path,
            'extractor_lazy': True,  # Bypass uploader ID extraction
        }

    def download_video(self, video_url):
        """
        Download a video from the provided URL.

        Args:
            video_url (str): The URL of the video to be downloaded.
        """
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([video_url])

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=96daW-XQpmE"
    output_path = "/path/to/videos/folder"
    
    # Create an instance of the VideoDownloader class
    downloader = VideoDownloader(output_path)
    
    # Download the video using the provided URL
    downloader.download_video(video_url)
