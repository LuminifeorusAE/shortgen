import os
import random
import requests
import json
from tqdm import tqdm
from urllib.parse import urlparse, parse_qs
class VideoDownloader:
    """
    A class for downloading videos from Pexels.com.
    """

    def __init__(self):
        """
        Initializes the VideoDownloader class.
        """
        self.api_key = self.api_keys()
        self.themes = ["beach", "city", "drone footages", "nature"]

    def api_keys(self):
        """
        Reads the Pexels API key from a JSON file.

        Returns:
            str: The Pexels API key.
        """
        try:
            with open('pexels_api_2.json') as file:
                config = json.load(file)
                return config["pexels_api_key"]
        except FileNotFoundError:
            print("Error: The pexels_api.json file was not found.")
            return None
        except KeyError:
            print("Error: The 'pexels_api_key' was not found in the pexels_api.json file.")
            return None

    def search_videos(self, theme, total_videos=1000):
        """
        Searches for videos on Pexels based on the specified theme.

        Args:
            theme (str): The theme to search for.
            total_videos (int): Total number of videos to retrieve (default is 1000).

        Returns:
            list: A list of video data returned by the API.
        """
        try:
            videos = []
            page = 1
            while len(videos) < total_videos:
                url = f'https://api.pexels.com/videos/search?query={theme}&per_page=80&page={page}'
                headers = {'Authorization': self.api_key}
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                page_videos = data.get('videos', [])
                if not page_videos:
                    break
                videos.extend(page_videos)
                page += 1
                next_page = data.get('next_page')
                if not next_page:
                    break
                page_url = urlparse(next_page)
                page_query = parse_qs(page_url.query) 
                page = int(page_query['page'][0])
            print("Total videos found:", len(videos))
            return videos[:total_videos]
        except requests.RequestException as e:
            print(f"Error searching for videos: {e}")
            return []


    def download_videos(self, theme, num_videos=10):
        """
        Downloads videos from Pexels based on the specified theme.

        Args:
            theme (str): The theme to download videos for.
            num_videos (int): The number of videos to download (default is 10).

        Returns:
            None
        """
        videos = self.search_videos(theme, total_videos=num_videos)
        if not videos:
            print(f"No videos found for the theme '{theme}'.")
            return
        random.shuffle(videos)
        selected_videos = random.sample(videos, min(num_videos, len(videos)))

        if not os.path.exists('footages'):
            os.makedirs('footages')

        for video in selected_videos:
            video_url = video['video_files'][0]['link']
            video_id = video['id']
            filename = f"{video_id}.mp4"
            filepath = os.path.join('footages', filename)

            try:
                with requests.get(video_url, stream=True) as response, open(filepath, "wb") as file:
                    response.raise_for_status()
                    total_size = int(response.headers.get('content-length', 0))
                    with tqdm(desc=filename, total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                        for data in response.iter_content(chunk_size=1024):
                            file.write(data)
                            pbar.update(len(data))
            except (requests.RequestException, IOError) as e:
                print(f"Error Downloading video {filename}: {e}")

    def main(self):
        """
        Main entry point of the script.
        """
        if not self.api_key:
            print("Unable to connect to the API. Check your internet connection or API key.")
            return

        theme = random.choice(self.themes)
        print(f"Selected theme: {theme}")

        self.download_videos(theme, num_videos=10)
        print("Videos downloaded successfully.")

# Create an instance of the VideoDownloader class and run the main function
downloader = VideoDownloader()
downloader.main()
