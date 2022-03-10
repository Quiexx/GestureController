from abc import ABC, abstractmethod

from src.model.Gesture.IGesture import IGesture


class IGestureRecognizer(ABC):

    @abstractmethod
    def get_gesture(self) -> IGesture:
        """Returns most likely gesture"""

