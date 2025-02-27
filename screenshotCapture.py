import os
import time
import threading
import pyautogui
import keyboard

# Function to take screenshots of a specific monitor
def take_screenshot(stop_event, screen_region=None):
    # Create a directory for screenshots if it doesn't exist
    counter = 0
    timestamp = time.strftime("%Y-%m-%d_%H-%M")
    if not os.path.exists(f"img/{timestamp}"):
        os.makedirs(f"img/{timestamp}")

    while not stop_event.is_set():
        # Take screenshot of the specified region
        keyboard.wait("c")
        counter += 1
        
        if screen_region:
            screenshot = pyautogui.screenshot(region=screen_region)
        else:
            screenshot = pyautogui.screenshot()  # Full screen

        screenshot.save(f"img/{timestamp}/{counter}.png")
        print(f"screenshot has saved to img/{timestamp}/{counter}.png")


# Main function
def main():

    # Get the screen region for the desired monitor
    x = 0
    y = 52
    width = int(920)
    height = int(640)
    screen_region = (x, y, width, height)

    # Create a stop event for the screenshot thread
    stop_event = threading.Event()
    
    # Create and start the screenshot thread
    screenshot_thread = threading.Thread(target=take_screenshot, args=(stop_event, screen_region))
    screenshot_thread.start()

    print("Screenshot program started. Press 'q' to quit.")

    # Listen for keyboard input to quit the program
    keyboard.wait("q")

    # Set the stop event to end the screenshot thread
    stop_event.set()

    # Wait for the screenshot thread to finish
    screenshot_thread.join()

    print("Program ended.")

if __name__ == "__main__":
    main()
