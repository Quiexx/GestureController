import unittest
import numpy as np
from unittest.mock import patch, Mock

from src.IoC.IoC import ioc
from src.model.GestureRecognizer.OneModelRecognizer import OneModelRecognizer


class TestOneModelRecognizer(unittest.TestCase):
    @patch("src.model.VideoStream.IVideoStream")
    @patch("src.model.HandTracker.IHandTracker")
    @patch("src.model.DataPreparator.IDataPreparator")
    @patch("src.model.GestureClassifier.IGestureClassifier")
    def setUp(self, mock_video, mock_tracker, mock_dp, mock_classifier) -> None:
        self.mock_video = mock_video()
        self.mock_tracker = mock_tracker()
        self.mock_dp = mock_dp()
        self.mock_classifier = mock_classifier()
        self.recognizer = OneModelRecognizer(self.mock_video, self.mock_tracker, self.mock_dp, self.mock_classifier)

    def test_get_gesture_normal(self):

        frame = np.zeros((1))
        positions = dict()
        data = np.ones(1)
        trajectory = np.ones(1)
        right_gesture = ioc("Gesture.Get", trajectory)

        self.mock_video.get_frame.return_value = frame
        self.mock_tracker.find_marks.return_value = positions
        self.mock_dp.get_data.return_value = data
        self.mock_classifier.predict.return_value = trajectory

        gesture = self.recognizer.get_gesture()

        self.mock_video.get_frame.assert_called()
        self.mock_tracker.find_marks.assert_called()
        self.mock_dp.prepare.assert_called_with(positions)
        self.mock_dp.get_data.assert_called()
        self.mock_classifier.predict.assert_called()

        self.assertEqual(right_gesture.get_name(), gesture.get_name())
