import sys
import time
import cv2
import traceback
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
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

class CameraThread(QThread):
    update_image = pyqtSignal(QImage)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.camera = cv2.VideoCapture(0)
        # self.camera = cv2.VideoCapture('rtsp://192.168.10.223:554/live.sdp')

    def run(self):
        while True:
            ret, frame = self.camera.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.update_image.emit(q_image)

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
        self.move_vel_0 = 0
        self.move_vel_1 = 0
        self.AutoMode_flag = False

        #------ Dialog ----------------------------------------------------
        self.actionGraph = QAction("Open Graph", self)
        self.actionPositionGraph = QAction("Position View", self)
        self.view_robot_3D = QAction("3D View", self)
        self.actionGraph.triggered.connect(self.open_graph_window)
        self.actionPositionGraph.triggered.connect(self.open_position_window)
        self.view_robot_3D.triggered.connect(self.open_view_robot_3D)

        self.fileMenu = self.menuBar().addMenu("Graph")
        self.fileMenu.addAction(self.actionGraph)
        self.fileMenu.addAction(self.actionPositionGraph)
        self.fileMenu.addAction(self.view_robot_3D)

        # ------ 버튼 -----------------------------------------------------
        self.connect_btn.clicked.connect(self.udp_connect) # 통신 연결 버튼
        self.camera_on_btn.clicked.connect(self.camera_on)
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

        self.auto_start_position_btn.pressed.connect(self.click_auto_start_Position)
        self.auto_end_position_btn.pressed.connect(self.click_auto_end_Position)

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

        self.input_position_0.valueChanged.connect(self.vel_position_value_0_changed)
        self.input_position_1.valueChanged.connect(self.vel_position_value_1_changed)

        # ------ Label -----------------------------------------------------
        self.SOC_label = self.findChild(QLabel, "SOC_label")
        self.Mode_label = self.findChild(QLabel, "mode_label")
        self.GaitType_label = self.findChild(QLabel, "gaittype_label")
        self.State_Position_0_label = self.findChild(QLabel, "state_position_0_label")
        self.State_Position_1_label = self.findChild(QLabel, "state_position_1_label")
        self.Yawspeed_value_label = self.findChild(QLabel, "yawspeed_value_label")
        #------ ComboBox ---------------------------------------------------
        self.Mode_ComboBox = self.findChild(QComboBox,"mode_comboBox")
        self.Mode_ComboBox.currentIndexChanged.connect(self.mode_combobox_changed)

        self.GaitType_ComboBox = self.findChild(QComboBox, "gaittype_comboBox")
        self.GaitType_ComboBox.currentIndexChanged.connect(self.gaittype_comboBox_changed)

#------ Dialog Window 띄우기 ----------------------
    def open_graph_window(self):
        self.graph_window = myDialog(self)
        self.graph_window.show()
    def open_position_window(self):
        self.graph_window = PositionDialog(self)
        self.graph_window.show()
    def open_view_robot_3D(self):
        self.view_window = View3DDialog(self)
        self.view_window.show()
#------ SendCmd -------------------------------------
    def sendCmd(self):
        self.isungb1.sendCmd()

        self.highstate_textBrowser.append(self.isungb1.highstate_info)

        self.data_SOC = self.isungb1.hstate_bms_SOC
        self.data_mode = self.isungb1.hstate_mode
        self.data_gaitType =self.isungb1.hstate_gaitType
        self.data_yawspeed = self.isungb1.hstate_yawspeed

        self.plot_data_bodyHeight = self.isungb1.hstate_bodyHeight
        self.plot_data_footforce = self.isungb1.hstate_footforce
        self.plot_data_position = self.isungb1.hstate_position

        self.view_data_rpy = self.isungb1.hstate_rpy
        self.view_data_motorQ = self.isungb1.hstate_motorQ
        self.view_data_quaternion =self.isungb1.hstate_quaternion

        self.update_label()

        # Auto 모드
        if self.AutoMode_flag == True:
            self.Auto_move_vel()

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

    def vel_position_value_0_changed(self,value):
        self.vel_position_0 = value
    def vel_position_value_1_changed(self,value):
        self.vel_position_1 = value

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

    def click_auto_start_Position(self):
        self.AutoMode_flag = True
    def click_auto_end_Position(self):
        self.AutoMode_flag = False
        self.isungb1.click_Stop()

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
        self.State_Position_0_label.setText("{:.1f}".format(self.plot_data_position[0]))
        self.State_Position_1_label.setText("{:.1f}".format(self.plot_data_position[1]))
        self.Yawspeed_value_label.setText("{:.01f}".format(self.data_yawspeed))

#------ 카메라 관련 메소드 ------------------------------------
    def camera_on(self):

        self.camera_thread = CameraThread(self)
        self.camera_thread.update_image.connect(self.update_camera_view)
        self.camera_thread.start()

    # 이미지에서 선을 감지하고 그려주는 함수
    def detect_lines(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # 입력 이미지를 흑백 이미지로 변환
        # 에지 검출을 통해 엣지 이미지 생성
        edges = cv2.Canny(gray_image, threshold1=50, threshold2=150)
        # 허프 변환을 사용하여 선 감지
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=5)

        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2) # 이미지에 감지된 선을 그림

        return image

    # 카메라 뷰를 업데이트하는 슬롯 함수
    @pyqtSlot(QImage)
    def update_camera_view(self, image):
        cv2_image = self.qimage_to_cv(image)  # QImage를 OpenCV 이미지로 변환
        image_with_lines = self.detect_lines(cv2_image) # 선 감지 함수 적용한 이미지 생성
        self.camera_view.setPixmap(QPixmap.fromImage(self.cv_to_qimage(image_with_lines)))  # 카메라 뷰 업데이트

    # QImage를 OpenCV 이미지로 변환하는 함수
    def qimage_to_cv(self, qimage):
        qimage = qimage.convertToFormat(QImage.Format_RGB888)
        width = qimage.width()
        height = qimage.height()
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())
        return np.array(ptr).reshape(height, width, 3)

    # OpenCV 이미지를 QImage로 변환하는 함수
    def cv_to_qimage(self, cv_image):
        height, width, channel = cv_image.shape
        bytes_per_line = 3 * width
        qimage = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return qimage

#------ Auto Position 메서드---------------------
    def Auto_move_vel(self):
        # plot_data_position: 현재 좌표 [y,x,높이]
        # vel_position_0: 지정한 y좌표
        # vel_position_1: 지정한 x좌표
        # y좌표 방향 확인
        if self.vel_position_0 > self.plot_data_position[0]:
            print(f"현재 위치1-1 :({self.plot_data_position[0]}, {self.plot_data_position[1]})")
            # y좌표 좌표 격차 확인
            if abs(self.vel_position_0 - self.plot_data_position[0]) > 0.1:
                print("1-1 격차가 0.1 초과")
                self.move_vel_0 = self.vel_0_N
            elif abs(self.vel_position_0 - self.plot_data_position[0]) < 0.1:
                print("1-1 격차가 0.1 미만")
                self.move_vel_0 = 0
        elif self.vel_position_0 < self.plot_data_position[0]:
            print(f"현재 위치1-2 :({self.plot_data_position[0]}, {self.plot_data_position[1]})")
            # y좌표 좌표 격차 확인
            if abs(self.vel_position_0 - self.plot_data_position[0]) > 0.1:
                print("1-2 격차가 0.1 초과")
                self.move_vel_0 = self.vel_0_S
            elif abs(self.vel_position_0 - self.plot_data_position[0]) < 0.1:
                print("1-2 격차가 0.1 미만")
                self.move_vel_0 = 0

        # x좌표 방향 확인
        # left(+)/right(-)
        if self.vel_position_1 > self.plot_data_position[1]:
            print(f"현재 위치2-1 :({self.plot_data_position[0]}, {self.plot_data_position[1]})")
            # x좌표 좌표 격차 확인
            if abs(self.vel_position_1 - self.plot_data_position[1]) > 0.1:
                print("2-1 격차가 0.1 초과")
                self.move_vel_1 = self.vel_1_W
            elif abs(self.vel_position_1 - self.plot_data_position[1]) <= 0.1:
                print("2-1 격차가 0.1 미만")
                self.move_vel_1 = 0
        elif self.vel_position_1 < self.plot_data_position[1]:
            print(f"현재 위치2-2 :({self.plot_data_position[0]}, {self.plot_data_position[1]})")
            # x좌표 좌표 격차 확인
            if abs(self.vel_position_1 - self.plot_data_position[1]) > 0.1:
                print("2-2 격차가 0.1 초과")
                self.move_vel_1 = self.vel_1_E
            elif abs(self.vel_position_1 - self.plot_data_position[1]) < 0.1:
                print("2-2 격차가 0.1 미만")
                self.move_vel_1 = 0

        # 좌표 지정 -> 이동
        self.isungb1.click_mult(self.move_vel_0, self.move_vel_1)

        # 좌표이동 완료
        if abs(self.vel_position_1 - self.plot_data_position[1]) < 0.1 and abs(self.vel_position_0 - self.plot_data_position[0]) < 0.1:
            print("좌표 지정 완료")
            self.click_auto_end_Position()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()