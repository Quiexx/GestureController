from abc import ABC, abstractmethod


class IGesture(ABC):

    @abstractmethod
    def get_name(self) -> str:
        """
        Get name of the gesture
        :return: str
        """
        pass
