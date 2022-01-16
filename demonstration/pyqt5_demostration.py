import cv2
import sys

import numpy

from tools import draw_marks
from src.model.HandTracker.AllMarksHandTracker import AllMarksHandTracker
from src.model.VideoStream.WebCamVideoStream import WebCamVideoStream

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    mode = 1

    def run(self):
        stream = WebCamVideoStream(0)
        hand_tracker = AllMarksHandTracker()
        while True:
            image = stream.read()
            result = hand_tracker.find_hands(image)

            if self.mode == -1:
                image = numpy.zeros_like(image)

            if result:
                if self.mode == 1:
                    image = draw_marks(image, result, pt_clr=(0, 0, 0), con_clr=(255, 228, 225))
                else:
                    image = draw_marks(image, result, pt_clr=(255, 255, 255), con_clr=(105, 105, 105))

            image = cv2.flip(image, 1)

            h, w, ch = image.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(image.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)

    def on_click(self):
        self.mode = -self.mode


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Demonstration"
        self.mode = 1
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(800, 800)
        self.label = QLabel(self)
        self.label.move(80, 160)
        self.label.resize(640, 480)
        button = QPushButton('Show only marks', self)
        button.resize(200, 50)
        button.move(295, 50)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        button.clicked.connect(th.on_click)
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    display_image_widget = App()
    display_image_widget.show()
    app.exec_()
