import os
from tiktok_uploader.upload import upload_video

class TikTokUploader:
    def __init__(self, video_directory, cookies_file="cookies.txt"):
        self.video_directory = video_directory
        self.cookies_file = cookies_file

    def upload_first_video(self):
        # Get a list of files in the directory
        files = os.listdir(self.video_directory)

        # Filter out only the .mp4 files
        mp4_files = [file for file in files if file.endswith(".mp4")]

        if mp4_files:
            # Take the first .mp4 file found
            video_path = os.path.join(self.video_directory, mp4_files[0])

            # Upload the video to TikTok
            upload_video(video_path,
                         description="This is a video from the local directory",
                         cookies=self.cookies_file)
        else:
            print("No .mp4 files found in the directory.")

if __name__ == "__main__":
    uploader = TikTokUploader(video_directory="final_videos")
    uploader.upload_first_video()
