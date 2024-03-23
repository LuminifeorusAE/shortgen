import os 
from moviepy.editor import VideoFileClip, concatenate_videoclips

class VideoMerger:
    def __init__(self, video_dir,output_dir):
        """• Constructor takes two parameters for where to take videos, and where to put edited videos"""
        self.video_dir = video_dir
        self.output_dir = output_dir


    def adjust_video_properties(self, video_path, output_path, aspect_ratio=(9, 16)):
        """• Function is defined to adjust differend video parameters as aspect ratio, codecs and fps to each outher
           • These lines calculate the dimensions for center cropping the video based on the specified aspect ratio. 
            It ensures that the cropped video maintains the aspect ratio while maximizing the dimensions.
        """
        clip = VideoFileClip(video_path)
        original_width, original_height = clip.size
        main_width = original_height*aspect_ratio[1] // aspect_ratio[1]
        if main_width > original_width:
            #center croping dimension calculation
            main_width = original_width

            main_height = original_height*aspect_ratio[1] // aspect_ratio[1]
            x_offset = 0
            y_offset  =(original_height - main_height) // 2
        else: 
            main_height = original_height
            x_offset = (original_width - main_width) // 2
            y_offset  = 0

        clip_cropped = clip.crop(x_center = x_offset, y_center=y_offset, width=main_width, height=main_height)
        clip_resized = clip_cropped.resize((720,1280))
        clip_resized.write_videofile(output_dir, fps = 30)
        clip.close()
        clip_cropped.close()
        clip_resized.close()
    
    def merge_videos(self):
        """
        • Method collects all the video files in the specified directory, adjusts each video's properties, as the previous function defines
        • After adjusting all videos, the clips are concatenated together
        • The resulting final clip is written to the specified path with a frame rate of 30 frames per second.
        """
        video_files = [file for file in os.listdir(self.video_dir) if file.endswith('.mp4')]
        clips = []
        for video_file in video_files:
            video_path = os.path.join(self.video_dir, video_file)
            adjusted_videos_path = os.path.join(self.video_dir, f"{os.path.splitext(video_file)[0]}_adjusted.mp4")
            self.adjust_video_properties(video_path, adjusted_videos_path, aspect_ratio=(9,16))
            clips.append(VideoFileClip(adjusted_videos_path))

        final_clip = concatenate_videoclips(clips, method = "compose")
        final_clip.write_videofile(self.output_dir, fps = 30)
        final_clip.close

if __name__ == "__main__":
    video_dir = "cut_videos"
    output_dir = "merged_videos.mp4"

    merger = VideoMerger(video_dir, output_dir)
    merger.merge_videos()