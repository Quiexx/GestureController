import pickle
from abc import ABC, abstractmethod

import torch
from numpy import ndarray

from src.app.config import GESTURE_CLASSIFIER_DEVICE, GESTURE_CLASSIFIER_PATH


class IGestureClassifier(ABC):

    @abstractmethod
    def predict(self, data: ndarray) -> ndarray:
        pass


class GestureClassifier(IGestureClassifier):
    model_path = GESTURE_CLASSIFIER_PATH
    device = GESTURE_CLASSIFIER_DEVICE

    def __init__(self):
        with open(self.model_path, "rb") as f:
            self.model = pickle.load(f)

    def predict(self, hand_track) -> ndarray:
        return self.model(torch.from_numpy(hand_track).float()).detach().numpy()
