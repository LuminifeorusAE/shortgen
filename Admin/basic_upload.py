import os
from tiktok_uploader.upload import upload_video
from OAuth_autorization import generate_title_and_description

def tik_tok_upload():
    # Get the current working directory
    current_directory = os.getcwd()

    # List all files in the current directory
    files = os.listdir(current_directory)

    # Filter out only the .mp4 files
    video_files = [file for file in files if file.endswith('.mp4')]

    if not video_files:
        print("No .mp4 files found in the current directory.")
        return

    # Iterate over each video file and upload
    for video_file in video_files:
        # Generate title and description dynamically for each video file
        title, description = generate_title_and_description(video_file)

        # Print out the generated title for each video
        print(f"Generated Title for '{video_file}':")

        # Upload the video with the dynamically generated title and description
        upload_video(os.path.join(current_directory, video_file),
                     description=description,
                     cookies='cookies.txt')

# Call the function
tik_tok_upload()
