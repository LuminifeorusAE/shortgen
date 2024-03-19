import g4f
import pyautogui
import time
import pygetwindow as gw
import cv2
import numpy as np
import threading

# Function to ask ChatGPT4
def ask_GPT(prompt: str) -> str:
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": f"{prompt}"}],
    )
    return response  # Return the response content

# Function to write the generated text to a file
def write_generated_text_to_file(generated_text: str, file_name: str):
    if generated_text:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(generated_text)
    else:
        print("ChatGPT4 didn't provide a response. Unable to write to the file.")

# Function to remove "Certainly!" or "Sure" from the beginning of the text
def remove_starting_word(text):
    if text.startswith("Certainly!") or text.startswith("Sure"):
        text = text[len("Certainly!"):] if text.startswith("Certainly!") else text[len("Sure"):]
        # Remove leading spaces and commas
        text = text.lstrip(", ")  
    return text

"""!!! Fix !!!"""
# Function to set window parameters for YouTube Shorts
def set_youtube_shorts_window_parameters():
    screen = gw.getWindowsWithTitle("generated_script.py")[0]
    screen.resizeTo(1080, 324)  # Assuming 19:6 aspect ratio (1080x324)
    screen.moveTo(0, 0) 


# Function to type in Visual Studio Code with adjusted typing speed
def type_in_visual_studio_code(file_name: str, video_duration: int):
    with open(file_name, 'r', encoding='utf-8') as read_file:
        generated_text = read_file.read()

        # Calculate the length of the generated text
        text_length = len(generated_text)

        # Calculate the typing speed to fit within the video duration
        typing_speed = text_length / video_duration if video_duration > 0 else 1

        # Calculate the typing interval based on the typing speed
        typing_interval = 0.5 / typing_speed

        # Type the generated text with the calculated typing interval
        pyautogui.typewrite(generated_text, interval=typing_interval)

        # Locate to the begining of the file
        
        pyautogui.keyDown("pgup")



'''USING THIS FUNCTION UNTIL I WILL FIND A WAY TO OPEN "genreated_script.py"IN YOUTUBE SHORTS ASPECT RATIO'''

# Function to record the left half of the screen with increased cropping
def record_left_half_screen_cropped(window_title: str, theme: str, recording_event: threading.Event, duration: int = 58):
    screen = gw.getWindowsWithTitle(window_title)[0]
    
    # Calculate the left half coordinates with increased cropping
    left_half_width = screen.width // 3 # Use left screen part by cuting it in tree halfs
    left_half_height = screen.height - 200  # Crop 100 pixels from the bottom
    left_half_rect = (screen.left + 50, screen.top + 50, left_half_width, left_half_height)

    
    # Append theme to the file name
    themed_file_name = f"{theme}_task.avi"

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(themed_file_name, fourcc, 20.0, (left_half_width, left_half_height))

    start_time = time.time()
    while time.time() - start_time < duration:
        if recording_event.is_set():  # Check if recording should be stopped
            break
        '''ADD BREACKPOINTS'''
        screenshot = pyautogui.screenshot(region=left_half_rect)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
 
    out.release()
    cv2.destroyAllWindows()

# Function for nameing a video file after generated task for generating a description and title for youtube videos
def extract_theme_from_script(file_name):
    theme = "Untitled"  # Default theme if no function name found
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip().startswith("def "):
                theme = line.strip()[4:].split('(')[0]
                break
    return theme


def main():
    # Get user input
    user_question = "randomly generate a task in Python, not longer than 30 lines"
    video_duration = 58 # One-minute video duration

    # Get response from ChatGPT4
    generated_text = ask_GPT(user_question)

    # Remove starting word if present
    generated_text = remove_starting_word(generated_text)

    # Write response to a Python file
    file_name = "generated_script.py"
    write_generated_text_to_file(generated_text, file_name)

    # Set YouTube Shorts window parameters
    set_youtube_shorts_window_parameters()

    # Update the typing record file name with the theme
    # Extract theme from the generated script (function name)
    theme = extract_theme_from_script(file_name)
    typing_record_file_name = f"{theme}_task.mp4"

    # Create threading events for synchronization
    recording_event = threading.Event()

    # Create threads for typing and recording the left half of the screen with increased cropping
    typing_thread = threading.Thread(target=type_in_visual_studio_code, args=(file_name, video_duration))
    recording_thread = threading.Thread(target=record_left_half_screen_cropped, args=("Visual Studio Code", theme, recording_event, video_duration))

    # Start the threads
    recording_thread.start()
    typing_thread.start()

    # Wait for the typing thread to finish
    typing_thread.join()

    # Wait for 2 seconds after typing is finished
    time.sleep(2)

    # Turn off video recording by setting the recording event
    recording_event.set()

    # Wait for the recording thread to finish
    recording_thread.join()

    # Print the name of the video file
    print(f"Video file named: {typing_record_file_name}")

if __name__ == "__main__":
    main()