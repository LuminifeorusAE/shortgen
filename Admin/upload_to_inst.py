import requests
import json
import time

graph_url = 'https://graph.facebook.com/v19.0/'

def post_reel(caption='Test Caption', media_type='REELS', share_to_feed='', thumb_offset='',
              video_url='https://davidtadevosyan.publit.io/file/second-largest-task.mp4'):
    with open('graph_api_param.json', 'r') as f:
        config = json.load(f)
    
    access_token = config['access_token']
    instagram_account_id = config['instagram_account_id']
    
    url = graph_url + instagram_account_id + '/media'
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

def status_of_upload(ig_container_id=''):
    with open('graph_api_param.json', 'r') as f:
        config = json.load(f)
    
    access_token = config['access_token']
    
    url = graph_url + ig_container_id
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

def publish_container(creation_id=''):
    with open('graph_api_param.json', 'r') as f:
        config = json.load(f)
    
    access_token = config['access_token']
    instagram_account_id = config['instagram_account_id']
    
    url = graph_url + instagram_account_id + '/media_publish'
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

# Run functions
if __name__ == "__main__":
    response_post_reel = post_reel()
    if response_post_reel:
        ig_container_id = response_post_reel.get('id')
        if ig_container_id:
            max_retries = 10  # Adjust as needed
            retries = 0
            while retries < max_retries:
                response_status_of_upload = status_of_upload(ig_container_id)
                if response_status_of_upload and response_status_of_upload.get('status_code') == 'FINISHED':
                    response_publish_container = publish_container(ig_container_id)
                    if response_publish_container:
                        print("Reel successfully published!")
                    else:
                        print("Error publishing reel.")
                    break  # Exit the loop if publishing was successful
                elif response_status_of_upload and response_status_of_upload.get('status_code') == 'IN_PROGRESS':
                    print("Upload still in progress. Waiting for 10 seconds...")
                    time.sleep(10)  # Wait for 10 seconds before checking again
                    retries += 1
                else:
                    print("Error getting upload status. Aborting.")
                    break
            else:
                print("Upload not finished within the specified number of retries.")
        else:
            print("Error: Missing Instagram container ID.")
