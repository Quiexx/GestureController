from src.model.GestureRecognizer.GestureRecognizer import GestureRecognizer
from src.model.VideoStream.VideoStream import VideoStream


class SingleWristGestureRecognizer(GestureRecognizer):

    def __init__(self, stream: VideoStream) -> None:
        self.stream = stream

    def get_gesture(self):
        pass

    def get_predictions(self):
        pass
