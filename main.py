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
    
    # Search for videos based on the theme with resolution filtering
    filtered_videos = downloader.search_videos(theme, num_videos)
    
    # Check if there are any filtered videos
    if filtered_videos:
        # Randomly select videos from the filtered list
        selected_videos = random.sample(filtered_videos, min(NUM_VIDEOS_TO_DOWNLOAD, len(filtered_videos)))
        
        # Print out all the links from the selected videos for downloading
        print("Links from Selected Videos for Downloading:")
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

    merger = VideoMerger(video_dir, output_path)
    merger.merge_videos()

    video_path = output_path
    music_folder = "music"
    output_dir = "final_videos"
          
        # Initialize VideoEditor
    video_editor = VideoEditor(video_path, music_folder, output_dir)
          
          # Add random music to the merged video
    video_editor.add_random_music()



