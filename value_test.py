import sys
import time
import cv2
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from myunitree_value_test import myunitree

from PyQt5.QtGui import *

class Tread1(QThread):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        while True:
            time.sleep(0.2)
            self.parent.sendCmd()

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'./control_gui.ui', self)

        self.isungb1 = myunitree()

        self.N_btn.clicked.connect(self.click_N)
        self.S_btn.clicked.connect(self.click_S)
        self.W_btn.clicked.connect(self.click_W)
        self.E_btn.clicked.connect(self.click_E)
        self.Stop_btn.clicked.connect(self.click_Stop)
        self.L_btn.clicked.connect(self.click_L)
        self.R_btn.clicked.connect(self.click_R)

        self.connect_btn.clicked.connect(self.udp_connect)
        self.camera_on_btn.clicked.connect(self.camera_on)

        self.input_vel_0.valueChanged.connect(self.vel_0_value_changed)
        self.input_vel_1.valueChanged.connect(self.vel_1_value_changed)
        self.input_yawspeed.valueChanged.connect(self.yawspeed_value_changed)


    def sendCmd(self):
        self.isungb1.sendCmd()

    #--------- 입력한 값 담기------------------
    def vel_0_value_changed(self, value):
        self.vel_0_N = value
        self.vel_0_S = -value
        # print("입력된 vel_0:", self.vel_0)
    def vel_1_value_changed(self, value):
        self.vel_1_W = value
        self.vel_1_E = -value
        # print("입력된 vel_1:", self.vel_1)
    def yawspeed_value_changed(self, value):
        self.yawspeed_value_L = value
        self.yawspeed_value_R = -value
        # print("입력된 yawspeed:", self.yawspeed_value)
    # -------- 컨트롤러--------
    def click_N(self):
        self.isungb1.click_N(self.vel_0_N)
    def click_S(self):
        self.isungb1.click_S(self.vel_0_S)
    def click_W(self):
        self.isungb1.click_W(self.vel_1_W)
    def click_E(self):
        self.isungb1.click_E(self.vel_1_E)
    def click_Stop(self):
        self.isungb1.click_Stop()
    def click_L(self):
        self.isungb1.click_L(self.yawspeed_value_L)
        # print("입력된 yawspeed_L:", self.yawspeed_value_L)
    def click_R(self):
        self.isungb1.click_R(self.yawspeed_value_R)
        # print("입력된 yawspeed_R:", self.yawspeed_value_R)

    # Udp 통신 연결
    def udp_connect(self):
        self.isungb1.connect()
        h1 = Tread1(self)
        h1.start()

    # 카메라 Qpixmap view
    def camera_on(self):
        # 이미지 테스트
        qPixmap =QPixmap()
        qPixmap.load("pixmap_image_sample.png")
        self.camera_view.setPixmap(qPixmap)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()

