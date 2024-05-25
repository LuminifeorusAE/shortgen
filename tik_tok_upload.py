import os
from tiktok_uploader.upload import upload_video
# from selenium.webdriver.chrome.options import Options

#line where you retrieve the cookies file path
cookies_file = os.getenv('COOKIES_FILE')

class TikTokUploader:
    def __init__(self, video_directory, captions_directory, cookies_file):
        self.video_directory = video_directory
        self.captions_directory = captions_directory
        self.cookies_file = cookies_file
        self.caption_files = []
        self.current_caption_index = 0

        # Populate list of caption files
        self._populate_caption_files()

    def _populate_caption_files(self):
        # Get a list of caption files in the captions directory
        caption_files = os.listdir(self.captions_directory)

        # Filter out only the text files
        self.caption_files = [file for file in caption_files if file.endswith(".txt")]

    def _get_next_caption(self):
        if self.caption_files:
            # Check if the file containing the last chosen index exists
            last_chosen_index_file = "last_chosen_index.txt"
            if os.path.exists(last_chosen_index_file):
                # Read the last chosen index from the file
                with open(last_chosen_index_file, "r") as index_file:
                    last_chosen_index = int(index_file.read())
                # Calculate the next index
                next_index = (last_chosen_index + 1) % len(self.caption_files)
            else:
                # If the file doesn't exist, start from the first caption
                next_index = 0

            # Get the next caption file based on the calculated index
            caption_file = self.caption_files[next_index]
            caption_path = os.path.join(self.captions_directory, caption_file)

            # Read the content of the caption file
            with open(caption_path, "r", encoding="utf-8") as file:
                caption = file.read()

            # Save the index of the chosen caption file for the next run
            with open(last_chosen_index_file, "w") as index_file:
                index_file.write(str(next_index))

            return caption.strip()
        else:
            return "No caption available."



    def _upload_video_in_directory(self):
        # Get a list of files in the video directory
        files = os.listdir(self.video_directory)

        # Filter out only the .mp4 files
        mp4_files = [file for file in files if file.endswith(".mp4")]

        if mp4_files:
            # Take the first .mp4 file found
            video_path = os.path.join(self.video_directory, mp4_files[0])

            # Get the next caption
            caption = self._get_next_caption()
            # options = Options()
            # #Start Uploading with full screen
            # options.add_argument('start-maximized')
            # Upload the video to TikTok with the caption
            upload_video(video_path,
                         description=caption,
                         cookies=self.cookies_file,
                         copyright = True
                        #  options=options,
                        #  headless=True
            )
        else:
            print("No .mp4 files found in the directory.")

if __name__ == "__main__":
    uploader = TikTokUploader(video_directory="output_videos", captions_directory="tags" ,cookies_file=cookies_file)
    uploader._upload_video_in_directory()