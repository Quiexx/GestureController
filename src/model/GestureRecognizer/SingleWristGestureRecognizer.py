import datetime
import logging

from src.model.DataPreparator.DataPreparator import DataPreparator
from src.model.GestureClassifier.GestureClassifier import GestureClassifier
from src.model.GestureRecognizer.GestureRecognizer import GestureRecognizer
from src.model.GestureRecognizer.Gestures import Gesture
from src.model.HandTracker.HandTracker import HandTracker
from src.model.VideoStream.VideoStream import VideoStream

logging.basicConfig(filename="SingleWristGestureRecognizer.log", filemode='w', level=logging.INFO)


class SingleWristGestureRecognizer(GestureRecognizer):
    __gesture_codes = {
        0: Gesture.UNKNOWN
    }

    __logger = logging.getLogger("SingleWristGestureRecognizer")

    def __init__(self,
                 stream: VideoStream,
                 hand_tracker: HandTracker,
                 gesture_classifier: GestureClassifier,
                 data_preparator: DataPreparator) -> None:
        self.__stream = stream
        self.__hand_tracker = hand_tracker
        self.__gesture_classifier = gesture_classifier
        self.__data_preparator = data_preparator

    def get_gesture(self) -> Gesture:
        if not self.__stream.is_ready():
            return Gesture.UNKNOWN

        try:
            frame = self.__stream.read()
            position = self.__hand_tracker.find_hands(frame)
            hand_track = self.__data_preparator.get_data(position)
            probs = self.__gesture_classifier.predict(hand_track)

        except Exception as exc:
            time = datetime.datetime.now()
            self.__logger.exception("Exception {}".format(time), exc_info=exc)
            return Gesture.UNKNOWN

        return self.__gesture_codes[probs.argmax()]
