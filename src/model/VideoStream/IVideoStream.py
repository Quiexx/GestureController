from abc import ABC, abstractmethod
from numpy import ndarray


class VideoStream(ABC):
    @abstractmethod
    def read(self) -> ndarray:
        """Returns RGB frame of video like numpy.ndarray"""

    @abstractmethod
    def is_ready(self) -> bool:
        """Returns True if video is ready to be read"""

    @abstractmethod
    def close(self):
        """Closes stream"""
