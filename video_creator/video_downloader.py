#video_downloader.py

import requests
import random
import os
import json
import re
from tqdm import tqdm
from moviepy.editor import VideoFileClip  # Add this import statement

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

    def delete_downloaded_videos(self):
        folder_path = "footages"  # Adjust the folder path accordingly
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            os.remove(filepath)
        print("Downloaded videos deleted.")

    def main(self):
        if not self.api_key:
            print("Error: Unable to retrieve API key.")
            return

        while True:
            theme = random.choice(self.themes)
            print(f"Selected theme: {theme}")

            videos = self.search_videos(theme)
            if not videos:
                print("No videos found.")
                continue

            selected_videos = []
            for video in videos:
                self.download_video(video)
                selected_videos.append(video)

                # Check total duration after each download
                if 55 <= self.total_duration <= 59:
                    break
                elif self.total_duration > 60:
                    # Remove the last downloaded video if total duration exceeds 60 seconds
                    last_downloaded_video = selected_videos.pop()
                    self.delete_video(last_downloaded_video)
                    # Adjust total duration
                    self.total_duration -= last_downloaded_video['duration']

            # Check if total duration meets criteria
            if 55 <= self.total_duration <= 59:
                break
            else:
                print("Total duration does not meet criteria. Continuing to download.")

