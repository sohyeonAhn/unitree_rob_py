import time

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5 import uic
from OpenGL.GL import *
from OpenGL.GLU import *
from robot3dmodel_4 import robot3d

class View3DDialog(QDialog):
    def __init__(self,parent):
        super().__init__()
        # super().__init__(parent) # parent 입력하면 modal
        uic.loadUi(r'./dialog_3D_gui.ui', self)
        self.parent = parent # 상위 윈도우의 데이터를 접근
        # print(self.parent.test)
        self.open_gl = robot3d(parent=self.View_3d)  # parent=self.프레임위젯 이름
        self.open_gl.setMinimumSize(701, 511)

        self.plot_timer = QTimer(self)
        self.plot_timer.timeout.connect(self.opengl3d)
        self.plot_timer.start(200)

        # self.opengl3d()

    def opengl3d(self):
        self.data_rpy = self.parent.view_data_rpy
        self.data_motorQ = self.parent.view_data_motorQ
        self.open_gl.robotRPY3d(self.data_rpy)
        self.open_gl.robotMotor3d(self.data_motorQ)
        self.open_gl.update()



