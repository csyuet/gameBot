from ultralytics import YOLO
import pyautogui
from PIL import Image
import numpy as np

model = YOLO('best.onnx')

decision = {
    "Bubble": False,
    "bait": False
}
region = (0, 53, 920, 695-53)
# region = (0, 53, 1050, 840-53)
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

results = model([grayscale_image], conf=.8, save=True)
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
# run_bot(decision)

print(decision)
