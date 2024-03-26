import os 
import random
import requests
from tqdm import tqdm
from ffprobe import FFProbe  
import json
import concurrent.futures

PER_PAGE = 80
CHUNK_SIZE = 1024
NUM_VIDEOS_TO_DOWNLOAD = 10

class VideoDownloader():
    """
    This class encapsulates the functionality related to downloading videos from Pexels.com.
    """

    def __init__(self):
        self.api_key = self.load_api_key()
        self.themes = ["drone beach", "drone city", "drone nature", "drone beach"]
        self.min_resolution = (1280, 720)  # Set a minimum resolution (e.g., 720p)
    
    def load_api_key(self):
        """
        Load the API key from a JSON file.
        """
        try:
            with open('pexels_api.json') as file:
                config = json.load(file)
                return config["pexels_api_key"]
        except (FileNotFoundError, KeyError) as e:
            print(f"Error loading API key: {e}")
            return None
    
    def search_videos(self, theme, num_videos):
        try:
            videos = []
            num_pages = -(-num_videos // PER_PAGE)  # Ceiling division to calculate total pages

            def fetch_page(page):
                url = f'https://api.pexels.com/videos/search?query={theme}&per_page={PER_PAGE}&page={page}'
                headers = {"Authorization": self.api_key}
                response = self.get_api_response(url, headers)
                if response is not None:
                    return response.json().get('videos', [])
                return []

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(fetch_page, page) for page in range(1, num_pages + 1)]
                for future in concurrent.futures.as_completed(futures):
                    videos.extend(future.result())

            print("Videos Found:", len(videos))

            print("Filtered Videos:")
            filtered_videos = []
            for video in videos:
                resolution = self.get_video_resolution(video)
                if resolution[0] >= self.min_resolution[0] and resolution[1] >= self.min_resolution[1]:
                    print(f"Downloading video with resolution {resolution}.")
                    filtered_videos.append(video)
                else:
                    print(f"Skipping download of video with resolution {resolution} because it is low.")

            return filtered_videos[:num_videos]

        except requests.RequestException as e:
            print(f'Error searching for videos: {e}')
            return []


    def get_video_resolution(self, video):
        """
        Extract resolution from video metadata.
        """
        if 'width' in video and 'height' in video:
            return (video['width'], video['height'])
        else:
            print("Video metadata:", video)  # Print video metadata for debugging
            return (0, 0)  # Unknown resolution



    def get_api_response(self, url, headers):
        """
        Make an HTTP GET request to the specified URL with the provided headers.
        """
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f'Error making API request: {e}')
            return None

    
    def download_video(self, video, output_folder):
        """
        Download a video and print its resolution and selected link for downloading.
        """
        video_id = video['id']
        filename = f'{video_id}.mp4'
        filepath = os.path.join(output_folder, filename)

        try:
            # Select the highest-quality link for downloading
            selected_link = self.select_highest_quality_link(video)
            
            # Print video ID, resolution, and selected link
            print(f"Video ID: {video_id}, Resolution: {self.get_video_resolution(video)}, Selected Link: {selected_link}")

            # Download the video using the selected link
            with requests.get(selected_link, stream=True) as response, open(filepath, 'wb') as f:
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                with tqdm(desc=f"{filename}", total=total_size, unit="B", unit_scale=True, unit_divisor=1024) as pbar:
                    for data in response.iter_content(chunk_size=CHUNK_SIZE):
                        f.write(data)
                        pbar.update(len(data))
            print(f"Downloaded: {filepath}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading video: {e}")
        except IOError as e:
            print(f"Error writing video: {e}")

    def select_highest_quality_link(self, video):
        """
        Select the highest-quality link for downloading from the list of video files.
        """
        # Extract the quality information from each link and select the link with the highest quality
        video_files = video.get('video_files', [])
        selected_link = max(video_files, key=lambda x: self.get_quality_from_link(x['link']))['link']
        return selected_link

    def get_quality_from_link(self, link):
        """
        Extract the quality information from the link URL.
        """
        # Split the link using '/' as a delimiter and select the second-to-last part containing the quality information
        parts = link.split('/')
        quality_info = parts[-2]
        return quality_info




    def get_video_metadata(self, filepath):
            """
            Extract metadata from a video file using ffprobe.
            """
            try:
                probe = FFProbe(filepath)
                video_info = next(s for s in probe.streams if s.is_video())
                resolution = f"{video_info.width}x{video_info.height}"
                return resolution
            except Exception as e:
                print(f"Error extracting metadata from video: {e}")
                return "Unknown"

if __name__ == "__main__":

    downloader = VideoDownloader()
    theme = random.choice(downloader.themes)
    num_videos = 1000
    
    # Search for videos based on the theme with resolution filtering
    filtered_videos = downloader.search_videos(theme, num_videos)
    
    # Check if there are any filtered videos
    if filtered_videos:
        # Randomly select videos from the filtered list
        selected_videos = random.sample(filtered_videos, min(NUM_VIDEOS_TO_DOWNLOAD, len(filtered_videos)))
        
        # Print out the randomly selected videos and their resolutions
        print("Randomly Selected Videos for Downloading:")
        for video in selected_videos:
            resolution = downloader.get_video_resolution(video)
            print(f"Video ID: {video['id']}, Resolution: {resolution}")

        # Start downloading the selected videos
        print("\nStarting Download...")
        for video in selected_videos:
            downloader.download_video(video, 'footages')
    else:
        print("No videos found with resolutions higher than the minimum set resolution.")