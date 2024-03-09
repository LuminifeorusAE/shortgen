import requests
import random
import os
import json
import re
from tqdm import tqdm
from moviepy.editor import VideoFileClip


class PexelsVideoDownloader:
    def __init__(self):
        self.api_key = self.read_api_key()
        self.themes = ["beach", "city", "drone footages", "nature", "wild life"]
        self.total_duration = 0

    def read_api_key(self):
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

    def search_videos(self, theme):
        try:
            url = f'https://api.pexels.com/videos/search?query={theme}&per_page=50'
            headers = {'Authorization': self.api_key}
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            videos = data.get('videos', [])
            return videos
        except requests.RequestException as e:
            print(f"Error searching for videos: {e}")
            return []

    def sanitize_filename(self, filename):
        return re.sub(r'[\\/*?:"<>|]', '', filename)

    def download_video(self, video):
        video_files = video.get('video_files', [])
        if not video_files:
            print("No video files found for the selected video.")
            return
        
        video_file = video_files[0]
        url = video_file['link']
        filename = f"{video['id']}.mp4"
        filename = self.sanitize_filename(filename)

        if not os.path.exists('footages'):
            os.makedirs('footages')

        filepath = os.path.join('footages', filename)
        try:
            with requests.get(url, stream=True) as response:
                response.raise_for_status()  
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

            # Get the duration of the downloaded video
            clip = VideoFileClip(filepath)
            duration = clip.duration
            clip.close()

            # Update total duration
            self.total_duration += duration

        except (requests.RequestException, IOError) as e:
            print(f"Error downloading video: {e}")

    def delete_downloaded_video(self, video):
        filename = f"{video['id']}.mp4"
        filepath = os.path.join('footages', filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Deleted: {filepath}")

    
    def main(self):
        if not self.api_key:
            print("Error: Unable to retrieve API key.") 
            return

        # Choose a random theme from the provided themes
        theme = random.choice(self.themes)
        print(f"Selected theme: {theme}")

        # Search for videos based on the chosen theme
        videos = self.search_videos(theme)
        if not videos:
            print("No videos found.")
            return

        print(f"Total videos found: {len(videos)}")

        # Sort videos by duration in ascending order
        videos.sort(key=lambda x: x.get('duration', 0))

        selected_videos = []
        total_duration = 0  # Initialize total duration for the current selection

        while True:
            # Select one short, one medium, and one long video
            short_videos = [video for video in videos if 0 < video.get('duration', 0) <= 15]
            medium_videos = [video for video in videos if 15 < video.get('duration', 0) <= 30]
            long_videos = [video for video in videos if video.get('duration', 0) > 30]

            print("Short videos:", len(short_videos), "Medium videos:", len(medium_videos), "Long videos:", len(long_videos))

            # Calculate total duration
            total_duration = sum(video.get('duration', 0) for video in selected_videos)
            print(f"Total duration after selection: {total_duration}")

            # Randomly select one video from each category
            if short_videos and medium_videos and long_videos:
                selected_videos = [
                    random.choice(short_videos),
                    random.choice(medium_videos),
                    random.choice(long_videos)
                ]

                # Calculate total duration
                total_duration = sum(video.get('duration', 0) for video in selected_videos)
                print(f"Total duration after selection: {total_duration}")

                if 50 <= total_duration <= 60:
                    print(f"Total duration of selected videos meets the criteria: {total_duration} seconds")

                    # Download the selected videos
                    for video in selected_videos:
                        self.download_video(video)

                    print("Videos downloaded successfully.")
                    break
                else:
                    print(f"Insufficient videos or total duration does not meet criteria.")
                    print(f"Total duration: {total_duration}")  