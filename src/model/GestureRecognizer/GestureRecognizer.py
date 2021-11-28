from abc import ABC, abstractmethod

from numpy import ndarray

from src.model.GestureRecognizer.Gestures import Gesture


class GestureRecognizer(ABC):

    @abstractmethod
    def get_gesture(self) -> Gesture:
        # TODO Написать список жестов
        """Returns most likely gesture"""

    @abstractmethod
    def get_predictions(self) -> ndarray:
        """Returns probabilities of gestures"""
