from video_downloader import VideoDownloader
from video_cutter import VideoCutter
from merge import VideoMerger

def main(): 
    # Calling video downloader
    downloader = VideoDownloader()  # Create an instance of PexelsVideoDownloader
    downloader.main()
    
    # Cutting the videos to 5-second long videos
    cutter = VideoCutter()
    downloaded_video_paths, total_duration = cutter.cut_videos()
    print("Videos downloaded and cut successfully:", downloaded_video_paths, total_duration)

    # Merging cut videos
    merger = VideoMerger(video_dir="cut_videos", output_path="merged_video.mp4")
    merger.merge_videos()
    print("Videos downloaded, cut, and merged successfully.")

if __name__ == "__main__":
    main()
