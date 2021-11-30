from abc import ABC, abstractmethod


class HandTracker(ABC):

    @abstractmethod
    def find_hands(self, frame):
        pass
