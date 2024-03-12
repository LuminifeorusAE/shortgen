import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

class VideoMerger:
    def __init__(self, video_dir, output_path):
        self.video_dir = video_dir
        self.output_path = output_path
    
    def adjust_video_properties(self, video_path, output_path, duration=None, aspect_ratio=(9, 16)):
        clip = VideoFileClip(video_path)
        if duration is None:
            duration = 5.0
        clip = clip.subclip(0, duration)
        
        # Calculate dimensions for center cropping
        original_width, original_height = clip.size
        target_width = original_height * aspect_ratio[0] // aspect_ratio[1]
        if target_width > original_width:
            target_width = original_width
            target_height = original_width * aspect_ratio[1] // aspect_ratio[0]
            x_offset = 0
            y_offset = (original_height - target_height) // 2
        else:
            target_height = original_height
            x_offset = (original_width - target_width) // 2
            y_offset = 0
        
        # Crop the center part of the video
        clip_cropped = clip.crop(x_center=x_offset, y_center=y_offset, width=target_width, height=target_height)
        
        # Resize to the specified resolution
        clip_resized = clip_cropped.resize((720, 1280))
        
        # Write the adjusted video to the output path
        clip_resized.write_videofile(output_path, fps=30)  # Set FPS here
        
        # Close the clips
        clip.close()
        clip_cropped.close()
        clip_resized.close()

    def merge_videos(self):
        video_files = [f for f in os.listdir(self.video_dir) if f.endswith('.mp4')]
        clips = []
        for video_file in video_files:
            video_path = os.path.join(self.video_dir, video_file)
            adjusted_video_path = os.path.join(self.video_dir, f"{os.path.splitext(video_file)[0]}_adjusted.mp4")
            self.adjust_video_properties(video_path, adjusted_video_path, duration=5.0, aspect_ratio=(9, 16))
    
            clips.append(VideoFileClip(adjusted_video_path))  # Append the adjusted clip
        
        final_clip = concatenate_videoclips(clips, method='compose')
        final_clip.write_videofile(self.output_path, fps=30)  # Set FPS here
        final_clip.close()

if __name__ == "__main__":
    video_dir = "cut_videos"  # Directory containing the input video files
    output_path = "merged_video.mp4"  # Path to the output merged video file

    merger = VideoMerger(video_dir, output_path)
    merger.merge_videos()
