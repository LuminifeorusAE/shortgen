#video_downloader.py
import os 
import random
import requests
import json
from tqdm import tqdm

#Class for downloading videos from pexels.com
"""!!!Modify to take videos for multiple sites for better randomization of video selection"""
class VideoDownloader:
    def __init__(self):
        self.api_key = self.api_keys()
        #seting themes to search in the website(you can add and change by your choise)
        self.themes = ["beach", "city", "drone footages", "nature"]

#Generate your api key from https://www.pexels.com/api/
    def api_keys(self):
        try:
            #optional name of the JSON file
            with open('pexels_api.json') as file:
                config = json.load(file)
                #name of the key in the json file that contains api key as value
                return config["pexels_api_key"]
            #handling error if the file is not exist
        except FileNotFoundError:
            print("Error: Your Json file should be in the same directory.")
            return None
            #handling error if the problem is the key or value in the json(less possible)
        except KeyError:
            print("If its in the correct directory please check if its not empety or corrupted.")
            return None
    
    #defining a function to search videos using api in the website
    def search_videos(self,theme):
        try:
            url = f'https://api.pexels.com/videos/search?query={theme}&per_page=80'
            headers = {'Authorization': self.api_key}
            response = requests.get(url,headers=headers)
            response.raise_for_status()
        #parsing the json responce from api in the dict
            data=response.json()
            #print out succesful responce from website
            print("Status Code:", response.status_code)
            print("Successful API Responce:")
            videos = data.get('videos',[])
            print("Number of videos Found:", len(videos))
            print("Videos")
            for video in videos:
                print("Video ID:", video.get('id'))
                print("Video URL:", video.get('url'))
                print("Video Duration:", video.get('duration'))
                print("Video Quality:", video.get('video_files')[0].get('quality'))
                print("Video Width:", video.get('video_files')[0].get('width'))
                print("Video Height:", video.get('video_files')[0].get('height'))
                print("-" *50)
            

            return videos
        except requests.RequestException as e:
            print(f"Error Searching for videos: {e}")
            return[]
        
if __name__ == "__main__":
    downloader = VideoDownloader()
    downloader.search_videos(theme=random.choice(downloader.themes))