# Import necessary libraries
import time
import requests
import json

# Function to upload video to Instagram
def upload_video(video_url, access_token, ig_user_id):
    post_url = "https://graph.facebook.com/v10.0/{}/media".format(ig_user_id)
    payload = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": "instagram post",
        "access_token": access_token
    }
    response = requests.post(post_url, data=payload).json()
    print(response)  # Print the response for debugging purposes
    return response

# Function to get status code
def get_status_code(ig_container_id, access_token):
    graph_url = 'https://graph.facebook.com/v18.0/'
    url = graph_url + ig_container_id
    params = {
        'access_token': access_token,
        'fields': 'status_code'
    }
    response = requests.get(url, params=params).json()
    return response.get('status_code')  # Use .get() to safely access the value

# Function to publish video to Instagram
def publish_video(results, access_token, ig_user_id):
    if 'id' in results:
        creation_id = results['id']
        second_url = "https://graph.facebook.com/v18.0/{}/media_publish".format(ig_user_id)
        second_payload = {
            "creation_id": creation_id,
            "access_token": access_token
        }
        response = requests.post(second_url, data=second_payload).json()
        print(response)  # Print the response for debugging purposes
        print("Video Published to Instagram")
    else:
        print("Video not published")

# Main script
if __name__ == "__main__":
    video_url = "https://davidtadevosyan.publit.io/file/second-largest-task.mp4"
    access_token = 'EAATlJuWNRjIBO1BOoCt7jFlymSKGfqo5u02FoVf2edKG1CmKBDVvvm43QXdFJr4SA4Tx88hGp3qDOZBQeHc7PLp9M2FknQWvkg0b3PsBn94Ib5jFXWZBFvqi97v6W4okZCFmflsXgTcgE2eVZAiCt1upT761rZAqJse1T9mMMiXl5t7Nc1P0RTlaJ'
    ig_user_id = "17841464783727454"

    res = upload_video(video_url, access_token, ig_user_id)
    print("Please wait for some time...")
    print("Uploading is still in progress")
    time.sleep(10)

    # Check if 'id' exists in the response before accessing it
    if 'id' in res:
        ig_container_id = res['id']
        status_code = get_status_code(ig_container_id, access_token)
        print("Status code:", status_code)
        publish_video(res, access_token, ig_user_id)
    else:
        print("Upload failed, 'id' not found in response.")
