import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.audio.fx.all import audio_fadeout

video_path = 'merged_video.mp4'
music_folder = 'music'
output_dir = 'final_videos'

class VideoEditor:
    def __init__(self, video_path, music_folder, output_dir):
        self.video_path = video_path
        self.music_folder = music_folder
        self.output_dir = output_dir
    
    def add_random_music(self, output_filename='reel.mp4', fade_duration=4):
        # Load video clip
        video_clip = VideoFileClip(self.video_path)
        
        # Get list of music files in the specified folder
        music_files = [f for f in os.listdir(self.music_folder) if os.path.isfile(os.path.join(self.music_folder, f))]
        
        # Choose a random music file from the list
        random_music_file = random.choice(music_files)
        
        # Load the randomly chosen music clip
        music_clip = AudioFileClip(os.path.join(self.music_folder, random_music_file))
        
        # Ensure music duration matches video duration
        if music_clip.duration > video_clip.duration:
            music_clip = music_clip.subclip(0, video_clip.duration)
        
        # Apply fade-out effect to the music
        music_clip = audio_fadeout(music_clip, fade_duration)
        
        # Set the audio of the video clip to the trimmed and faded music clip
        video_clip = video_clip.set_audio(music_clip)
        
        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Construct the output path
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Write the output video with the added music
        video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        # Close the clips
        video_clip.close()
        music_clip.close()


if __name__ == "__main__":
    video_editor = VideoEditor(video_path, music_folder, output_dir)
    video_editor.add_random_music()
