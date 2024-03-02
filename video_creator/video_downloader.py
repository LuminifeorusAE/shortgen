import requests
import random
import os
import json
import re
from tqdm import tqdm

# Function to read API key from JSON file
def read_api_key():
    try:
        with open('pexels_api.json') as f:
            config = json.load(f)
            return config['pexels_api_key']
    except FileNotFoundError:
        print("Error: config.json file not found.")
        return None
    except KeyError:
        print("Error: 'api_key' not found in config.json.")
        return None

# List of themes
themes = ["beach", "city", "drone footages", "nature", "wild life"]

# Function to search for videos based on a theme
def search_videos(theme, api_key):
    try:
        url = f'https://api.pexels.com/videos/search?query={theme}&per_page=50'
        headers = {'Authorization': api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        videos = data.get('videos', [])
        return videos
    except requests.RequestException as e:
        print(f"Error searching for videos: {e}")
        return []

# Function to sanitize filename
def sanitize_filename(filename):
    # Remove invalid characters from filename
    return re.sub(r'[\\/*?:"<>|]', '', filename)

# Function to randomly select 2-3 videos from a list of videos
def select_random_videos(videos):
    num_videos = min(len(videos), random.randint(2, 3))
    return random.sample(videos, num_videos)

# Function to download a video
def download_video(video):
    video_files = video.get('video_files', [])
    if not video_files:
        print("No video files found for the selected video.")
        return
    
    # Select the first video file
    video_file = video_files[0]
    url = video_file['link']
    
    # Generate a filename with the .mp4 extension
    filename = f"{video['id']}.mp4"
    filename = sanitize_filename(filename)  # Sanitize filename

    # Create 'footages' folder if it doesn't exist
    if not os.path.exists('footages'):
        os.makedirs('footages')

    # Download the video to the 'footages' folder
    filepath = os.path.join('footages', filename)
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # Raise an exception for HTTP errors
            total_size = int(response.headers.get('content-length', 0))
            with open(filepath, 'wb') as f, tqdm(
                desc=filename,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as pbar:
                for data in response.iter_content(chunk_size=1024):
                    f.write(data)
                    pbar.update(len(data))
        print(f"Downloaded: {filepath}")
    except (requests.RequestException, IOError) as e:
        print(f"Error downloading video: {e}")

# Main function
def main():
    # Read API key from JSON file
    api_key = read_api_key()
    if not api_key:
        print("Error: Unable to retrieve API key.")
        return

    # Randomly select a theme
    theme = random.choice(themes)
    print(f"Selected theme: {theme}")

    # Search for videos based on the theme
    videos = search_videos(theme, api_key)
    if not videos:
        print("No videos found.")
        return

    # Randomly select 2-3 videos from the search results
    selected_videos = select_random_videos(videos)

    # Download the selected videos
    for video in selected_videos:
        download_video(video)

if __name__ == "__main__":
    main()
