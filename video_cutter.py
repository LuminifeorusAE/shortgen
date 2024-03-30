from moviepy.editor import VideoFileClip
import os
import random

"""
#cutvideos

Module for cutting video clips from a directory of video files.
"""

class VideoCutter:
    """Class for cutting video clips from a directory of video files."""

    def __init__(self, input_dir='footages', output_dir='cut_videos'):
        """Initialize the VideoCutter instance.

        Args:
            input_dir (str): Path to the directory containing input video files.
            output_dir (str): Path to the directory to save the cut video files.
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def check_video_count(self, min_count=10):
        """Check if there are enough video files in the input directory.

        Args:
            min_count (int): Minimum number of video files required.

        Returns:
            bool: True if there are 'min_count' or more video files, False otherwise.
        """
        video_count = sum(1 for file in os.listdir(self.input_dir) if file.endswith('.mp4'))
        return video_count >= min_count

    def cut_videos(self, min_duration=55, max_duration=59):
        """Cut video clips from input video files and save them to the output directory.

        Args:
            min_duration (int): Minimum duration of the combined video clips.
            max_duration (int): Maximum duration of the combined video clips.

        Returns:
            tuple: A tuple containing a list of paths to the cut video files and the total duration of all cut videos.
        """
        if not self.check_video_count():
            print("There are not enough videos in the directory to start cutting.")
            return [], 0

        total_duration = 0
        cut_files = []

        try:
            while total_duration < min_duration:
                for filename in os.listdir(self.input_dir):
                    if filename.endswith('.mp4'):
                        file_path = os.path.join(self.input_dir, filename)
                        clip = VideoFileClip(file_path)

                        start_time = random.uniform(0, clip.duration - 4)
                        max_clip_duration = min(max_duration - total_duration, clip.duration - start_time)
                        end_time = start_time + random.uniform(3, max_clip_duration)

                        try:
                            cut_clip = clip.subclip(start_time, end_time)
                            cut_duration = cut_clip.duration
                            total_duration += cut_duration

                            output_filename = f"cut_{filename}"
                            output_path = os.path.join(self.output_dir, output_filename)
                            cut_clip.write_videofile(output_path, codec="libx264", audio=False)

                            cut_clip.close()
                            cut_files.append(output_path)
                            print(f'Total duration of all cut videos: {total_duration} seconds')

                            if total_duration >= min_duration:
                                return cut_files, total_duration
                        except Exception as e:
                            print(f"Error processing file {file_path}: {e}")
                            continue

                if total_duration < min_duration:
                    print("Total duration is less than the minimum required. Cutting another video...")
                elif total_duration > max_duration:
                    print("Total duration exceeds the maximum allowed. Deleting one video...")

                    last_output_path = cut_files[-1]
                    last_clip = VideoFileClip(last_output_path)
                    extra_duration = total_duration - max_duration
                    last_duration = last_clip.duration - extra_duration
                    last_clip = last_clip.subclip(0, last_duration)
                    last_clip.write_videofile(last_output_path, codec="libx264", audio_codec='aac')
                    last_clip.close()
                    total_duration = max_duration
                    print(f"Total duration of all cut videos: {total_duration} seconds")
                    return cut_files, total_duration
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return cut_files, total_duration  # Ensure the method returns the values even if the loop terminates early



if __name__ == "__main__":            
    cutter = VideoCutter()
    downloaded_video_paths, total_duration = cutter.cut_videos()
