from abc import ABC, abstractmethod
from typing import Optional

import cv2
from numpy import ndarray
import numpy as np
import mediapipe as mp

from src.app.config import MODEL_COMPLEXITY, MIN_DETECTION_CONFIDENCE, MIN_TRACKING_CONFIDENCE, GESTURE_ICONS, \
    MIN_GESTURE_CONFIDENCE
from src.app.gesture_handler.gesture_handler import KBMGestureHandler
from src.app.model.classifier.gesture import GestureClassifier


class ModelManager(ABC):
    """
    Class that operates with NN models
    """

    @abstractmethod
    def handle_image(self, image: ndarray) -> ndarray:
        """
        Handle an image
        :param image: image to handle
        :return: handled image
        """
        pass

    @property
    @abstractmethod
    def draw_hands(self) -> bool:
        """
        Determines whether to draw hand landmarks
        :return: True if hand landmarks drawing is on else False
        """
        pass

    @draw_hands.setter
    @abstractmethod
    def draw_hands(self, value: bool) -> None:
        """
        Set draw_hands property
        :param value: bool
        :return: None
        """
        pass

    @property
    @abstractmethod
    def draw_result(self) -> bool:
        """
        Determines whether to draw result of prediction
        :return: True if result of prediction drawing is on else False
        """
        pass

    @draw_result.setter
    @abstractmethod
    def draw_result(self, value: bool) -> None:
        """
        Set draw_result property
        :param value: bool
        :return: None
        """
        pass

    @property
    @abstractmethod
    def show_image(self) -> bool:
        """
        Determines whether to show image from camera
        :return: True if camera image showing is on else False
        """
        pass

    @show_image.setter
    @abstractmethod
    def show_image(self, value: bool) -> None:
        """
        Set show_image property
        :param value: bool
        :return: None
        """
        pass


class GestureModelManager(ModelManager):
    """
    Manager that uses mediapipe hands and GestureClassifier to handle images
    """

    def __init__(self) -> None:
        """
        Creates GestureModelManager
        """
        self._mp_hands = mp.solutions.hands
        self._mp_drawing = mp.solutions.drawing_utils
        self._mp_drawing_styles = mp.solutions.drawing_styles
        self._model = GestureClassifier()
        self._draw_hands = False
        self._draw_pred_res = False
        self._show_image = False
        self._gesture_handler = KBMGestureHandler()

    @property
    def draw_hands(self) -> bool:
        """
        Determines whether to draw hand landmarks
        :return: True if hand landmarks drawing is on else False
        """
        return self._draw_hands

    @draw_hands.setter
    def draw_hands(self, value: bool) -> None:
        """
        Set draw_hands property
        :param value: bool
        :return: None
        """
        self._draw_hands = value

    @property
    def draw_result(self) -> bool:
        """
        Determines whether to draw result of prediction
        :return: True if result of prediction drawing is on else False
        """
        return self._draw_pred_res

    @draw_result.setter
    def draw_result(self, value: bool) -> None:
        """
        Set draw_result property
        :param value: bool
        :return: None
        """
        self._draw_pred_res = value

    @property
    def show_image(self) -> bool:
        """
        Determines whether to show image from camera
        :return: True if camera image showing is on else False
        """
        return self._show_image

    @show_image.setter
    def show_image(self, value: bool) -> None:
        """
        Set show_image property
        :param value: bool
        :return: None
        """
        self._show_image = value

    def handle_image(self, image: ndarray) -> ndarray:
        """
        Handle an image
        :param image: image to handle
        :return: handled image
        """
        image, gest_num, data = self.get_gesture(image)
        self._gesture_handler.handle(gest_num, data)

        return image

    def get_gesture(self, image: ndarray) -> tuple[ndarray, Optional[int], list]:
        """
        Predicts gesture on the image, draw hand landmarks and result of the prediction on the image if needed
        :param image: image to predict a gesture on
        :return: handled image, gesture index, gesture data (landmarks coordinates)
        """
        flipped_horizontally = False
        gest_num = None
        data = None

        with self._mp_hands.Hands(
                model_complexity=MODEL_COMPLEXITY,
                min_detection_confidence=MIN_DETECTION_CONFIDENCE,
                min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        ) as hands:

            results = hands.process(image)

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                data = [[hand_landmarks.landmark[lm].x, hand_landmarks.landmark[lm].y, hand_landmarks.landmark[lm].z]
                        for lm in self._mp_hands.HandLandmark]

                data_np = np.array(data).reshape(-1).reshape(1, -1)
                res = self._model.predict(data_np)
                prob = int(res.max(axis=1, initial=0)[0] * 100)
                gest_num = res.argmax(1)[0]

                if prob < MIN_GESTURE_CONFIDENCE * 100:
                    gest_num = None

                if not self._show_image:
                    image = np.zeros_like(image)

                if self.draw_hands:
                    self._mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        self._mp_hands.HAND_CONNECTIONS,
                        self._mp_drawing_styles.get_default_hand_landmarks_style(),
                        self._mp_drawing_styles.get_default_hand_connections_style())

                image = cv2.flip(image, 1)
                flipped_horizontally = True

                if self.draw_result and gest_num is not None:
                    gesture_icon = GESTURE_ICONS[gest_num]
                    gesture_icon = np.array(gesture_icon)
                    h, w, _ = gesture_icon.shape
                    image[:h, :w] = gesture_icon
                    image = cv2.putText(image, f"{gest_num} ({prob}%)",
                                        (105, 110), cv2.FONT_HERSHEY_PLAIN, 0.8, (255, 255, 255), 1)

            elif not self._show_image:
                image = np.zeros_like(image)

        if not flipped_horizontally:
            image = cv2.flip(image, 1)
        image = cv2.flip(image, 0)

        return image, gest_num, data
