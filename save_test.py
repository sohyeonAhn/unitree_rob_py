import sys
import time
import traceback
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import pyqtgraph as pg
import numpy as np
from myunitree_value_test import myunitree
from myDialog import myDialog

class Tread1(QThread):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        try:
            while True:
                time.sleep(0.2)
                self.parent.sendCmd()
        except Exception as e:
            print("Tread1에서 예외 발생:")
            traceback.print_exc()

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'./control_gui.ui', self)
        self.isungb1 = myunitree()

        self.actionGraph = QAction("Open Graph", self)
        self.actionGraph.triggered.connect(self.open_graph_window)

        self.fileMenu = self.menuBar().addMenu("Graph")
        self.fileMenu.addAction(self.actionGraph)

        self.connect_btn.clicked.connect(self.udp_connect)
        # ------ 버튼 -----------------------------------------------------
        self.N_btn.pressed.connect(self.click_N)
        self.S_btn.pressed.connect(self.click_S)
        self.W_btn.pressed.connect(self.click_W)
        self.E_btn.pressed.connect(self.click_E)
        self.Stop_btn.clicked.connect(self.click_Stop)
        self.L_btn.pressed.connect(self.click_L)
        self.R_btn.pressed.connect(self.click_R)
        self.Up_btn.pressed.connect(self.click_Up)
        self.Down_btn.pressed.connect(self.click_Down)
        self.euler_btn.pressed.connect(self.click_Euler)
        self.height_btn.pressed.connect(self.click_Height)
        self.trot_btn.pressed.connect(self.click_Trot)
        # ------ 값 입력 ----------------------------------------------------
        self.input_vel_0.valueChanged.connect(self.vel_0_value_changed)
        self.input_vel_1.valueChanged.connect(self.vel_1_value_changed)
        self.input_yawspeed.valueChanged.connect(self.yawspeed_value_changed)

        self.input_euler_0.valueChanged.connect(self.vel_euler_value_0_changed)
        self.input_euler_1.valueChanged.connect(self.vel_euler_value_1_changed)
        self.input_euler_2.valueChanged.connect(self.vel_euler_value_2_changed)
        self.input_height.valueChanged.connect(self.bodyHeight_value_changed)
        # ------ Label -----------------------------------------------------
        self.SOC_label = self.findChild(QLabel, "SOC_label")
        self.Mode_label = self.findChild(QLabel, "mode_label")
        self.GaitType_label = self.findChild(QLabel, "gaittype_label")

    def open_graph_window(self):
        self.graph_window = myDialog(self)
        self.graph_window.show()

    def sendCmd(self):
        self.isungb1.sendCmd()

        self.highstate_textBrowser.append(self.isungb1.highstate_info)

        self.data_SOC = self.isungb1.hstate_bms_SOC
        self.data_mode = self.isungb1.hstate_mode
        self.data_gaitType =self.isungb1.hstate_gaitType
        self.update_label()

        self.plot_data_bodyHeight = self.isungb1.hstate_bodyHeight
        self.plot_data_footforce = self.isungb1.hstate_footforce

#------데이터 입력 이벤트------------
    def vel_0_value_changed(self, value):
        self.vel_0_N = value
        self.vel_0_S = -value
    def vel_1_value_changed(self, value):
        self.vel_1_W = value
        self.vel_1_E = -value
    def yawspeed_value_changed(self, value):
        self.yawspeed_value_L = value
        self.yawspeed_value_R = -value

    def vel_euler_value_0_changed(self,value):
        self.vel_euler_0 = value
    def vel_euler_value_1_changed(self,value):
        self.vel_euler_1 = value
    def vel_euler_value_2_changed(self,value):
        self.vel_euler_2 = value

    def bodyHeight_value_changed(self, value):
        self.vel_bodyheight = value

#------버튼 클릭 이벤트--------------
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
    def click_R(self):
        self.isungb1.click_R(self.yawspeed_value_R)
    def click_Up(self):
        self.isungb1.click_Up()
    def click_Down(self):
        self.isungb1.click_Down()
    def click_Euler(self):
        self.isungb1.click_Euler(self.vel_euler_0,self.vel_euler_1,self.vel_euler_2)
        # self.isungb1.click_Euler()
    def click_Height(self):
        self.isungb1.click_Height(self.vel_bodyheight)
    def click_Trot(self):
        self.isungb1.click_Trot()
#----------------------------------
    def udp_connect(self):
        try:
            self.isungb1.connect()
            h1 = Tread1(self)
            h1.start()
        except Exception as e:
            print("udp_connect에서 예외 발생:")
            traceback.print_exc()

    def update_label(self):
        self.SOC_label.setText("{:.1f}".format(self.data_SOC))
        self.Mode_label.setText("{:.1f}".format(self.data_mode))
        self.GaitType_label.setText("{:.1f}".format(self.data_gaitType))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()