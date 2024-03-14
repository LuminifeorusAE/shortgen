import os 
import random
import requests
import json
from tqdm import tqdm

class VideoDownloader:
    """
    A class for downloading videos from Pexels.com.
    """
    def __init__(self):
        self.api_key = self.load_api_key()
        self.themes = ["beach", "city", "drone footages", "nature"]
    """
    Initializes the VideoDownloader class.
    """
    def load_api_key(self):
        """
        Reads the Pexels API key from a JSON file.

        Returns:
            str: The Pexels API key.
        """
        try:
            with open('pexels_api_2.json') as file:
                config = json.load(file)
                return config["pexels_api_key_2"]
        except FileNotFoundError:
            print("Error: Your JSON file should be in the same directory.")
            return None
        except KeyError:
            print("If it's in the correct directory, please check if it's not empty or corrupted.")
            return None
    
    def search_videos(self, theme, num_videos):
        try:
            videos = []
            per_page = 80  # Maximum per_page allowed by the API
            num_pages = -(-num_videos // per_page)  # Ceiling division to calculate total pages
            for page in range(1, num_pages + 1):
                url = f'https://api.pexels.com/videos/search?query={theme}&per_page={per_page}&page={page}'
                headers = {'Authorization': self.api_key}
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                videos.extend(data.get('videos', []))
            
            print("Total Number of videos Found:", len(videos))
            print("Videos")
            for video in videos[:num_videos]:  # Output only the desired number of videos
                print("Video ID:", video.get('id'))
                print("Video URL:", video.get('url'))
                print("Video Duration:", video.get('duration'))
                print("Video Quality:", video.get('video_files')[0].get('quality'))
                print("Video Width:", video.get('video_files')[0].get('width'))
                print("Video Height:", video.get('video_files')[0].get('height'))
                print("-" * 50)

            print("Number of videos on the page:", len(videos))
            return videos[:num_videos]
        except requests.RequestException as e:
            print(f"Error searching for videos: {e}")
            return []
    def download_videos(self, theme, num_videos=10, selected_videos=None):
        if selected_videos is None:
            print("Error: No videos selected for download.")
            return
        
        print(f"Total videos found for theme '{theme}': {len(selected_videos)}")

        # Create 'footages' folder if it doesn't exist
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

if __name__ == "__main__":
    downloader = VideoDownloader()
    theme = random.choice(downloader.themes)
    num_videos = 1000
    videos = downloader.search_videos(theme, num_videos)
    if videos:
        selected_videos = random.sample(videos, min(10, len(videos)))
        downloader.download_videos(theme, num_videos=10, selected_videos=selected_videos)
