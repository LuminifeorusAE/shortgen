import requests
import random
import os
import json
from tqdm import tqdm

class PexelsVideoDownloader:
    def __init__(self):
        self.api_key = self.read_api_key()
        self.themes = ["beach", "city", "drone footages", "nature"]

    def read_api_key(self):
        try:
            with open('pexels_api.json') as f:
                config = json.load(f)
                return config['pexels_api_key']
        except FileNotFoundError:
            print("Error: pexels_api.json file not found.")
            return None
        except KeyError:
            print("Error: 'pexels_api_key' not found in pexels_api.json.")
            return None

    def search_videos(self, theme):
        try:
            url = f'https://api.pexels.com/videos/search?query={theme}&per_page=50'
            headers = {'Authorization': self.api_key}
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            return data.get('videos', [])
        except requests.RequestException as e:
            print(f"Error searching for videos: {e}")
            return []

    def download_videos(self, theme, num_videos=10):
        videos = self.search_videos(theme)
        if not videos:
            print(f"No videos found for theme '{theme}'.")
            return

        print(f"Total videos found for theme '{theme}': {len(videos)}")

        # Shuffle the list of videos to ensure randomness
        random.shuffle(videos)

        # Select random videos up to the specified number
        selected_videos = random.sample(videos, min(num_videos, len(videos)))

        if not os.path.exists('footages'):
            os.makedirs('footages')

        for video in selected_videos:
            video_url = video['video_files'][0]['link']
            video_id = video['id']
            filename = f"{video_id}.mp4"
            filepath = os.path.join('footages', filename)

            try:
                with requests.get(video_url, stream=True) as response, open(filepath, 'wb') as f:
                    response.raise_for_status()  
                    total_size = int(response.headers.get('content-length', 0))
                    with tqdm(
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

    def main(self):
        if not self.api_key:
            print("Error: Unable to retrieve API key.") 
            return

        # Choose a random theme from the provided themes
        theme = random.choice(self.themes)
        print(f"Selected theme: {theme}")

        # Download 10 random videos for the selected theme
        self.download_videos(theme, num_videos=10)

        print("Videos downloaded successfully.")
