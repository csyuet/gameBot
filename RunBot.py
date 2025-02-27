from ultralytics import YOLO
import threading
import pyautogui
import keyboard
import numpy as np
from PIL import Image
import os
import time
from inference import get_model

region = (0, 53, 920, 695-53)
# region = (0, 53, 1050, 840-53)

# timestamp = time.strftime("%Y-%m-%d_%H-%M")
# if not os.path.exists(f"img/{timestamp}"):
#     os.makedirs(f"img/{timestamp}")

def run_bot(decision, screenshot):
# def run_bot(decision):
    if "bait_location" in decision and "Bubble_location" in decision:
        if decision["fish"] == False:
            pyautogui.click(decision["bait_location"])
            decision["fish"] = True
        else:
            pyautogui.click(decision["Bubble_location"])
            decision["fish"] = False

    elif "Bubble_location" in decision:
        pyautogui.click(decision["Bubble_location"])
    # elif "bait_location" not in decision and "Bubble_location" not in decision:
    #     second = time.strftime("%M%S")
    #     screenshot.save(f"img/{timestamp}/{second}.png")
    #     print(f"screenshot has saved to img/{timestamp}/{second}.png")

def bot(stop_event, model):
    # screenx_center = 1050/2
    # screeny_center = (840-53)/2+53

    pyautogui.FAILSAFE = False
    fish = False
    
    while not stop_event.is_set(): #1050, 840
        
        decision = {
        "Bubble": False,
        "bait": False,
        "fish": fish
        }
        
        screenshot = pyautogui.screenshot(region=region)
        # Convert the screenshot to a NumPy array
        screenshot_array = np.array(screenshot)

        # Apply the weighted sum formula to convert to grayscale
        grayscale_array = (
            0.2125 * screenshot_array[:, :, 0] +  # Red channel
            0.7154 * screenshot_array[:, :, 1] +  # Green channel
            0.0721 * screenshot_array[:, :, 2]    # Blue channel
        ).astype(np.uint8)

        # Convert back to a PIL image
        grayscale_image = Image.fromarray(grayscale_array)

        results = model([grayscale_image], conf=.8)
        boxes = results[0].boxes.xyxy.tolist()
        classes = results[0].boxes.cls.tolist()
        names = results[0].names
        confidences = results[0].boxes.conf.tolist()

        for box, cls, conf in zip(boxes, classes, confidences):
            x1, y1, x2, y2 = box
            
            center_x = (x1+x2) / 2
            center_y = (y1+y2) / 2 + 53

            name = names[int(cls)]
            
            if name=="Bubble":
                decision["Bubble"] = True
                decision["Bubble_location"] = (center_x, center_y)
            elif name=="bait":
                decision["bait"] = True
                # distance = 1050 - center_x
                distance = center_x
                if "bait_location" in decision:
                    if distance < decision["bait_distance"]:
                        decision["bait_location"] = (center_x, center_y)
                        decision["bait_distance"] = distance
                else:
                    decision["bait_location"] = (center_x, center_y)
                    decision["bait_distance"] = distance
        # run_bot(decision, screenshot)
        run_bot(decision)

        # os.system('cls' if os.name == 'nt' else 'clear')
        print(decision)
        fish = decision["fish"]
        del decision
        

def main():
    model = YOLO('Christmas.onnx')
    # model = get_model(model_id="petpals-fishing-bot/8")
    stop_event = threading.Event()

    bot_thread = threading.Thread(target=bot, args=(stop_event, model))
    bot_thread.start()

    keyboard.wait("q")

    stop_event.set()
    bot_thread.join()

    print("Program ended.")

if __name__ == "__main__":
    main()
