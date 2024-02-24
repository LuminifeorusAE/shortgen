import requests
import json
import time

class InstagramAPI:
    def __init__(self):
        # Initialize the base URL for the Graph API and load configuration from file
        self.graph_url = 'https://graph.facebook.com/v19.0/'
        with open('graph_api_param.json', 'r') as f:
            self.config = json.load(f)

    def post_reel(self, caption='Test Caption', media_type='REELS', share_to_feed='', thumb_offset='',
                  video_url='https://davidtadevosyan.publit.io/file/second-largest-task.mp4'):
        # Post a reel on Instagram
        access_token = self.config['access_token']
        instagram_account_id = self.config['instagram_account_id']
        url = self.graph_url + instagram_account_id + '/media'
        param = {
            'access_token': access_token,
            'caption': caption,
            'media_type': media_type,
            'share_to_feed': share_to_feed,
            'thumb_offset': thumb_offset,
            'video_url': video_url
        }
        try:
            response = requests.post(url, params=param)
            response_json = response.json()
            print("\nResponse from post_reel:", response_json)
            return response_json
        except requests.RequestException as e:
            print("Error posting reel:", e)
            return None

    def status_of_upload(self, ig_container_id=''):
        # Check the status of upload
        access_token = self.config['access_token']
        url = self.graph_url + ig_container_id
        param = {
            'access_token': access_token,
            'fields': 'status_code'
        }
        try:
            response = requests.get(url, params=param)
            response_json = response.json()
            print("\nResponse from status_of_upload:", response_json)
            return response_json
        except requests.RequestException as e:
            print("Error getting upload status:", e)
            return None

    def publish_container(self, creation_id=''):
        # Publish the container
        access_token = self.config['access_token']
        instagram_account_id = self.config['instagram_account_id']
        url = self.graph_url + instagram_account_id + '/media_publish'
        param = {
            'access_token': access_token,
            'creation_id': creation_id
        }
        try:
            response = requests.post(url, params=param)
            response_json = response.json()
            print("\nResponse from publish_container:", response_json)
            return response_json
        except requests.RequestException as e:
            print("Error publishing container:", e)
            return None

    def post_and_publish_reel(self):
        # Combine posting and publishing a reel into a single operation
        response_post_reel = self.post_reel()
        if response_post_reel:
            ig_container_id = response_post_reel.get('id')
            if ig_container_id:
                max_retries = 10  # Maximum number of retries
                retries = 0
                while retries < max_retries:
                    response_status_of_upload = self.status_of_upload(ig_container_id)
                    if response_status_of_upload and response_status_of_upload.get('status_code') == 'FINISHED':
                        response_publish_container = self.publish_container(ig_container_id)
                        if response_publish_container:
                            print("Reel successfully published!")
                        else:
                            print("Error publishing reel.")
                        break
                    elif response_status_of_upload and response_status_of_upload.get('status_code') == 'IN_PROGRESS':
                        print("Upload still in progress. Waiting for 10 seconds...")
                        time.sleep(10)
                        retries += 1
                    else:
                        print("Error getting upload status. Aborting.")
                        break
                else:
                    print("Upload not finished within the specified number of retries.")
            else:
                print("Error: Missing Instagram container ID.")

# Example usage:
if __name__ == "__main__":
    # Create an instance of InstagramAPI
    instagram_api = InstagramAPI()
    # Call the method to post and publish a reel
    instagram_api.post_and_publish_reel()
