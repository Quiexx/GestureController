from abc import ABC, abstractmethod

import torch
from numpy import ndarray
from torch import nn

from src.app.config import GESTURE_CLASSIFIER_DEVICE, GESTURE_CLASSIFIER_PATH


class IGestureClassifier(ABC):

    @abstractmethod
    def predict(self, data: ndarray) -> ndarray:
        pass


class WristGestureClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.norm = nn.BatchNorm1d(42)
        self.linear = nn.Linear(42, 7)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        return self.softmax(self.linear(self.norm(x)))


class GestureClassifier(IGestureClassifier):
    model_path = GESTURE_CLASSIFIER_PATH
    device = GESTURE_CLASSIFIER_DEVICE

    def __init__(self):
        self.model = WristGestureClassifier()
        self.model.load_state_dict(torch.load(self.model_path, map_location=torch.device(self.device)))

    def predict(self, hand_track) -> ndarray:
        self.model.eval()
        with torch.no_grad():
            res = self.model(torch.from_numpy(hand_track).float()).detach().numpy()
        return res