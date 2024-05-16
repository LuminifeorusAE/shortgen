import os
from moviepy.editor import *

# Class named VideoTextOverlay, which will handle overlaying text on videos.
class VideoTextOverlay:
    """
    Class to overlay text on videos.

    Attributes:
        video_directory (str): Path to the directory containing input videos.
        captions_directory (str): Path to the directory containing caption text files.
        output_directory (str): Path to the directory to save output videos.
        index_file (str): Name of the file to store the index of the last used caption.
        last_index (int): Index of the last used caption.
    """
     # This is the constructor method of the VideoTextOverlay class. It initializes the object with three parameters: video_directory, captions_directory, and output_directory.
    def __init__(self, video_directory, captions_directory, output_directory):
        """
        Initialize VideoTextOverlay object.

        Args:
            video_directory (str): Path to the directory containing input videos.
            captions_directory (str): Path to the directory containing caption text files.
            output_directory (str): Path to the directory to save output videos.
        """
        self.video_directory = video_directory
        self.captions_directory = captions_directory
        self.output_directory = output_directory
        #This file will store the index of the last used caption
        self.index_file = "last_used_index.txt"
        # method to load the last used index from the index file and assigns it to self.last_index
        self.last_index = self._load_last_index()

    def _load_last_index(self):
        """
        Load the index of the last used caption from the index file.

        Returns:
            int: Index of the last used caption.
        """
        if os.path.exists(self.index_file):
            with open(self.index_file, "r") as f:
                return int(f.read().strip())
        else:
            return 0
    # This method gets every next caption text form text file each time script is executed by storing indexin txt file in the directory
    def _get_next_caption(self):
        """
        Get the next caption text from the captions directory.

        Returns:
            str: Next caption text.
        """
        # Lists all files in the captions directory and sorts them alphabetically
        caption_files = sorted(os.listdir(self.captions_directory))

        # Retrieves the caption file based on the last used index.
        caption_file = caption_files[self.last_index]

        # Opens the caption file, reads the first line, strips any leading or trailing whitespace, and assigns it to the text variable.
        text_file_path = os.path.join(self.captions_directory, caption_file)

        # Increments the last used index, and updates the index file.
        with open(text_file_path, "r") as file:
            text = file.readline().strip()
        # wraps it around if it exceeds the number of caption files
        self.last_index = (self.last_index + 1) % len(caption_files)
        # updates the index file.
        with open(self.index_file, "w") as f:
            f.write(str(self.last_index))

        # Returns the text read from the caption file.
        return text

    # This method iterates over each video file, overlays text on each video using the captions obtained from _get_next_caption(), and saves the modified videos to the output directory.
    def overlay_text_on_videos(self):
        """
        Overlay text on input videos and save the modified videos to the output directory.
        """
        #Checks if the output directory specified exists.If it doesn't, it creates the directory and any necessary parent directories
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        # Lists all files in the video directory and stores them in the files variable.
        files = os.listdir(self.video_directory)
        # Filters the list of files to only include those ending with ".mp4" and stores them in the video_files list comprehension.
        video_files = [file for file in files if file.endswith(".mp4")]

        # Iterates over each video file in the list.
        for video_file in video_files:

            # Loads the current video file as a VideoFileClip object using VideoFileClip() from the moviepy.editor module.
            video_clip = VideoFileClip(os.path.join(self.video_directory, video_file))

            # Calls the _get_next_caption() method to retrieve the next caption text
            text = self._get_next_caption()

            # It specifies the text (txt), size, font, and color.
            # Creates a text clip containing the retrieved caption text using TextClip() from the moviepy.editor module.
            text_clip = TextClip(txt=text, size=(900, 0), font="Verdana-bold", color="black")

            # It specifies the text (txt), size, font, and color.
            text_width, text_height = text_clip.size

            # Creates a color clip to serve as the background for the text using ColorClip() from the moviepy.editor module.
            # It specifies the size and color. The opacity is set to 40% using set_opacity()
            color_clip = ColorClip(size=(text_width + 100, text_height + 50), color=(0, 255, 255)).set_opacity(.4)

            # Sets the position of the text clip. 
            
            text_clip = text_clip.set_position(('center'))
            # Creates a composite video clip by overlaying the color clip and text clip at the center of the frame.

            clip_to_overlay = CompositeVideoClip([color_clip, text_clip]).set_position('center')
            # Sets the duration of the composite video clip to match the duration of the original video clip.
            clip_to_overlay = clip_to_overlay.set_duration(video_clip.duration)
            # Creates a final composite video clip by overlaying the original video clip and the composite clip containing the text overlay.
            final_clip = CompositeVideoClip([video_clip, clip_to_overlay])

            # Defines the output file path by joining the output directory path with the name of the original video file.
            output_file = os.path.join(self.output_directory, video_file)

            # Writes the final composite video clip to the output file using write_videofile() from the moviepy.editor module with the H.264 codec.
            final_clip.write_videofile(output_file, codec="libx264")
            
            # Closes the original video clip using close() to release system resources.
            video_clip.close()

if __name__ == "__main__":
    # Example usage
    video_overlay = VideoTextOverlay("final_videos", "captions", "output_videos")
    video_overlay.overlay_text_on_videos()
