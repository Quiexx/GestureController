from abc import ABC, abstractmethod

from numpy import ndarray


class IDataPreparator(ABC):

    @abstractmethod
    def get_data(self) -> ndarray:
        pass

    @abstractmethod
    def prepare(self, positions: dict):
        pass