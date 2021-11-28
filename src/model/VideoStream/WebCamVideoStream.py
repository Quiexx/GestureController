import cv2
import numpy
from numpy import ndarray

from src.model.VideoStream.VideoStream import VideoStream


class WebCamVideoStream(VideoStream):

    __width = 640
    __height = 480
    __channels = 3

    def __init__(self, cam: int) -> None:
        self.__cap = cv2.VideoCapture(cam)

    def read(self) -> ndarray:
        if not self.is_ready():
            return numpy.zeros(shape=(self.__width, self.__height, self.__channels))

        success, frame = self.__cap.read()

        if not success:
            return numpy.zeros(shape=(self.__width, self.__height, self.__channels))

        frame = cv2.resize(frame, (self.__width, self.__height), interpolation=cv2.INTER_AREA)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def is_ready(self) -> bool:
        return self.__cap.isOpened()

    def close(self):
        self.__cap.release()
