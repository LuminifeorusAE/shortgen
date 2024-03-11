from moviepy.editor import VideoFileClip
import os
import random

class VideoCutter:
    def __init__(self, input_dir='footages', output_dir='cut_videos'):
        self.input_dir = input_dir
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def cut_videos(self):
        total_duration = 0
        cut_files = []
        
        while total_duration < 55:
            for filename in os.listdir(self.input_dir):
                if filename.endswith('.mp4'):
                    file_path = os.path.join(self.input_dir, filename)
                    clip = VideoFileClip(file_path)
                    
                    # Generate random start and end times for cutting
                    start_time = random.uniform(0, clip.duration - 6)  # Ensure at least 6 seconds left
                    end_time = start_time + random.uniform(5, 6)
                    if end_time > clip.duration:
                        end_time = clip.duration
                    
                    # Cut the video segment
                    cut_clip = clip.subclip(start_time, end_time)
                    cut_duration = cut_clip.duration
                    total_duration += cut_duration
                    
                    # Save the cut video segment
                    output_filename = f"cut_{filename}"
                    output_path = os.path.join(self.output_dir, output_filename)
                    cut_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
                    
                    # Close the clip to free up resources
                    cut_clip.close()
                    
                    cut_files.append(output_path)
                    
                    print(f"Total duration of all cut videos: {total_duration} seconds")
                    
                    if total_duration >= 55:
                        break  # Stop cutting if total duration reaches 55 seconds or more
            
            if total_duration < 55:
                print("Total duration is less than 55 seconds. Cutting another video...")
            elif total_duration > 59:
                print("Total duration exceeded 59 seconds. Adjusting last video...")
                # Adjust the last video segment if total duration exceeds 60 seconds
                last_output_path = cut_files[-1]
                last_clip = VideoFileClip(last_output_path)
                excess_duration = total_duration - 59
                last_duration = last_clip.duration - excess_duration
                last_clip = last_clip.subclip(0, last_duration)
                last_clip.write_videofile(last_output_path, codec="libx264", audio_codec="aac")
                last_clip.close()
                total_duration = 59  # Set total duration to 59 seconds
        
        print(f"Total duration of all cut videos: {total_duration} seconds")
        return cut_files, total_duration
    
cutter = VideoCutter()
downloaded_video_paths, total_duration = cutter.cut_videos()
