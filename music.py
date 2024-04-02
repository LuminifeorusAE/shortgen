import os
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.audio.fx.all import audio_fadeout

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the video file
video_dir = os.path.join(script_dir, "merged_video")
video_path = os.path.join(video_dir, "merged_video.mp4")

music_folder = 'music'
output_dir = 'final_videos'
index_file = 'last_chosen_index.txt'

class VideoEditor:
    def __init__(self, video_path, music_folder, output_dir):
        """
        Initialize the VideoEditor instance.

        Args:
            video_path (str): Path to the video file to which music will be added.
            music_folder (str): Path to the folder containing music files.
            output_dir (str): Path to the directory where the final videos will be saved.
        """
        self.video_path = video_path
        self.music_folder = music_folder
        self.output_dir = output_dir
        print("Video path:", self.video_path)
    
    def add_music_from_index(self, output_filename='reel.mp4', fade_duration=4):
        """
        Add a music clip from the specified folder to the video based on the last chosen index.

        Args:
            output_filename (str): Name of the output video file with the added music.
            fade_duration (float): Duration (in seconds) of the fade-out effect applied to the music.

        """
        # Load video clip
        print("Attempting to load video from path:", self.video_path)
        video_clip = VideoFileClip(self.video_path)
        print("Loaded video:", self.video_path)
        
        # Read the last chosen index from the index file
        last_chosen_index = self._get_last_chosen_index()
        print("Last chosen index:", last_chosen_index)
        
        # Get list of music files in the specified folder
        music_files = [f for f in os.listdir(self.music_folder) if os.path.isfile(os.path.join(self.music_folder, f))]
        print("Music files:", music_files)
        
        # Ensure there are music files in the folder
        if not music_files:
            raise ValueError("No music files found in the specified folder.")
        
        # Calculate the index to choose from based on the last chosen index
        index_to_choose = last_chosen_index % len(music_files)
        print("Index to choose:", index_to_choose)
        
        # Load the chosen music file
        chosen_music_file = music_files[index_to_choose]
        print("Chosen music file:", chosen_music_file)
        music_clip = AudioFileClip(os.path.join(self.music_folder, chosen_music_file))
        
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
        
        # Update the last chosen index for next run
        self._update_last_chosen_index(index_to_choose)

    def _get_last_chosen_index(self):
        """
        Read the last chosen index from the index file.
        If the index file doesn't exist or is empty, return 0.

        Returns:
            int: Last chosen index.
        """
        if os.path.exists(index_file):
            with open(index_file, 'r') as f:
                last_chosen_index = int(f.read().strip())
        else:
            last_chosen_index = 0
        return last_chosen_index

    def _update_last_chosen_index(self, index):
        """
        Update the last chosen index in the index file.

        Args:
            index (int): Index to be written to the index file.
        """
        with open(index_file, 'w') as f:
            f.write(str(index + 1))

if __name__ == "__main__":
    video_editor = VideoEditor(video_path, music_folder, output_dir)
    video_editor.add_music_from_index()
