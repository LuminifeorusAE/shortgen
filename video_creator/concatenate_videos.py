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
                if 55 <= duration <= 60:
                    video_files.append(filepath)
                clip.close()
        return video_files

    def concatenate_videos(self):
        video_files = self.get_videos()
        if len(video_files) < 2:
            print("Insufficient videos found to concatenate.")
            return

        selected_clips = []
        for video_file in video_files:
            clip = VideoFileClip(video_file)
            selected_clips.append(clip)
        
        final_clip = concatenate_videoclips(selected_clips)
        final_clip.write_videofile("concatenated_video.mp4", codec="libx264")
        final_clip.close()
        print("Concatenated video saved as 'concatenated_video.mp4'")
