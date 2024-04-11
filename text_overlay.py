import os
import random
from moviepy.editor import *

class VideoTextOverlay:
    def __init__(self, video_directory, captions_directory, output_directory):
        self.video_directory = video_directory
        self.captions_directory = captions_directory
        self.output_directory = output_directory
        self.index_file = "last_used_index.txt"
        self.last_index = self._load_last_index()

    def _load_last_index(self):
        if os.path.exists(self.index_file):
            with open(self.index_file, "r") as f:
                return int(f.read().strip())
        else:
            return 0

    def _get_next_caption(self):
        caption_files = sorted(os.listdir(self.captions_directory))
        caption_file = caption_files[self.last_index]
        text_file_path = os.path.join(self.captions_directory, caption_file)
        with open(text_file_path, "r") as file:
            text = file.readline().strip()
        self.last_index = (self.last_index + 1) % len(caption_files)
        with open(self.index_file, "w") as f:
            f.write(str(self.last_index))
        return text

    def overlay_text_on_videos(self):
        files = os.listdir(self.video_directory)
        video_files = [file for file in files if file.endswith(".mp4")]

        for video_file in video_files:
            video_clip = VideoFileClip(os.path.join(self.video_directory, video_file))
            text = self._get_next_caption()

            text_clip = TextClip(txt=text, size=(800, 0), font="Verdana-bold", color="black")
            text_width, text_height = text_clip.size
            color_clip = ColorClip(size=(text_width + 100, text_height + 50), color=(0, 255, 255)).set_opacity(.4)
            text_clip = text_clip.set_position(('center'))
            clip_to_overlay = CompositeVideoClip([color_clip, text_clip]).set_position('center')
            clip_to_overlay = clip_to_overlay.set_duration(video_clip.duration)
            final_clip = CompositeVideoClip([video_clip, clip_to_overlay])

            output_file = os.path.join(self.output_directory, video_file)
            final_clip.write_videofile(output_file, codec="libx264")
            video_clip.close()

if __name__ == "__main__":
    video_overlay = VideoTextOverlay("final_videos", "captions", "output_videos")
    video_overlay.overlay_text_on_videos()
