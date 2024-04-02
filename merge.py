import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

class VideoMerger:
    def __init__(self, video_dir, output_path):
        """• Constructor takes two parameters for where to take videos, and where to put edited videos"""
        self.video_dir = video_dir
        self.output_path = output_path
    
        
    def adjust_video_properties(self, video_path, output_path, aspect_ratio=(9, 16)):
        """• Function is defined to adjust differend video parameters as aspect ratio, codecs and fps to each outher
           • These lines calculate the dimensions for center cropping the video based on the specified aspect ratio. 
            It ensures that the cropped video maintains the aspect ratio while maximizing the dimensions.
        """
        clip = VideoFileClip(video_path)
        
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
        """
        • Method collects all the video files in the specified directory, adjusts each video's properties, as the previous function defines
        • After adjusting all videos, the clips are concatenated together
        • The resulting final clip is written to the specified path with a frame rate of 30 frames per second.
        """
        output_directory = "merged_video"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        video_files = [f for f in os.listdir(self.video_dir) if f.endswith('.mp4')]
        clips = []
        for video_file in video_files:
            video_path = os.path.join(self.video_dir, video_file)
            adjusted_video_path = os.path.join(output_directory, f"{os.path.splitext(video_file)[0]}_adjusted.mp4")
            self.adjust_video_properties(video_path, adjusted_video_path, aspect_ratio=(9, 16))
    
            clips.append(VideoFileClip(adjusted_video_path))
        
        final_clip = concatenate_videoclips(clips, method='compose')
        final_clip.write_videofile(os.path.join(output_directory, self.output_path), fps=30)
        final_clip.close()

if __name__ == "__main__":
    video_dir = "cut_videos"  # Directory containing the input video files
    output_path = "merged_video.mp4"  # Path to the output merged video file

    merger = VideoMerger(video_dir, output_path)
    merger.merge_videos()
