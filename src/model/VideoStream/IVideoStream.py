from abc import ABC, abstractmethod
from numpy import ndarray


class VideoStream(ABC):
    @abstractmethod
    def get_frame(self) -> ndarray:
        """
        Get current frame of the video stream
        :return: frame - ndarray
        """
        pass
