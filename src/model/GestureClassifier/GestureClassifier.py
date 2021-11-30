from abc import ABC, abstractmethod

from numpy import ndarray


class GestureClassifier(ABC):

    @abstractmethod
    def predict(self, hand_track) -> ndarray:
        pass