import PIL
import cv2
import json
import numpy as np
import mediapipe as mp
from PIL import Image

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

with open("gestures_ru.json", "r", encoding="utf-8") as f:
    gesture_names = list(json.load(f).keys())

current_gesture = 0
cap = cv2.VideoCapture(1)
with mp_hands.Hands(
        max_num_hands=1,
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = np.zeros_like(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True


        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        # Flip the image horizontally for a selfie-view display.

        image = cv2.flip(image, 1)
        image_with_text = image.copy()

        cv2.putText(image_with_text,
                    gesture_names[current_gesture],
                    (20, 20),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (255, 255, 255)
                    )

        cv2.imshow('MediaPipe Hands', image_with_text)
        key = cv2.waitKey(5)
        if key == 27:
            break
        elif key == 32:
            file_path = f"./gesture_snapshots/{gesture_names[current_gesture]}.jpg"
            im = Image.fromarray(image)
            im = im.resize((160, 120), PIL.Image.LANCZOS)
            im.save(file_path, "JPEG")
            # cv2.imwrite(file_path, image)
            current_gesture += 1
            if current_gesture >= len(gesture_names):
                break

cap.release()
