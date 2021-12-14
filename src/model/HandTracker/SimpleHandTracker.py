from typing import Union

import mediapipe as mp

from src.model.HandTracker.HandTracker import HandTracker

LANDMARKS = mp.solutions.hands.HandLandmark


class SimpleHandTracker(HandTracker):
    __num_hands = 1

    def __init__(self,
                 static_image_mode: bool = True,
                 min_detection_confidence: float = 0.5,
                 landmark: mp.solutions.hands.HandLandmark = LANDMARKS.INDEX_FINGER_DIP) -> None:

        self.__hands = mp.solutions.hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=self.__num_hands,
            min_detection_confidence=min_detection_confidence)

        self.__landmark = landmark

    def find_hands(self, frame) -> Union[None, tuple[int, int]]:
        results = self.__hands.process(frame)

        if not results.multi_hand_landmarks:
            return None

        frame_height, frame_width, _ = frame.shape

        hand_landmarks = results.multi_hand_landmarks[0].landmark[self.__landmark]
        x, y = hand_landmarks.x * frame_width, hand_landmarks.y * frame_height
        return int(x), int(y)
