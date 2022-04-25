import os.path

import cv2
import json
import numpy as np
import mediapipe as mp
from PIL import Image

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

marks = [
    mp_hands.HandLandmark.WRIST,
    mp_hands.HandLandmark.THUMB_CMC,
    mp_hands.HandLandmark.THUMB_MCP,
    mp_hands.HandLandmark.THUMB_IP,
    mp_hands.HandLandmark.THUMB_TIP,
    mp_hands.HandLandmark.INDEX_FINGER_MCP,
    mp_hands.HandLandmark.INDEX_FINGER_PIP,
    mp_hands.HandLandmark.INDEX_FINGER_DIP,
    mp_hands.HandLandmark.INDEX_FINGER_TIP,
    mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
    mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
    mp_hands.HandLandmark.MIDDLE_FINGER_DIP,
    mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
    mp_hands.HandLandmark.RING_FINGER_MCP,
    mp_hands.HandLandmark.RING_FINGER_PIP,
    mp_hands.HandLandmark.RING_FINGER_DIP,
    mp_hands.HandLandmark.RING_FINGER_TIP,
    mp_hands.HandLandmark.PINKY_MCP,
    mp_hands.HandLandmark.PINKY_PIP,
    mp_hands.HandLandmark.PINKY_DIP,
    mp_hands.HandLandmark.PINKY_TIP,
]

# dataset_file = "gesture_ds.json"
# with open("gesture_ds.json", "r") as f:
#     ds = json.load(f)
#
# if ds is None:
#     shot_count_dict = {}
#     ds = {}
#     with open("gesture_ds.json", "w") as f:
#         json.dump({}, f)
# else:
#     shot_count_dict = {int(code): len(d) for code, d in ds.items()}

gesture_dir = "data"
gesture_count = 9
shot_count_dict = {}

for gest_num in range(gesture_count):
    gest_data_path = os.path.join(gesture_dir, str(gest_num))
    if not os.path.exists(gest_data_path):
        os.mkdir(gest_data_path)

    shot_count_dict[gest_num] = len(os.listdir(gest_data_path))

with open("gestures_ru.json", "r", encoding="utf-8") as f:
    gesture_dict = json.load(f)
    gesture_names = list(gesture_dict.keys())

gesture_snapshots = []
shapshots_path = "gesture_snapshots/{}.jpg"
for name in gesture_names:
    file_name = shapshots_path.format(name)
    im = Image.open(file_name).convert('RGB')
    im = np.array(im)
    im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    gesture_snapshots.append(im)

shots_per_gesture = 1200
shots_made = 0

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
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = np.zeros_like(image)

        image.flags.writeable = True

        coords = []
        mirror_coords = []

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            for mark in marks:
                x, y, z = hand_landmarks.landmark[mark].x, hand_landmarks.landmark[mark].y, hand_landmarks.landmark[
                    mark].z
                coords.append(x)
                coords.append(y)
                coords.append(z)
                mirror_coords.append(1 - x)
                mirror_coords.append(y)
                mirror_coords.append(z)

            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        image = cv2.flip(image, 1)

        cv2.putText(image,
                    gesture_names[current_gesture],
                    (165, 20),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.4,
                    (255, 255, 255)
                    )

        shots_made = shot_count_dict.get(current_gesture, 0)
        cv2.putText(image,
                    f"{shots_made}/{shots_per_gesture}",
                    (165, 40),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.4,
                    (255, 255, 255)
                    )

        cv2.putText(image,
                    f"SPACE - make shot",
                    (165, 60),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.4,
                    (255, 255, 255)
                    )

        cv2.putText(image,
                    f"TAB - next gesture",
                    (165, 80),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.4,
                    (255, 255, 255)
                    )

        snap = gesture_snapshots[current_gesture]
        h, w, _ = snap.shape
        image[:h, :w] = snap

        cv2.imshow('MediaPipe Hands', image)
        key = cv2.waitKey(5)
        if key == 27:
            break
        elif key == 32:
            gest_name = gesture_names[current_gesture]
            gest_code = gesture_dict[gest_name]

            if coords:
                gest_count = shot_count_dict.get(gest_code, 0)
                coords_path = os.path.join(gesture_dir, str(gest_code), str(gest_count) + ".npy")
                mir_coords_path = os.path.join(gesture_dir, str(gest_code), str(gest_count + 1) + ".npy")

                np.save(coords_path, coords)
                np.save(mir_coords_path, mirror_coords)

                shot_count_dict[gest_code] = gest_count + 2

        elif key == 9:
            current_gesture += 1
            if current_gesture == len(gesture_names):
                break

cap.release()
