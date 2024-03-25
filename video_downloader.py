import os
import random
import requests
import json
from tqdm import tqdm
import concurrent.futures

class VideoDownloader():
    """
    Class to download videos from Pexels.com.
    """

    def __init__(self):
        self.api_key = self.load_api_key()
        self.themes = ["drone beach", "drone city", "drone nature", "sunsets"]

    def load_api_key(self):
        """
        Load API key from a JSON file.
        """
        try:
            with open('pexels_api.json') as file:
                config = json.load(file)
                return config["pexels_api_key"]
        except FileNotFoundError:
            print("Error: Your JSON file should be in the same directory.")
            return None
        except KeyError:
            print("API KEY ERROR: key is corrupted or does not exist")
            return None

    def search_videos(self, theme, num_videos):
        """
        Search for videos based on a given theme and number of videos.
        """
        try:
            videos = []
            per_page = 80  # Maximum per_page allowed by the API
            num_pages = -(-num_videos // per_page)  # Ceiling division to calculate total pages
            total_found = 0

            def fetch_page(page):
                """
                Fetch videos for a single page.
                """
                url = f'https://api.pexels.com/videos/search?query={theme}&per_page={per_page}&page={page}'
                headers = {"Authorization": self.api_key}
                response = self.get_api_response(url, headers)
                if response is not None:
                    return response.json().get('videos', [])
                return []

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(fetch_page, page) for page in range(1, num_pages + 1)]
                for future in concurrent.futures.as_completed(futures):
                    videos.extend(future.result())
                    total_found += len(future.result())

            print("Total videos found:", total_found)  # Print total number of videos found

            # Print resolution of each video
            for video in videos:
                if 'width' in video and 'height' in video:
                    resolution = f"{video['width']}x{video['height']}"
                    print(f"Video Resolution: {resolution}")

            return videos[:num_videos]
        except requests.RequestException as e:
            print(f'Error searching for videos: {e}')
            return []


    def get_api_response(self, url, headers):
        """
        Make an HTTP GET request to the specified URL.
        """
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            return None

    def download_video(self, video, output_folder):
        """
        Download a video.
        """
        video_url = video['video_files'][0]['link']
        video_id = video['id']
        filename = f'{video_id}.mp4'
        filepath = os.path.join(output_folder, filename)
         # Retrieve resolution information
        resolution = f"{video['width']}x{video['height']}"

        # Print resolution before starting the download
        print(f"Downloading video with resolution: {resolution}")
        try:
            with requests.get(video_url, stream=True) as response, open(filepath, 'wb') as f:
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                with tqdm(desc=filename, total=total_size, unit="B", unit_scale=True, unit_divisor=1024) as pbar:
                    for data in response.iter_content(chunk_size=1024):
                        f.write(data)
                        pbar.update(len(data))
            print(f"Downloaded: {filepath}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading video: {e}")
        except IOError as e:
            print(f"Error writing video: {e}")

    def download_videos(self, theme, num_videos=10, selected_videos=None, min_resolution='HD'):
        """
        Download high-definition or higher resolution videos based on the selected theme and metadata.
        """
        if selected_videos is None:
            print("Error: There are no selected videos to download.")
            return

        print(f"Total videos found for theme '{theme}': {len(selected_videos)}")

        output_folder = 'footages'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        downloaded_count = 0  # Counter to track the number of downloaded videos

        for video in selected_videos:
            # Check if video resolution meets the minimum requirement
            if self.is_resolution_sufficient(video, min_resolution):
                self.download_video(video, output_folder)
                downloaded_count += 1

                # Break the loop if the required number of videos is downloaded
                if downloaded_count >= num_videos:
                    break

    def is_resolution_sufficient(self, video, min_resolution):
        """
        Check if the resolution of the video is equal to or higher than the specified minimum resolution.
        """
        resolutions = {'HD': (1280, 720), 'Full HD': (1920, 1080), '4K': (3840, 2160)}  # Define resolutions

        if 'width' in video and 'height' in video:
            width, height = video['width'], video['height']
            min_width, min_height = resolutions.get(min_resolution, (0, 0))
            return width >= min_width and height >= min_height

        return False  # Return False if width or height metadata is missing


if __name__ == "__main__":
    downloader = VideoDownloader()
    theme = random.choice(downloader.themes)
    num_videos = 1000
    videos = downloader.search_videos(theme, num_videos)
    if videos:
        selected_videos = random.sample(videos, min(10, len(videos)))
        downloader.download_videos(theme, num_videos=10, selected_videos=selected_videos)
