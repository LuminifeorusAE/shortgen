import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from pprint import pprint
import os

# Configuration Constants
CLIENT_SECRETS_FILE = "client_secret_1.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Rate Limit Constants
REQUESTS_PER_SECOND = 1  # Adjust as needed
MIN_REQUEST_INTERVAL = 1.0 / REQUESTS_PER_SECOND

def authenticate_and_get_youtube_service():
    """
    Authenticates the application and returns the YouTube service instance.
    """
    try:
        # Set up the OAuth flow using client secrets file and specified scopes.
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        
        # Run a local server to handle authentication and retrieve credentials.
        credentials = flow.run_local_server(port=0)
        
        # Build and return the YouTube service instance.
        return build('youtube', 'v3', credentials=credentials)
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None

def generate_title_and_description(video_file):
    """
    Generates a standardized title and description based on the video file name.
    """
    # Remove underscores and capitalize words
    video_name = os.path.splitext(video_file)[0].replace("_", " ").title()

    # Extract the theme from the filename
    # Assuming the theme is the words right before "task" in the title
    title_words = video_name.split()
    index_of_task = title_words.index("Task") if "Task" in title_words else -1

    if index_of_task > 1:
        # Extract the words before "task" to form the theme
        theme = " ".join(title_words[index_of_task - 2:index_of_task])
    else:
        # If "task" is not found or doesn't have enough preceding words, use a placeholder
        theme = "the topic"

    # Generate a more descriptive title based on the theme
    title = f"Coding Tutorials. {theme}"

    # Provide a more descriptive explanation in the description
    description = (
        f"This video demonstrates the tutorial of the {theme.lower()}. "
        f"We provide insights and examples to help you understand the process better. "
        "Feel free to contact us at dtadevosyan@gmail.com for any inquiries or further information."
    )

    return title, description


def upload_videos_with_task(youtube_service):
    try:
        # Get all files in the current directory
        current_directory = os.getcwd()
        files_in_directory = os.listdir(current_directory)

        # Filter files containing the word "task" in their name
        task_files = [file for file in files_in_directory if "task" in file.lower()]

        for task_file in task_files:
            title, description = generate_title_and_description(task_file)

            # Rate Limiting: Wait before making the next API request
            time.sleep(MIN_REQUEST_INTERVAL)

            video_upload_request = youtube_service.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": title,
                        "description": description,
                        "tags": ["education", "tutorial"],
                        "categoryId": "22"
                    },
                    "status": {
                        "privacyStatus": "private"
                    }
                },
                media_body=MediaFileUpload(task_file)
            )
            
            response = video_upload_request.execute()

            print(f"\nVideo Upload Successful for file: {task_file}")
            print("-" * 30)
            
            # Pretty print the response dictionary for better readability.
            pprint(response)

    except Exception as e:
        print(f"\nError during video upload: {e}")

if __name__ == '__main__':
    youtube_service = authenticate_and_get_youtube_service()

    if youtube_service:
        upload_videos_with_task(youtube_service)

