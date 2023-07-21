import cv2
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui


class ImageViewer(QtWidgets.QWidget):
    # parent 가 없어도 단독으로 사용가능하게
    # super parent를 상속받음
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    # 다시 위젯을 그려줌 여기서 웹캠 화면을 출력
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)

    # 웹캠 사이즈에 맞춰 조절
    def setImage(self, image):
        # 이미지가 안넘어오면 출력
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        # size가 다르면 fixed
        # image 사이즈는 640 480 웹캠 크기
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()


class ShowVideo(QtCore.QObject):
    flag = 1  # 이미지 경로를 각각 다르게 해주기위해

    VideoSignal1 = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)
        self.run_video = True
        self.camera = cv2.VideoCapture(0)

    def startVideo(self):
        # run_video가 true인 동안 실행
        while self.run_video:
            # 웹캠 영상 이미지 가져옴
            self.ret, self.image = self.camera.read()
            # 웹캠 영상 이미지 크기 가져옴
            height, width = self.image.shape[:2]
            # rgb형태로 변환
            color_swapped_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.qt_image = QtGui.QImage(color_swapped_image.data,
                                         width,
                                         height,
                                         color_swapped_image.strides[0],
                                         QtGui.QImage.Format_RGB888)

            # 각각의 화면에 웹캠 영상 이미지 내보냄
            self.VideoSignal1.emit(self.qt_image)

            # 영상 이미지 갱신 간격
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(25, loop.quit)  # 25 ms
            loop.exec_()

    def restartVideo(self):
        self.run_video = True
        self.startVideo()