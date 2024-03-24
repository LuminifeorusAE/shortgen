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
    def __init__(self, input_dir='footages', output_dir='cut_videos'):
        self.input_dir = input_dir
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def check_video_count(self):
        video_count = sum(1 for file in os.listdir(self.input_dir) if file.endswith('.mp4'))
        return video_count >= 10

    def cut_videos(self):
        if not self.check_video_count():
            print("There are not enough videos in the directory to start cutting.")
            return

        total_duration = 0
        cut_files = []

        while total_duration < 59:
            for filename in os.listdir(self.input_dir):
                if filename.endswith('.mp4'):
                    file_path = os.path.join(self.input_dir, filename)
                    clip = VideoFileClip(file_path)

                    start_time = random.uniform(0, clip.duration - 4)
                    max_duration = min(6, clip.duration - start_time)
                    end_time = start_time + random.uniform(3, max_duration)

                    try:
                        cut_clip = clip.subclip(start_time, end_time)
                        cut_duration = cut_clip.duration
                        total_duration += cut_duration

                        output_filename = f"cuted_{filename}"
                        output_path = os.path.join(self.output_dir, output_filename)
                        cut_clip.write_videofile(output_path, codec="libx264", audio=False)

                        cut_clip.close()
                        cut_files.append(output_path)
                        print(f'Total durations of all cut videos: {total_duration} seconds')

                        if total_duration >= 55:
                            break
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")
                        continue

            if total_duration < 55:
                print("Total duration is less than 55 seconds. Cutting another video...")
            elif total_duration > 59:
                print("Total duration is more than 59 seconds. Deleting one video...")

                last_output_path = cut_files[-1]
                last_clip = VideoFileClip(last_output_path)
                not_enough_duration = total_duration - 59
                last_duration = last_clip.duration - not_enough_duration
                last_clip = last_clip.subclip(0, last_duration)
                last_clip.write_videofile(last_output_path, codec="libx264", audio_codec='aac')
                last_clip.close()
                total_duration = 59
                print(f"Total duration of all cut videos: {total_duration} seconds")
                return cut_files, total_duration
if __name__ == "__main__":            
    cutter = VideoCutter()
    downloaded_video_paths, total_duration = cutter.cut_videos()