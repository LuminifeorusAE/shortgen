from OAuth_autorization import authenticate_and_get_youtube_service
from OAuth_autorization import upload_videos_with_task
from bot_1_0_2 import main 
from upload_to_inst import InstagramAPI



#bot
def bot():
    main()
    """!!!Make this functions OOP !!!"""
    youtube_service = authenticate_and_get_youtube_service()
    upload_videos_with_task(youtube_service)
    # Create an instance of the InstagramAPI class
    instagram_api = InstagramAPI()
    # Call the method to post and publish a reel
    instagram_api.post_and_publish_reel()



    
if __name__ == "__main__":
    
    bot()
