import concurrent.futures # using to make multiple api calls reach more than default 80 videos

import os # creates folder for downloading videos in it
import random # to select random videos from website
import requests # using to get api responce for downloading videos
from tqdm import tqdm # visualises downloading process
from moviepy.editor import * # gets video metadata for selecting a link for video resolution

PER_PAGE = 80 # default quantity of videos per request
CHUNK_SIZE = 1024 # Modify if how got a better hardware 
NUM_VIDEOS_TO_DOWNLOAD = 10 # Modify if you need more videos to download

class VideoDownloader():
    """
    This class encapsulates the functionality related to downloading videos from Pexels.com.
    """

    # This is the constructor method for the VideoDownloader class
    def __init__(self):
        print("Initializing Video Downloader...")

        # Initialize the api_key by accessing it from the environment variables
        self.api_key = os.getenv('PEXELS_API_KEY')
        if not self.api_key:
            raise EnvironmentError("PEXELS_API_KEY environment variable is not set. Please refer to the readme file on how to obtain and set up your API key.")


        # defines a list of themes to search for videos.
        self.themes = ["drone beach waves", "horizon", "drone adriatic sea", "beautiful nature drone", "drone forest", "night sky"]
         # sets a minimum resolution for the videos.
        self.min_resolution = (2560, 1440)

    


    #This method get_api_response takes a URL and headers as input and makes an HTTP GET request to the specified URL with the provided headers.
    def get_api_response(self,url,headers):
        print("Requesting API response...")
        """
        Make an HTTP GET request to the specified URL with the provided headers.
        """
        # attempts to make the GET request using the requests.get() function
        try:
            response = requests.get(url, headers=headers)
            # checks if the response status code is not in the 2xx range, indicating an error, using response.raise_for_status()
            response.raise_for_status()
            # returns the response object if the request is successful
            print("Successful API Request...")
            return response
            
        # If there's any exception raised during the request (e.g., network error), it catches it with except block and prints an error message.
        except requests.RequestException as e:
            print(f"Error making API request: {e}")
        # If the request is not successful, it returns None.
        return None
            
        
    def get_quality_from_link(self,link):
        """
        Extract the quality information from the link URL.

        Args:
            link (str): URL of the video file.

        Returns:
            str: Quality information extracted from the link.
        """
        # Spliting link in two parts
        parts = link.split('/')
        #choosing second part
        quality_info = parts[-2]
        #returning second part
        return quality_info
    
    def get_video_info(self, video, mode="resolution"):
        """
        Get video resolution or select the highest quality link based on the mode.

        Args:
            video (dict): Dictionary containing information about the video.
            mode (str): Mode to determine the action. Can be 'resolution' or 'link'.
        
        Returns:
            str: Resolution of the video in the format "width x height" if mode is 'resolution'.
            str: URL of the selected highest-quality video file if mode is 'link'.
            None: If mode is invalid or no suitable link found.
        """
        # takes a video dictionary and a mode parameter (defaulting to 'resolution') as input.
        if mode == "resolution":
            # checks if the video dictionary contains 'width' and 'height' keys, indicating that the resolution information is available.
            if "width" in video and "height" in video:
                # If the resolution information is available, it constructs and returns a string representing the resolution in the format "width x height".
                return f"{video['width']}x{video['height']}"
            else:
                print("Video metadata:", video['height'])
                # If the resolution information is not available, it prints the video metadata for debugging purposes and returns "Unknown"
                return "Unknown"
            # If mode is 'link', it searches for HD video files in the page.
        elif mode == "link":
            # searches for video files in the video dictionary with links containing the string 'hd_2560_1440'
            hd_video_files = [vf for vf in video.get('video_files', [])if 'hd_2560_1440' in vf['link']]
            print (f"Found videos with {mode}")
            # If there are no HD video files, it returns None.
            if not hd_video_files:
                return None
            # If HD video files are found, it selects the link with the highest quality based on the quality information extracted from the link using the get_quality_from_link() method.    
            selected_link = max(hd_video_files, key=lambda x: self.get_quality_from_link(x['link']))['link']
            return selected_link
        else:
            print('invalid mode specified')
            # returns the resolution or URL accordingly, or None if the mode is invalid or no suitable link is found.
        return None
    
    def get_video_metadata(self, filepath):
        """
        Extract metadata from a video file using moviepy.

        Args:
            filepath (str): Path to the video file.

        Returns:
            tuple: A tuple containing duration (in seconds) and resolution (e.g., "width x height").
        """
        # takes a filepath as input.
        try:
            # loads the video file using VideoFileClip from moviepy.
            clip = VideoFileClip(filepath)
            # It extracts the duration and resolution of the video clip.
            duration = clip.duration
            resolution = f"{clip.size[0]}x{clip.size[1]}"

            # It returns a tuple containing duration (in seconds) and resolution.
            return duration, resolution
        except Exception as e:
            print(f"Error extracting metadata from video: {e}")
            return None, None
    
    def search_videos(self,theme,num_videos):
        print("Searching Videos...")

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
            #Ceiling division to calculate total pages
            num_pages = -(-num_videos//PER_PAGE) 

        # This is an inner function fetch_page() definition that fetches videos from a single page of the Pexels API.
            def fetch_page(page):
                """
                Fetch videos from a single page of Pexels API.

                Args:
                    page (int): The page number to fetch.

                Returns:
                    list: A list of dictionaries, each containing information about a video.
                """
                # constructs the URL for fetching videos from the Pexels API based on the provided theme, PER_PAGE, and page.
                url = f'https://api.pexels.com/videos/search?query={theme}&per_page={PER_PAGE}&page={page}'
                # constructs the HTTP headers with the API key.
                headers = {"Authorization": self.api_key}
                # makes an API request to the constructed URL using the get_api_response() method and stores the response.
                responce = self.get_api_response(url,headers)
                # checks if the response is not None, indicating a successful API request.
                if responce is not None:
                    #It returns the list of videos if available, otherwise an empty list.
                    return responce.json().get("videos", [])
            # uses concurrent execution with a ThreadPoolExecutor to fetch videos from multiple pages asynchronously.
            with concurrent.futures.ThreadPoolExecutor() as executor:
                #submits tasks to fetch pages using fetch_page() for each page number in the range of 1 to num_pages.
                futures = [executor.submit(fetch_page, page) for page in range(1, num_pages+1)]
                # It iterates through the completed futures
                for future in concurrent.futures.as_completed(futures):
                    # extends the videos list with the results.
                    videos.extend(future.result())
            
            #  prints the total number of videos found and creates a list filtered_videos to store filtered videos.
            print("Videos Found:", len(videos))

            print("Filtered Videos:")

            filtered_videos = []
            #  iterates through each video fetched and checks its resolution using the get_video_info() method
            for video in videos:
                resolution = self.get_video_info(video, mode="resolution")
                # If the resolution is not "Unknown", it appends the video to the filtered_videos list.
                if resolution != "Unknown":
                    filtered_videos.append(video)
            #we return a slice of the filtered_videos list containing the first num_videos items.
            #this ensures that we only return the desired number of videos that passed our filtering criteria.
            return filtered_videos[:num_videos]
        except requests.RequestException as e:
            print(f'Error searching videos: {e}')                
            return []

    def download_video(self, video, output_folder):
        """Selects link for downloading by given resolution and downloads it """
        
                # extracts the video ID from the video dictionary.
        video_id = video['id']
        # constructs a filename by appending the video ID with the '.mp4' extension.
        filename = f'{video_id}.mp4'
        # creates the full filepath by joining the output_folder path with the filename.
        filepath = os.path.join(output_folder, filename)

        try:
            # Print all available links for video
            links = [vf['link'] for vf in video.get('video_files', [])]
            # creates the full filepath by joining the output_folder path with the filename.
            print(f'Available links for Video ID {video_id}')
            for link in links:
                print(link)
            # Selecting quality of from the link to download
            selected_link = self.get_video_info(video, mode="link")

            # checks if a suitable download link is found
            if selected_link is None:
                # If selected_link is None, it prints a message indicating that no suitable link is found and returns False.
                print("No suitable link found. Fetching another link...")
                # signal to fetch another link
                return False
            # Print video ID, resolution, and selected link
            print(f"Selected Link: {selected_link}")
            # download videos using a selected link
            with requests.get(selected_link, stream=True) as response, open(filepath, 'wb') as f:
                # opens a file for writing in binary mode and streams the video content in chunks.
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                # tracks the progress of the download using tqdm, which provides a progress bar.
                with tqdm(
                        desc=f"{filename}",
                        total=total_size,
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024) as pbar:

                    # iterates over each downloading file data and shows downloading progress bar for every video
                    for data in response.iter_content(chunk_size=CHUNK_SIZE):
                        # writes downloaded data in chunks
                        f.write(data)
                        # updates uploading bar when data is downloaded
                        pbar.update(len(data))
            # prints a message indicating that the video is downloaded successfully and returns True.
            print(f"Downloaded {filepath}")
            return True

        # catches exceptions that might occur during the download process, such as network errors or file writing errors.
        except requests.exceptions.RequestException as e:
            print(f'Error downloading video: {e}')
        except IOError as e:
            print(f"Error writing video: {e}")
        return False


    
# Check if this script is being run as the main program
if __name__ == "__main__":
    
    # Print a message indicating the initialization of the Video Downloader instance
    print("initializing Video Downloader instance...")

    # Creating an instance of the VideoDownloader class
    downloader=VideoDownloader()

    # Selecting a random theme from the list of themes
    theme = random.choice(downloader.themes)

    num_videos = 1000
    # creating directory for downloading videos 
    output_folder  = 'footages'
    # Checking if the output folder already exists, if not, creating it
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
        print("Links containing HD videos for downloading")
        # iterates over each selected video, prints its ID
        for video in selected_videos:
            print(f"Video ID: {video['id']}")
            #prints the download links of the HD videos contained in that video
            links = [vf['link'] for vf in video.get('video_files', [])
                                if "hd_2560_1440" in vf['link']]
            for link in links:
                print(link)
    # Start downloading the selected videos
    print("\nStarting Download...")
    # keeps track of the number of videos successfully downloaded
    downloaded_count = 0
    #to store IDs of attempted videos
    attempted_videos = set() 

    # if letss than 10 videos were downloaded, fetch more videos
    remaining_videos_needed = NUM_VIDEOS_TO_DOWNLOAD - downloaded_count
    # starts a loop that continues until the number of remaining videos needed is zero.
    while remaining_videos_needed > 0:
        print("Fething additional videos to ensure enough link for download...")
        # calls the search_videos() method to fetch additional videos based on the selected theme.
        additional_videos = downloader.search_videos(theme,num_videos)
        if additional_videos:
            #checks if additional videos were found.
            for video in additional_videos:
                #check if the video has already ben attempted
                if video['id'] in attempted_videos:
                    continue #Skip the video if already attempted
                                # Iterate over each link in the video's video_files list
                for link in video.get('video_files', []):
                    # Check if the link contains 'hd_2560_1440'
                    if "hd_2560_1440" in link['link']:
                        # Attempt to download the video using the selected link
                        success = downloader.download_video(video, 'footages')
                        # Add the video ID to the set of attempted videos
                        attempted_videos.add(video['id'])
                        # If the download is successful, update counters and print status
                        if success:
                            downloaded_count += 1
                            remaining_videos_needed -= 1
                            print(f"Downloaded videos count: {downloaded_count}/{NUM_VIDEOS_TO_DOWNLOAD}")
                            # Break out of the loop if the target number of videos is reached
                            break
                # Check if the target number of videos has been reached
                if remaining_videos_needed <= 0:
                    # Break out of the loop if the target number of videos is reached
                    break
            print(f"Total downloaded videos: {downloaded_count}")
        else:
            print("No more videos available.")
            break
    print(f"Total videos in directory:{downloaded_count}")
else:
    # If this script is not being run as the main program, print a message indicating so
    print("No videos found with resolution higher than the minimum set resoultion")


