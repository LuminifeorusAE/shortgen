from OAuth_autorization import authenticate_and_get_youtube_service, upload_videos_with_task
from bot_1_0_2 import main 
from upload_to_inst import InstagramAPI
from basic_upload import tik_tok_upload

# Function for YouTube bot
def run_youtube_bot():
    youtube_service = authenticate_and_get_youtube_service()
    upload_videos_with_task(youtube_service)

# Function for Instagram bot
def run_instagram_bot():
    instagram_api = InstagramAPI()
    instagram_api.post_and_publish_reel()

# Function for TikTok bot
def run_tiktok_bot():
    tik_tok_upload()

# Main bot function
def bot():
    
    main()

    # Run each bot/task one after another
    run_youtube_bot()
    run_instagram_bot()
    run_tiktok_bot()

if __name__ == "__main__":
    bot()
