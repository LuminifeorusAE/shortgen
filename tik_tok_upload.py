import os
from tiktok_uploader.upload import upload_video

VIDEO_DIRECTORY = "final_videos"

if __name__ == "__main__":
    # Get a list of files in the directory
    files = os.listdir(VIDEO_DIRECTORY)

    # Filter out only the .mp4 files
    mp4_files = [file for file in files if file.endswith(".mp4")]

    if mp4_files:
        # Take the first .mp4 file found
        video_path = os.path.join(VIDEO_DIRECTORY, mp4_files[0])

        # Upload the video to TikTok
        upload_video(video_path,
                     description="This is a video from the local directory",
                     cookies="cookies.txt")
    else:
        print("No .mp4 files found in the directory.")
