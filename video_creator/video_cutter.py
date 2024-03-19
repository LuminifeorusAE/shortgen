#cutvideos

from moviepy.editor import VideoFileClip
import os
import random

"""
• Module moviepy.editor used to represent a video file as a clip, allowing you to perform various operations such as cutting, concatenating, and applying effects.
• Module os is used to manipulate file paths, check for file existence, create directories if they don't exist, and list files in a directory.
random is used to generate random start and end times for cutting video segments within specified ranges. This randomness adds variability to the selection of video segments to cut.
• Module random is used to generate random start and end times for cutting video segments within specified ranges. This randomness adds variability to the selection of video segments to cut.
"""

class VideoCutter:
    def __init__(self, input_dir = 'footages', output_dir='cut_videos'):
        """ • Method to initialize input and output directories. If the output directory doesn't exist, it creates one."""
        self.input_dir = input_dir
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def cut_videos(self):
        """
        • Defines a method cut_videos within the class. It initializes total_duration and cut_files lists.
        • Iterates through each file in the input directory. If the file has a '.mp4' extension, it constructs the file's full path and creates a VideoFileClip object.
        • Randomly generates start and end times for cutting the video. It ensures that at least 6 seconds are left after the start time and adjusts the duration if the remaining clip is too short.
        • Cuts the video segment according to the generated start and end times, calculates its duration, and updates the total duration.
        • Defines the output filename, constructs the output path, and saves the cut video segment with specified codec and audio settings.
        • Closes the clip to free up resources, appends the output path to the list of cut files, and prints the total duration of all cut videos.
        • Breaks the loop if the total duration of all cut videos reaches or exceeds 55 seconds.
        • Catches any exceptions that may occur during video processing, prints an error message, and continues with the next file.
        • Checks if the total duration is less than 55 seconds or exceeds 59 seconds. If the latter, it adjusts the last video segment's duration to ensure it doesn't exceed 59 seconds.
        """
        
        total_duration = 0
        cut_files = []


        while total_duration < 59:
            for filename in os.listdir(self.input_dir):
                if filename.endswith('mp4'):
                    file_path = os.path.join(self.input_dir, filename)
                    clip = VideoFileClip(file_path)

                    start_time = random.uniform(0, clip.duration - 4)
                    max_duration = min(6, clip.duration-start_time)
                    end_time = start_time+random.uniform(3, max_duration)

                    try:
                        cut_clip = clip.subclip(start_time, end_time)
                        cut_duration = cut_clip.duration
                        total_duration +=cut_duration

                        output_filename = f"cuted{filename}"
                        output_path = os.path.join(self.output_dir, output_filename)
                        cut_clip.write_videofile(output_path, codec = "libx264", audio = False)

                        cut_clip.close()
                        cut_files.append(output_path)
                        print(f'Total durations of all cut videos: {total_duration} seconds')

                        if total_duration >= 55:
                            break
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")
                        continue
            if total_duration < 55:
                print(f"Total duration is less than 55 seconds. Cutting another video...")
            elif total_duration > 59:
                print("Total duration is more then 59 seconds.Deleting one video...")

                last_output_path = cut_files[-1]
                last_clip = VideoFileClip(last_output_path)
                not_enaugh_duration = total_duration - 59
                last_duration = last_clip.duration - not_enaugh_duration
                last_clip = last_clip.subclip(0,last_duration)
                last_clip.write_videofile(last_output_path, codec = "libx264", audio_codec = 'aac')
                last_clip.close()
                total_duration = 59
                print(f"Total duration of all cut videos: {total_duration} seconds")
                return cut_files, total_duration
            
cutter = VideoCutter()
downloaded_video_paths, total_duration = cutter.cut_videos()