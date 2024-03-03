#concatenate_videos.py
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

class VideoConcatenator:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def get_videos(self):
        video_files = []
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".mp4"):
                filepath = os.path.join(self.folder_path, filename)
                clip = VideoFileClip(filepath)
                duration = clip.duration
                if 45 <= duration <= 60:
                    video_files.append(filepath)
                clip.close()
        return video_files

    def concatenate_videos(self):
        video_files = self.get_videos()
        total_duration = sum(duration for _, duration in video_files)
        print("Total duration:", total_duration)  # Debugging statement
        
        # Check if total duration meets the criteria
        if 55 <= total_duration <= 60 and len(video_files) > 1:
            # Concatenate videos
            clips = [VideoFileClip(filepath) for filepath, _ in video_files]
            concatenated_clip = concatenate_videoclips(clips)
            concatenated_clip.write_videofile("concatenated_video.mp4", codec="libx264")
            concatenated_clip.close()
            print("Concatenated video saved as 'concatenated_video.mp4'")
        elif len(video_files) == 1 and 55 <= video_files[0][1] <= 60:
            print("Single video meets duration criteria. No concatenation needed.")
        else:
            print("Insufficient videos or total duration does not meet criteria.")


