import os
from video_downloader import VideoDownloader
from video_cutter import VideoCutter
from merge import VideoMerger

def main():
    # Define directories
    download_dir = "downloaded_videos"
    cut_dir = "cut_videos"
    output_path = "merged_video.mp4"

    # Download videos
    downloader = VideoDownloader()
    theme = downloader.themes[0]  # Choose a theme
    num_videos = 10
    videos = downloader.search_videos(theme, num_videos)
    downloader.download_videos(videos, download_dir)

    # Cut videos
    cutter = VideoCutter(download_dir, cut_dir)
    cutter.cut_videos()

    # Merge videos
    merger = VideoMerger(cut_dir, output_path)
    merger.merge_videos()

    # Clean up
    clean_up_directory(download_dir)
    clean_up_directory(cut_dir)

def clean_up_directory(directory):
    if os.path.exists(directory):
        for file in os.listdir(directory):
            os.remove(os.path.join(directory, file))
        os.rmdir(directory)

if __name__ == "__main__":
    main()
