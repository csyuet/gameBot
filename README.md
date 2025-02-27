## Computer Vision Project - Fishing bot in Pet Pals
-	Automates a fishing mini-game by detecting the game objects in real-time.
-	Uses object detection with YOLOv11 to interact with in-game elements.
-	Model petpals-fishing-bot/8 (https://app.roboflow.com/6uo-testing/petpals-fishing-bot/models) was trained and used
<img width="700" alt="Screenshot 2025-02-28 at 2 13 16 AM" src="https://github.com/user-attachments/assets/6520a42c-1efa-40e8-a7b2-3ff9ca1ee7a0" />



<img width="1047" alt="image" src="https://github.com/user-attachments/assets/90db34e3-2757-4fed-aef6-f95e6ce984df" />
The bot will first detect and click on the baits, then click the bubbles to start fishing. Next, it will continuously track the positions of new bubbles and click them automatically until the fishing is successful. The bot will repeat this process until the user presses the 'q' key.
