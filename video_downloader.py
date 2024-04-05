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
        print("Initializing VideoDownloader...")
        """
        Initialize the VideoDownloader object.

        Args:
            api_key (str, optional): The API key for accessing the Pexels API. Defaults to None.
            per_page (int, optional): Number of videos to fetch per page from Pexels API. Defaults to 80.
            chunk_size (int, optional): Size of each chunk to download the video file. Defaults to 1024.
            num_videos_to_download (int, optional): Number of videos to download. Defaults to 10.
        """
        self.api_key = self.load_api_key()
        self.themes = ["drone beach", "sunsets", "drone adriatic", "drone nature", "drone forest", "drone waterfall"]
        self.min_resolution = (1080, 1920)  # Set a minimum resolution (e.g., 720p)

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
        
    def get_quality_from_link(self, link):
        """
        Extract the quality information from the link URL.

        Args:
            link (str): URL of the video file.

        Returns:
            str: Quality information extracted from the link.
        """
        # Split the link using '/' as a delimiter and select the second-to-last part containing the quality information
        parts = link.split('/')
        quality_info = parts[-2]
        return quality_info
    
    def get_video_resolution(self, video):
        
        """
        Extract resolution from video metadata.
        """
        if 'width' in video and 'height' in video:
            return (video['width'], video['height'])
        else:
            print("Video metadata:", video)  # Print video metadata for debugging
            return (0, 0)  # Unknown resolution
        
    def get_video_metadata(self, filepath):
        print("Getting video metadata...")
        """
        Extract metadata from a video file using ffprobe.

        Args:
            filepath (str): Path to the video file.

        Returns:
            str: Resolution of the video in the format "width x height".
        """
        try:
            probe = FFProbe(filepath)
            video_info = next(s for s in probe.streams if s.is_video())
            resolution = f"{video_info.width}x{video_info.height}"
            return resolution
        except Exception as e:
            print(f"Error extracting metadata from video: {e}")
            return "Unknown"
        
        
    def load_api_key(self):
        print("Loading API key...")
        """
        Load the API key from a JSON file.

        Args:
            api_key_file (str): Path to the JSON file containing the API key.
        """
        try:
            with open('pexels_api.json') as file:
                config = json.load(file)
                return config["pexels_api_key"]
        except (FileNotFoundError, KeyError) as e:
            print(f"Error loading API key: {e}")
            return None
    
    def search_videos(self, theme, num_videos):
        print("Searching videos...")
        """
        Search for videos based on a given theme with resolution filtering.

        Args:
            theme (str): The theme to search for.
            num_videos (int): The number of videos to search for.

        Returns:
            list: A list of dictionaries, each containing information about a video.
        """
        try:
            videos = []
            num_pages = -(-num_videos // PER_PAGE)  # Ceiling division to calculate total pages

            def fetch_page(page):
                """
                Fetch videos from a single page of Pexels API.

                Args:
                page (int): The page number to fetch.

                Returns:
                list: A list of dictionaries, each containing information about a video.
                """
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
                    filtered_videos.append(video)

            return filtered_videos[:num_videos]

        except requests.RequestException as e:
            print(f'Error searching for videos: {e}')
            return []


    def select_highest_quality_link(self, video):
        print("Selecting highest quality link...")
        """
        Select the highest-quality link for downloading from the list of video files,
        ensuring it meets the minimum resolution requirement.

        Args:
            video (dict): Dictionary containing information about the video.

        Returns:
            str: URL of the selected highest-quality video file, or None if not found.
        """
        # Filter video files to those containing 'hd' in the link
        hd_video_files = [vf for vf in video.get('video_files', []) if 'hd_1920_1080' in vf['link']]
        
        # If no 'hd' video files are found, return None
        if not hd_video_files:
            return None
        
        # Select the link with the highest resolution among 'hd' video files
        selected_link = max(hd_video_files, key=lambda x: self.get_quality_from_link(x['link']))['link']
        
        return selected_link

    def download_video(self, video, output_folder):
        """
        Download a video and print its resolution and selected link for downloading.
        """
        video_id = video['id']
        filename = f'{video_id}.mp4'
        filepath = os.path.join(output_folder, filename)

        try:
            # Print all available links for the video
            links = [vf['link'] for vf in video.get('video_files', [])]
            print(f"Available Links for Video ID {video_id}:")
            for link in links:
                print(link)

            # Select the highest-quality link for downloading
            selected_link = self.select_highest_quality_link(video)

            if selected_link is None:
                print("No suitable link found. Fetching another video...")
                return False  # Signal to fetch another video
            
            # Print video ID, resolution, and selected link
            print(f"Selected Link: {selected_link}")

            # Download the video using the selected link
            with requests.get(selected_link, stream=True) as response, open(filepath, 'wb') as f:
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                with tqdm(desc=f"{filename}", total=total_size, unit="B", unit_scale=True, unit_divisor=1024) as pbar:
                    for data in response.iter_content(chunk_size=CHUNK_SIZE):
                        f.write(data)
                        pbar.update(len(data))
            print(f"Downloaded: {filepath}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error downloading video: {e}")
        except IOError as e:
            print(f"Error writing video: {e}")
        return False

if __name__ == "__main__":
    print("Initializing VideoDownloader instance...")
    downloader = VideoDownloader()
    theme = random.choice(downloader.themes)
    num_videos = 1000
    
    # Ensure the 'footages' directory exists or create it if it doesn't
    output_folder = 'footages'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Directory '{output_folder}' created.")

    # Search for videos based on the theme with resolution filtering
    filtered_videos = downloader.search_videos(theme, num_videos)
    print(f"Downloading {NUM_VIDEOS_TO_DOWNLOAD} from {theme}")
    
    # Check if there are any filtered videos
    if filtered_videos:
        # Randomly select videos from the filtered list
        selected_videos = random.sample(filtered_videos, min(NUM_VIDEOS_TO_DOWNLOAD, len(filtered_videos)))
        
        # Print out all the links from the selected videos for downloading
        print("Links Containing HD Videos for Downloading:")
        for video in selected_videos:
            print(f"Video ID: {video['id']}")
            links = [vf['link'] for vf in video.get('video_files', []) if 'hd_1920_1080' in vf['link']]
            for link in links:
                print(link)

        # Start downloading the selected videos
        print("\nStarting Download...")
        downloaded_count = 0
        attempted_videos = set()  # To store IDs of attempted videos
        
        # If less than NUM_VIDEOS_TO_DOWNLOAD videos were downloaded, fetch more videos
        remaining_videos_needed = NUM_VIDEOS_TO_DOWNLOAD - downloaded_count
        while remaining_videos_needed > 0:
            print("Fetching additional videos to ensure enough links for download...")
            additional_videos = downloader.search_videos(theme, num_videos)
            if additional_videos:
                for video in additional_videos:
                    # Check if the video has already been attempted
                    if video['id'] in attempted_videos:
                        continue  # Skip this video if already attempted
                    for link in video.get('video_files', []):
                        if 'hd_1920_1080' in link['link']:
                            success = downloader.download_video(video, 'footages')
                            attempted_videos.add(video['id'])
                            if success:
                                downloaded_count += 1
                                remaining_videos_needed -= 1
                                print(f"Downloaded video count: {downloaded_count}/{NUM_VIDEOS_TO_DOWNLOAD}")
                                break
                    if remaining_videos_needed <= 0:
                        break  # Exit the loop if enough videos have been downloaded
                print(f"Total downloaded videos: {downloaded_count}")
                if remaining_videos_needed <= 0:
                    break  # Exit the loop if enough videos have been downloaded
            else:
                print("No more videos available.")
                break

        print(f"Total downloaded videos: {downloaded_count}")
    else:
        print("No videos found with resolutions higher than the minimum set resolution.")




