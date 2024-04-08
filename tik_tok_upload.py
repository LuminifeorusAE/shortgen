import os
from tiktok_uploader.upload import upload_video

VIDEO_DIRECTORY = "final_videos"

def upload_video_from_directory():
    try:
        # Get a list of files in the directory
        files = os.listdir(VIDEO_DIRECTORY)
        print("Files in the directory:", files)

        # Filter out only the .mp4 files
        mp4_files = [file for file in files if file.endswith(".mp4")]
        print("MP4 files found:", mp4_files)

        if mp4_files:
            # Take the first .mp4 file found
            video_path = os.path.join(VIDEO_DIRECTORY, mp4_files[0])
            print("Selected video:", video_path)

            # Upload the video to TikTok
            print("Uploading video...")
            upload_video(video_path,
                         description="This is a video from the local directory",
                         cookies="cookies.txt", headless=True)
            print("Upload completed.")
        else:
            print("No .mp4 files found in the directory.")
    except Exception as e:
        print("An error occurred during video upload:", str(e))

if __name__ == "__main__":
    upload_video_from_directory()
