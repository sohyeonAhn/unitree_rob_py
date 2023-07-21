import sys
import time
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from myunitree import myunitree

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

    def sendCmd(self):
        self.isungb1.sendCmd()

    def click_N(self):
        self.isungb1.click_N()
    def click_S(self):
        self.isungb1.click_S()
    def click_W(self):
        self.isungb1.click_W()
    def click_E(self):
        self.isungb1.click_E()
    def click_Stop(self):
        self.isungb1.click_Stop()
    def click_L(self):
        self.isungb1.click_L()
    def click_R(self):
        self.isungb1.click_R()

    def udp_connect(self):
        self.isungb1.connect()
        h1 = Tread1(self)
        h1.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()

