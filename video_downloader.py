import os 
import random
import requests
import json
from tqdm import tqdm
import concurrent.futures
"""
Imports: The code imports necessary modules such as os,
• random,
• requests,
• json,
• concurrent.futures, and tqdm
to handle file operations, random selection, HTTP requests, JSON parsing, concurrent execution, and progress bar display, respectively.
"""

class VideoDownloader():

    """
• This class encapsulates the functionality related to downloading videos from Pexels.com.

• It has methods to load the API key from a JSON file, search for videos based on a given theme,
 fetch API responses, download videos, and manage the overall video downloading process."""

    def __init__(self):
        self.api_key = self.load_api_key()
        self.themes = ["beach", "city", "drone footages", "nature"]
    
    def load_api_key(self):
        """
        • Opens the JSON file containing the API key.
        • Loads the JSON data from the file.
        • Returns the API key from the loaded JSON data.
        • Handles the case where the JSON file is not found.
        • Handles the case where the key is not found in the JSON data.

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
    def search_videos (self, theme, num_videos):
        """
        • Defines a method for searching videos based on a given theme and the desired number of videos to retrieve.
        • Initializes an empty list to store the fetched videos.
        • Specifies the maximum number of videos per page allowed by the API.
        • Calculates the total number of pages needed to retrieve the desired number of videos using ceiling division.
        • Initializes a counter to keep track of the total number of videos found.
        """
        try:
            videos = []
            per_page = 80 # Maximum per_page allowed by the API
            num_pages = -(-num_videos//per_page) # Ceiling division to calculate total pages
            total_found = 0
            
            def fetch_page(page):
                """
                • Defines an inner function to fetch videos for a single page.
                • Constructs the URL for the API request using the provided theme, page number, and videos per page.
                • Sets the request headers with the API key.
                • Calls method to make the HTTP request and fetch the response.
                • Checks if the response is not None, then parses the JSON response and extracts the list of videos; otherwise, returns an empty list.
                """
                url = f'https://api.pexels.com/videos/search?query={theme}&per_page={per_page}&page={page}'
                headers = {"Authorization": self.api_key}
                response = self.get_api_response(url,headers)
                if response is not None:
                    return response.json().get('videos', [])
                return[]
            """
            • Uses ThreadPoolExecutor from the concurrent.futures module to fetch multiple pages concurrently.
            • Submits tasks (fetching pages) to the executor for each page.
            • Waits for the futures to complete using as_completed(), and extends the videos list with the results while updating the total number of videos found.
            """
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(fetch_page,page) for page in range(1, num_pages +1)]
                for future in concurrent.futures.as_completed(futures):
                    videos.extend(future.result())
                    total_found += len(future.result())
            print("Videos Found:", total_found)
            return videos[:num_videos]
            """
            • Handles any requests.RequestException that might occur during the video search process, such as network errors, and prints an error message.
            """        
        except requests.RequestException as e:
            print(f'Error searching for videos: {e}')
            return[]
        
    def get_api_response(self,url,headers):
        """
        • Tries to make an HTTP GET request to the specified URL with the provided headers.
        • Raises an exception (requests.HTTPError) if the response status code is not successful (not in the 200 range).
        • If an exception occurs during the request (e.g., network error), it catches the requests.RequestException and prints an error message.

        """
        try:
            responce = requests.get(url, headers=headers)
            responce.raise_for_status()
            return responce
        except requests.RequestException as e:
            return None
    def download_video(self,video,output_folder):
        """
        • Extracts the URL of the video file from the video object.
        • Retrieves the video ID and constructs the filename.
        • Constructs the full filepath by joining the output folder path and filename.

        """
        video_url = video['video_files'] [0]['link']
        video_id = video['id']
        filename = f'{video_id}.mp4'
        filepath = os.path.join(output_folder,filename)

        try:
            with requests.get(video_url,stream=True) as response, open(filepath, 'wb') as f:
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                with tqdm(desc = filename, total = total_size, unit = "B", unit_scale= True, unit_divisor= 1024,) as pbar:
                    for data in response.iter_content(chunk_size=1024):
                        f.write(data)
                        pbar.update(len(data))
            print(f"Downloaded: {filepath}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading video: {e}")
        except IOError as e:
            print(f"Error writing video: ")
            """
            • Attempts to download the video file from the specified URL in chunks using requests.get() with the stream=True parameter.
            • Opens a file in binary write mode to save the video content.
            • Raises an exception if there's an error during the download or writing process.
            • Uses tqdm to display a progress bar while downloading.
            • Updates the progress bar as data chunks are received and written to the file.
            • Prints a success message if the download completes without errors.
            
            """
    def download_videos(self, theme, num_videos=10, selected_videos=None):
        """
        • Defines a method to download a specified number of videos based on the selected theme.
        • Checks if any video selected, indicating that no videos were selected for download.
        • If there is no selected video, it prints an error message and returns early.
        • Checks if the output folder does not exist, and if so, creates it.
        • Iterates over each selected video
        • Calls the download_video() method to download each video, passing the video object and the output folder as arguments.
        """
        if selected_videos is None:
            print("Error: There is no selected video to download.")
            return
        print(f"Total videos found for theme '{theme}: {len(selected_videos)}'")

        output_folder = 'footages'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        for video in selected_videos:
            self.download_video(video, output_folder)
if __name__ == "__main__":
    """
    • Creates an instance of the VideoDownloader class named downloader.
    • Randomly selects a theme from the themes list using random.choice().
    • Sets the num_videos variable to 1000.
    • Calls the search_videos() method of the downloader object to search for videos based on the randomly selected theme and the specified number of videos.
    • Checks if the videos list is not empty (i.e., videos were found for the selected theme).
    • Selects a subset of videos from the videos list using random.sample(). It selects either 10 videos or all available videos (whichever is smaller).
    • Calls the download_videos() method of the downloader object to download the selected subset of videos, passing the theme, the number of videos to download (num_videos=10), and the selected videos as arguments.
    """
    downloader = VideoDownloader()
    theme = random.choice(downloader.themes)
    num_videos = 1000
    videos = downloader.search_videos(theme, num_videos)
    if videos:
        selected_videos = random.sample(videos, min(10, len(videos)))
        downloader.download_videos(theme, num_videos=10, selected_videos=selected_videos)
