from video_downloader import VideoDownloader
from video_cutter import VideoCutter
from merge import VideoMerger
from music import VideoEditor
import random
import os

NUM_VIDEOS_TO_DOWNLOAD = 10  # Set the desired number of videos to download

if __name__ == "__main__":
    # Create an instance of VideoDownloader
    print("Initializing VideoDownloader instance...")
    downloader = VideoDownloader()
    theme = random.choice(downloader.themes)
    num_videos = 1000
    
    # Ensure the 'footages' directory exists or create it if it doesn't
    output_folder = 'footages'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Directory '{output_folder}' created.")

    # Search for videos based on the theme with resolution filtering
    filtered_videos = downloader.search_videos(theme, num_videos)
    
    # Check if there are any filtered videos
    if filtered_videos:
        # Randomly select videos from the filtered list
        selected_videos = random.sample(filtered_videos, min(NUM_VIDEOS_TO_DOWNLOAD, len(filtered_videos)))
        
        # Print out all the links from the selected videos for downloading
        print("Links Containing HD Videos for Downloading: \n")
        print(f"Downloading {NUM_VIDEOS_TO_DOWNLOAD} videos from {theme} theme")
        for video in selected_videos:
            print(f"Video ID: {video['id']}")
            links = [vf['link'] for vf in video.get('video_files', []) if 'hd' in vf['link']]
            for link in links:
                print(link)

        # Start downloading the selected videos
        print("\nStarting Download...")
        for video in selected_videos:
            downloader.download_video(video, 'footages')
    else:
        print("No videos found with resolutions higher than the minimum set resolution.")

    cutter = VideoCutter()
    downloaded_video_paths, total_duration = cutter.cut_videos()

    video_dir = "cut_videos" 
    output_path = "merged_video.mp4"  

    video_dir = "cut_videos"  # Directory containing the input video files
    output_path = "merged_video.mp4"  # Path to the output merged video file

    merger = VideoMerger(video_dir, output_path)
    merger.merge_videos()

    # Search for the "merged_video.mp4" file in the merged video directory
    merged_video_dir = "merged_video"
    merged_video_path = os.path.join(merged_video_dir, "merged_video.mp4")

    # Check if the file exists
    if os.path.exists(merged_video_path):
        print("Found merged video:", merged_video_path)
        # Use the path to the merged video in your script
        video_path = merged_video_path
    else:
        print("Merged video not found:", merged_video_path)
        # Handle the case where the merged video is not found

    music_folder = "music"
    output_dir = "final_videos"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    video_editor = VideoEditor(video_path, music_folder, output_dir)
    
    video_editor.add_music_from_index()
# Detect and delete MP4 files in the "final_videos" directory

    mp4_in_final_videos = any(filename.endswith(".mp4") for filename in os.listdir(output_dir))

    if mp4_in_final_videos:
        print("MP4 file found in 'final_videos' directory. Deleting videos...")
        for directory in ["cut_videos", "merged_video", "footages"]:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if filename.endswith(".mp4"):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
        print("Videos deleted successfully.")
    else:
        print("No MP4 file found in 'final_videos' directory.")