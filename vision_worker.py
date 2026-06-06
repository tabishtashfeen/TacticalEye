import mss
import cv2
import numpy as np
import requests
import time
from ultralytics import YOLO

# Initialize YOLO model configured for AMD ROCm / DirectML execution providers
model = YOLO("models/radar_yolov8n.pt")

# Bounding box coordinates for a standard 1080p resolution CS2 minimap
# Adjust matching your in-game safezone / HUD scale settings
RADAR_ROI = {"top": 40, "left": 40, "width": 200, "height": 200}

API_ENDPOINT = "http://localhost:5000/api/telemetry/position"

def continuous_inference():
    with mss.mss() as sct:
        print("[TacticalEye] Real-time screen capture pipeline initialized via ROCm/DirectML.")
        while True:
            start_time = time.time()

            # Low-overhead desktop screen capture
            screen_img = np.array(sct.grab(RADAR_ROI))
            frame = cv2.cvtColor(screen_img, cv2.COLOR_RGBA2BGR)

            # Predict coordinates from map landmarks/player icon
            results = model.predict(frame, verbose=False, device="0") # Enforce GPU utilization

            for result in results:
                boxes = result.boxes.xyxy.cpu().numpy()
                if len(boxes) > 0:
                    # Calculate center point of your position bounding box on the minimap
                    x_center = int((boxes[0][0] + boxes[0][2]) / 2)
                    y_center = int((boxes[0][1] + boxes[0][3]) / 2)

                    # POST positions asynchronously to the central backend layer
                    payload = {"mapName": "de_mirage", "radarX": x_center, "radarY": y_center}
                    try:
                        requests.post(API_ENDPOINT, json=payload, timeout=0.05)
                    except requests.exceptions.RequestException:
                        pass # Prevent network micro-stutters from stalling main inference loop

            # Enforce execution ceiling matching radar display refresh intervals
            time.sleep(max(0.016, 0.016 - (time.time() - start_time)))

if __name__ == "__main__":
    continuous_inference()
