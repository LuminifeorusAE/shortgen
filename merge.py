import os 
from moviepy.editor import VideoFileClip, concatenate_videoclips



class VideoMerger:
    def __init__(self, video_dir, output_path):
        """• Constructor takes two parameters for where to take videos, and where to put edited videos"""
        self.video_dir = video_dir
        self.output_path = output_path

    def adjust_video_parameters(self, video_path, output_path, aspect_ratio =(9,16)):
        """• Function is defined to adjust differend video parameters as aspect ratio, codecs and fps to each outher
           • These lines calculate the dimensions for center cropping the video based on the specified aspect ratio. 
            It ensures that the cropped video maintains the aspect ratio while maximizing the dimensions.
        """
        # loads the video file using VideoFileClip from moviepy
        clip = VideoFileClip(video_path)

        #calculates dimensions for center croping 

        #retrieves the original width and height of the video clip.
        original_width, original_height = clip.size
        # calculates the width of the cropped region.
        # It multiplies the original height of the video by the first value of the aspect ratio tuple and divides the result by the second value.
        target_width = original_height * aspect_ratio[0] // aspect_ratio[1]

        if target_width > original_width:
            # sets the target width to the original width to ensure no horizontal cropping is needed
            target_width = original_width
            # it calculates the target height based on the aspect ratio
            target_height = original_width * aspect_ratio[1] // aspect_ratio[0]
            # x-offset is set to 0
            x_offset = 0
            # y-offset is calculated to center the cropped region vertically.
            y_offset = (original_height - target_height) // 2
            # handles the case where the calculated target width is less than/equal to the original width
        else:
            #sets the target height to the original height to ensure no vertical cropping is needed
            target_height = original_height
            # it calculates the x-offset to center the cropped region horizontally
            x_offset = (original_width - target_width) // 2
            # y-offset is set to 0 since there's no need for vertical centering
            y_offset = 0

            # Crops the center part of the video
            clip_cropped = clip.crop(x_center=x_offset, y_center=y_offset, width = target_width, height = target_height)

            # resizes it to the specified resolution (1440,2560)
            clip_resized = clip_cropped.resize((1440,2560))
            # Write the adjusted video to the output path
            clip_resized.write_videofile(output_path, fps = 30) # set fps here

            # Close the clips
            clip.close()
            clip_cropped.close()
            clip_resized.close()

    #function connecting merged video cuts with adjusted parameters
    def merge_videos(self):
        """
        • Method collects all the video files in the specified directory, adjusts each video's properties, as the previous function defines
        • After adjusting all videos, the clips are concatenated together
        • The resulting final clip is written to the specified path with a frame rate of 30 frames per second.
        """
        #defining directory were merged videos will be created
        output_directory = "merged_video"
        #if directory is not created already or deleted create one
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        #selecting video files from the directory
        video_files = [file for file in os.listdir(self.video_dir) if file.endswith('.mp4')]
        #storing them in the list
        clips = []
        # iterating over each video file in the directory
        for video_file in video_files:
            video_path = os.path.join(self.video_dir, video_file)

            # nameing video files according to its name in the directory and adding "adjuted" to identify adjusted videos
            adjusted_video_path = os.path.join(output_directory, f"{os.path.splitext(video_file)[0]}_adjusted.mp4")

            # adjusting all the video clips to each other
            self.adjust_video_parameters(video_path, adjusted_video_path, aspect_ratio = (9,16))
            #joining to make one single video clip to list
            clips.append(VideoFileClip(adjusted_video_path))

            #main proccess of concatenating videos together into one video
            final_clip = concatenate_videoclips(clips, method="compose")
            #creating video file in the directory
            final_clip.write_videofile(os.path.join(output_directory, self.output_path), fps=30)
            #clossing session
            final_clip.close()

# main instance to run script in module or separately
if __name__ == "__main__":
    #directory that script takes the videos
    video_dir = "cut_videos"
    # directory where to create merged video
    output_path = "merged_video.mp4"
    # calling created class with function 
    merger = VideoMerger(video_dir, output_path)
    merger.merge_videos()


