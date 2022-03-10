from abc import ABC, abstractmethod

from numpy import ndarray


class HandTracker(ABC):

    @abstractmethod
    def find_hands(self, frame: ndarray) -> list[dict]:
        pass
