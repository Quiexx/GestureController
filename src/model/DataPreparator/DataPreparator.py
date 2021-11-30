from abc import ABC, abstractmethod

from numpy import ndarray


class DataPreparator(ABC):

    @abstractmethod
    def get_data(self, position) -> ndarray:
        pass