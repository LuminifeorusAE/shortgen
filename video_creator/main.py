#main.py
from video_downloader import PexelsVideoDownloader
from concatenate_videos import VideoConcatenator 

def main():
    downloader = PexelsVideoDownloader()
    downloader.main()
    folder_path = "footages"  # Adjust the folder path accordingly
    concatenator = VideoConcatenator(folder_path)
    concatenator.concatenate_videos()

if __name__ == "__main__":
    main()

