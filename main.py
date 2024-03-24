from video_downloader import VideoDownloader
from video_cutter import VideoCutter
from merge import VideoMerger
import random

if __name__ == "__main__":
   downloader = VideoDownloader()
   theme = random.choice(downloader.themes)
   num_videos = 1000
   videos = downloader.search_videos(theme, num_videos)
   if videos:
        selected_videos = random.sample(videos, min(10, len(videos)))
        downloader.download_videos(theme, num_videos=10, selected_videos=selected_videos)
        cutter = VideoCutter()
        downloaded_video_paths, total_duration = cutter.cut_videos()

        video_dir = "cut_videos"  # Directory containing the input video files
        output_path = "merged_video.mp4"  # Path to the output merged video file

        merger = VideoMerger(video_dir, output_path)
        merger.merge_videos()


