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

    def download_video_segment(self, video, duration):
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

            # Clip the downloaded video to the specified duration
            clip = VideoFileClip(filepath)
            clip = clip.subclip(0, duration)
            clip.write_videofile(filepath, codec="libx264", audio_codec="aac")
            clip.close()

        except (requests.RequestException, IOError) as e:
            print(f"Error downloading video: {e}")

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

        # Initialize variables for total duration and selected videos
        total_duration = 0
        selected_videos = []

        # Shuffle the list of videos to ensure randomness
        random.shuffle(videos)

        # Iterate over all videos and select segments until total duration meets criteria
        for video in videos:
            duration = video.get('duration', 0)
            # Calculate remaining duration needed to reach target duration
            remaining_duration = 55 - total_duration if total_duration < 55 else 60 - total_duration
            # Cut the video into segments and add to selected videos
            segment_duration = min(remaining_duration, random.randint(5, 6))
            if total_duration + segment_duration > 60:
                break  # Stop if adding the segment exceeds the total duration limit
            selected_videos.append((video, segment_duration))
            total_duration += segment_duration
            if total_duration >= 55 and total_duration <= 60:
                break  # Stop if total duration meets the criteria

        print(f"Total duration of selected videos: {total_duration} seconds")

        # Download the selected videos
        for video, duration in selected_videos:
            self.download_video_segment(video, duration)

        print("Videos downloaded successfully.")

