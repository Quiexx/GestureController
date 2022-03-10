from src.IoC.IoC import ioc
from src.model.DataPreparator.IDataPreparator import IDataPreparator
from src.model.Gesture.IGesture import IGesture
from src.model.GestureClassifier.IGestureClassifier import IGestureClassifier
from src.model.GestureRecognizer.IGestureRecognizer import IGestureRecognizer
from src.model.HandTracker import IHandTracker
from src.model.VideoStream import IVideoStream


class OneModelRecognizer(IGestureRecognizer):

    def __init__(self,
                 video: IVideoStream,
                 hand_tracker: IHandTracker,
                 dp: IDataPreparator,
                 classifier: IGestureClassifier):

        self.video = video
        self.hand_tracker = hand_tracker
        self.dp = dp
        self.classifier = classifier


    def get_gesture(self) -> IGesture:
        positions = self.hand_tracker.find_marks(self.video.get_frame())
        self.dp.prepare(positions)
        trajectory = self.classifier.predict(self.dp.get_data())
        return ioc("Gesture.Get", trajectory=trajectory)