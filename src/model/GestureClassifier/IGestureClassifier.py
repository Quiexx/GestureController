from abc import ABC, abstractmethod

from numpy import ndarray


class IGestureClassifier(ABC):

    @abstractmethod
    def predict(self, hand_track) -> ndarray:
        pass