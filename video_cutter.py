from moviepy.editor import VideoFileClip
import os

class VideoCutter:
    def __init__(self, input_dir='footages', output_dir='cut_videos'):
        self.input_dir = input_dir
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def cut_videos(self, duration=3):
        for filename in os.listdir(self.input_dir):
            if filename.endswith('.mp4'):
                file_path = os.path.join(self.input_dir, filename)
                clip = VideoFileClip(file_path)

                try:
                    cut_clip = clip.subclip(0, duration)
                    output_filename = f"cut_{filename}"
                    output_path = os.path.join(self.output_dir, output_filename)
                    cut_clip.write_videofile(output_path, codec="libx264", audio=False)
                    cut_clip.close()
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
                    continue


if __name__ == "__main__":
    cutter = VideoCutter()
    cutter.cut_videos()
