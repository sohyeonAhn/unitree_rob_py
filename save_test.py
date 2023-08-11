import sys
import time
import traceback
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from myunitree_value_test import myunitree
from myDialog import myDialog
from PositionDialog import PositionDialog
from View3DDialog import View3DDialog


class Tread1(QThread):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        try:
            while True:
                time.sleep(0.01)
                self.parent.sendCmd()
        except Exception as e:
            print("Tread1에서 예외 발생:")
            traceback.print_exc()

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'./control_gui.ui', self)
        self.isungb1 = myunitree()
        #----- 변수 초기화 ------------------------------------------
        self.vel_0_N = 0
        self.vel_0_S = 0
        self.vel_1_W = 0
        self.vel_1_E = 0
        self.yawspeed_value_L = 0
        self.yawspeed_value_R = 0
        self.vel_euler_0 = 0
        self.vel_euler_1 = 0
        self.vel_euler_2 = 0
        #------ Dialog ----------------------------------------------------
        self.actionGraph = QAction("Open Graph", self)
        self.actionPositionGraph = QAction("Position View", self)
        self.view_robot_3D = QAction("3D View",self)
        self.actionGraph.triggered.connect(self.open_graph_window)
        self.actionPositionGraph.triggered.connect(self.open_position_window)
        self.view_robot_3D.triggered.connect(self.open_view_robot_3D)



        self.fileMenu = self.menuBar().addMenu("Graph")
        self.fileMenu.addAction(self.actionGraph)
        self.fileMenu.addAction(self.actionPositionGraph)
        self.fileMenu.addAction(self.view_robot_3D)

        # ------ 버튼 -----------------------------------------------------
        self.connect_btn.clicked.connect(self.udp_connect) # 통신 연결 버튼
        # 컨트롤러 버튼
        self.N_btn.pressed.connect(self.click_N)
        self.N_btn.released.connect(self.release_N)

        self.S_btn.pressed.connect(self.click_S)
        self.S_btn.released.connect(self.release_S)

        self.W_btn.pressed.connect(self.click_W)
        self.W_btn.released.connect(self.release_W)

        self.E_btn.pressed.connect(self.click_E)
        self.E_btn.released.connect(self.release_E)

        self.Stop_btn.clicked.connect(self.click_Stop)

        self.L_btn.pressed.connect(self.click_L)
        self.L_btn.released.connect(self.release_L)

        self.R_btn.pressed.connect(self.click_R)
        self.R_btn.released.connect(self.release_R)

        self.Up_btn.pressed.connect(self.click_Up)
        self.Down_btn.pressed.connect(self.click_Down)
        # euler, height 설정 버튼
        self.euler_btn.pressed.connect(self.click_Euler)
        self.height_btn.pressed.connect(self.click_Height)

        self.is_N_btn_pressed = False
        self.is_S_btn_pressed = False
        self.is_W_btn_pressed = False
        self.is_E_btn_pressed = False
        self.is_L_btn_pressed = False
        self.is_R_btn_pressed = False

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
        #------ ComboBox ---------------------------------------------------
        self.Mode_ComboBox = self.findChild(QComboBox,"mode_comboBox")
        self.Mode_ComboBox.currentIndexChanged.connect(self.mode_combobox_changed)

        self.GaitType_ComboBox = self.findChild(QComboBox, "gaittype_comboBox")
        self.GaitType_ComboBox.currentIndexChanged.connect(self.gaittype_comboBox_changed)


    def open_graph_window(self):
        self.graph_window = myDialog(self)
        self.graph_window.show()
    def open_position_window(self):
        self.graph_window = PositionDialog(self)
        self.graph_window.show()
    def open_view_robot_3D(self):
        self.view_window = View3DDialog(self)
        self.view_window.show()

    def sendCmd(self):
        self.isungb1.sendCmd()

        self.highstate_textBrowser.append(self.isungb1.highstate_info)

        self.data_SOC = self.isungb1.hstate_bms_SOC
        self.data_mode = self.isungb1.hstate_mode
        self.data_gaitType =self.isungb1.hstate_gaitType

        self.plot_data_bodyHeight = self.isungb1.hstate_bodyHeight
        self.plot_data_footforce = self.isungb1.hstate_footforce
        self.plot_data_position = self.isungb1.hstate_position

        self.view_data_rpy = self.isungb1.hstate_rpy
        self.view_data_motorQ = self.isungb1.hstate_motorQ

        self.update_label()

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
        self.is_N_btn_pressed = True
        self.N_btn.setStyleSheet("background-color: rgb(172, 206, 255);")
        self.isungb1.click_N(self.vel_0_N)
    def click_S(self):
        self.is_S_btn_pressed = True
        self.S_btn.setStyleSheet("background-color: rgb(172, 206, 255);")
        self.isungb1.click_S(self.vel_0_S)
    def click_W(self):
        self.is_W_btn_pressed = True
        self.W_btn.setStyleSheet("background-color: rgb(172, 206, 255);")
        self.isungb1.click_W(self.vel_1_W)
    def click_E(self):
        self.is_E_btn_pressed = True
        self.E_btn.setStyleSheet("background-color: rgb(172, 206, 255);")
        self.isungb1.click_E(self.vel_1_E)
    def click_Stop(self):
        self.isungb1.click_force_Stop()
    def click_L(self):
        self.is_L_btn_pressed = True
        self.L_btn.setStyleSheet("background-color: rgb(206, 206, 206);")
        self.isungb1.click_L(self.yawspeed_value_L)
    def click_R(self):
        self.is_R_btn_pressed = True
        self.R_btn.setStyleSheet("background-color: rgb(206, 206, 206);")
        self.isungb1.click_R(self.yawspeed_value_R)
    def click_Up(self):
        self.isungb1.click_Up()
    def click_Down(self):
        self.isungb1.click_Down()
    def click_Euler(self):
        self.isungb1.click_Euler(self.vel_euler_0,self.vel_euler_1,self.vel_euler_2)
    def click_Height(self):
        self.isungb1.click_Height(self.vel_bodyheight)

    def release_N(self):
        self.is_N_btn_pressed = False
        self.N_btn.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.isungb1.click_Stop()
    def release_S(self):
        self.is_S_btn_pressed = False
        self.S_btn.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.isungb1.click_Stop()
    def release_W(self):
        self.is_W_btn_pressed = False
        self.W_btn.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.isungb1.click_Stop()
    def release_E(self):
        self.is_E_btn_pressed = False
        self.E_btn.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.isungb1.click_Stop()
    def release_L(self):
        self.is_L_btn_pressed = False
        self.L_btn.setStyleSheet("background:rgb(112, 112, 112);"
                                 "color:rgb(255, 255, 255);")
        self.isungb1.click_Stop()
    def release_R(self):
        self.is_R_btn_pressed = False
        self.R_btn.setStyleSheet("background:rgb(112, 112, 112);"
                                 "color:rgb(255, 255, 255);")
        self.isungb1.click_Stop()

#------ 콤보 박스 클릭 이벤트 --------------
    def mode_combobox_changed(self, index):
        selected_item = self.Mode_ComboBox.currentText()
        print(f"Selected Mode: {selected_item}")

        if selected_item == "IDLE (0)":
            self.isungb1.click_ModeCombo_IDLE()
        elif selected_item == "Force Stand (1)":
            self.isungb1.click_ModeCombo_Force_Stand()
        # elif selected_item == "Vel Walk (2)":
            # self.isungb1.click_ModeCombo_VEL_WALK()
        elif selected_item == "Stand Down (5)":
            self.isungb1.click_ModeCombo_STAND_DOWN()
        elif selected_item == "Stand Up (6)":
            self.isungb1.click_ModeCombo_STAND_UP()

    def gaittype_comboBox_changed(self, index):
        selected_item = self.GaitType_ComboBox.currentText()
        print(f"Selected GaitType: {selected_item}")

        if selected_item == "IDLE (0)":
            self.isungb1.click_GaitTypeCombo_IDLE()
        elif selected_item == "Trot (1)":
            self.isungb1.click_GaitTypeCombo_Trot()
        elif selected_item == "Climb Stair (2)":
            self.isungb1.click_GaitTypeCombo_CLIMB_STAIR()
        elif selected_item == "Trot Obstacle (3)":
            self.isungb1.click_GaitTypeCombo_TROT_OBSTACLE()
#---------------------------------------------------------------------
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