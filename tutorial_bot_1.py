from OAuth_autorization import authenticate_and_get_youtube_service
from OAuth_autorization import upload_videos_with_task
from bot_1_0_2 import main 

def bot():
    main()
    youtube_service = authenticate_and_get_youtube_service()
    upload_videos_with_task(youtube_service)
if __name__ == "__main__":
    
    bot()
