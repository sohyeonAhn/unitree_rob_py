import sys
import time
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from myunitree import myunitree

# 스레드
class Tread1(QThread):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent

    def run(self): # 스레드가 시작되면 실행
        while True:
            time.sleep(0.2) # 0.2초 대기 후 실행
            self.parent.sendCmd() # 부모(MyWindow)의 sendCmd 호출

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

        self.Act_1_btn.clicked.connect(self.udp_connect)
        self.Act_2_btn.clicked.connect(self.click_act2)


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

    # udp 통신
    def udp_connect(self):
        self.isungb1.connect()
        h1 = Tread1(self)
        h1.start()

    # 모드 6 테스트
    def click_act2(self):
        self.isungb1.mode6()

    # myunitree 인스턴스를 통해 명령을 보내는 함수
    def sendCmd(self):
        self.isungb1.sendCmd()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()

