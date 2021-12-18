import mediapipe as mp
from numpy import ndarray

from src.model.HandTracker.HandTracker import HandTracker

LANDMARKS = mp.solutions.hands.HandLandmark


class AllMarksHandTracker(HandTracker):
    __num_hands = 1

    def __init__(self,
                 static_image_mode: bool = True,
                 min_detection_confidence: float = 0.5,) -> None:
        self.__hands = mp.solutions.hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=self.__num_hands,
            min_detection_confidence=min_detection_confidence)

    def find_hands(self, frame: ndarray) -> list[dict]:
        results = self.__hands.process(frame)

        if not results.multi_hand_landmarks:
            return []

        frame_height, frame_width, _ = frame.shape

        result = []

        for mark in LANDMARKS:
            hand_landmark = results.multi_hand_landmarks[0].landmark[mark]
            x, y = hand_landmark.x * frame_width, hand_landmark.y * frame_height
            result.append({"landmark": mark, "x": int(x), "y": int(y)})

        return result
