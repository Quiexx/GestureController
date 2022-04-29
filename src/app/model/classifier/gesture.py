import pickle
from abc import ABC, abstractmethod

import torch
from numpy import ndarray

from src.app.config import GESTURE_CLASSIFIER_DEVICE, GESTURE_CLASSIFIER_PATH


class IGestureClassifier(ABC):
    """
    Abstract class for classes that work with NN models
    """

    @abstractmethod
    def predict(self, data: ndarray) -> ndarray:
        """
        Get model prediction on the data
        :param data: data to be transmitted to the model
        :return: prediction
        """
        pass


class GestureClassifier(IGestureClassifier):
    """
    Class that works with PyTorch model.
    Model is loaded from pickle file.
    """

    model_path = GESTURE_CLASSIFIER_PATH
    device = GESTURE_CLASSIFIER_DEVICE

    def __init__(self):
        """
        Crates classifier, loads the torch model
        """
        with open(self.model_path, "rb") as f:
            self.model = pickle.load(f)

    def predict(self, data: ndarray) -> ndarray:
        """
        Get model prediction on the data
        :param data: data to be transmitted to the model
        :return: prediction
        """
        return self.model(torch.from_numpy(data).float()).detach().numpy()
