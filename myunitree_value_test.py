import time
from ucl.common import byte_print, decode_version, decode_sn, getVoltage, pretty_print_obj, lib_version
from ucl.highCmd import highCmd
from ucl.highState_b1 import highState
from ucl.unitreeConnection import unitreeConnection, HIGH_WIFI_DEFAULTS, HIGH_WIRED_DEFAULTS
from ucl.enums import MotorModeHigh, GaitType
from ucl.complex import motorCmd

class myunitree:
    def __init__(self):
        i = 0
    def connect(self):
        self.conn = unitreeConnection(HIGH_WIFI_DEFAULTS)  # 네트워크 연결
        self.conn.startRecv()

        self.hcmd = highCmd()
        self.hstate = highState()

    def cmdInit(self):
        time.sleep(0.01)
        data = self.conn.getData()
        for paket in data:
            self.hstate.parseData(paket)

            # self.highstate_info = f"bodyHeight:\t\t{self.hstate.bodyHeight}\n"

            self.highstate_info = f"Position:\t\t{self.hstate.position}\n"

            self.hstate_bodyHeight = self.hstate.bodyHeight
            self.hstate_bms_SOC = self.hstate.bms.SOC
            self.hstate_footforce = self.hstate.footForce
            self.hstate_mode =self.hstate.mode
            self.hstate_gaitType =self.hstate.gaitType
            self.hstate_position = self.hstate.position

            self.hstate_rpy = [self.hstate.imu.rpy[0],self.hstate.imu.rpy[1],self.hstate.imu.rpy[2]]
            self.hstate_motorQ = []
            for i in range(20):
                self.hstate_motorQ.append(self.hstate.motorstate[i].q)

    def sendCmd(self):
        self.cmd_bytes = self.hcmd.buildCmd(debug=False)
        self.conn.send(self.cmd_bytes)
        self.cmdInit()
        # print(self.hcmd.mode)
        # print(self.hcmd.gaitType)
    #------ 뱡향키 입력 메소드 ---------------------------------
    def click_N(self,vel_0):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.VEL_WALK # mode 2
        self.hcmd.velocity = [vel_0, 0]  # -1  ~ +1
        print(vel_0)
    def click_S(self,vel_0):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.VEL_WALK  # mode 2
        self.hcmd.velocity = [vel_0, 0]  # -1  ~ +1
    def click_W(self,vel_1):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.VEL_WALK  # mode 2
        self.hcmd.velocity = [0, vel_1]  # -1  ~ +1
    def click_E(self,vel_1):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.VEL_WALK  # mode 2
        self.hcmd.velocity = [0, vel_1]  # -1  ~ +1
    def click_Stop(self):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.FORCE_STAND
        self.hcmd.velocity = [0,0]  # -1  ~ +1
        self.hcmd.yawSpeed = 0
    def click_L(self,yawspeed_value):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.VEL_WALK
        self.hcmd.yawSpeed = yawspeed_value
    def click_R(self,yawspeed_value):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.VEL_WALK
        self.hcmd.yawSpeed = yawspeed_value
    def click_force_Stop(self):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.IDLE
        self.hcmd.gaitType = GaitType.IDLE
        self.hcmd.velocity = [0,0]  # -1  ~ +1
        self.hcmd.yawSpeed = 0
        self.hcmd.euler = [0, 0, 0]
        print("강제 STOP")
    # -------------------------------------------------------
    def click_Up(self):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.STAND_UP
        print("Click Up")
    def click_Down(self):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.STAND_DOWN
        print("Click Down")

    def click_Euler(self,vel_row,vel_pitch,vel_yaw): #self,vel_row,vel_pitch,vel_yaw
        self.cmdInit()

        # euler = [Roll, Pitch, Yaw]
        # Row: (+)왼쪽, (-)오른쪽
        # Pitch: (+)고개 숙이기 ,(-)고개 들기
        # Yaw: (+)왼쪽, (-)오른쪽
        self.hcmd.euler = [vel_row,vel_pitch,vel_yaw]

    def click_Height(self,vel_bodyHeight):
        self.cmdInit()
        # self.hcmd.mode = MotorModeHigh.FORCE_STAND
        self.hcmd.bodyHeight = vel_bodyHeight # default: 0.28m

    # ------ Mode ComboBox 입력 메소드 --------------------
    def click_ModeCombo_IDLE(self):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.IDLE # mode  0
    def click_ModeCombo_Force_Stand(self):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.FORCE_STAND # mode  1
    def click_ModeCombo_VEL_WALK(self):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.VEL_WALK # mode 2
    def click_ModeCombo_STAND_DOWN(self):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.STAND_DOWN # mode 5
    def click_ModeCombo_STAND_UP(self):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.STAND_UP # mode 6

    #------ GaitType ComboBox 입력 메소드 --------------------
    def click_GaitTypeCombo_IDLE(self):
        self.cmdInit()
        self.hcmd.gaitType = GaitType.IDLE  # GaitType 0
    def click_GaitTypeCombo_Trot(self):
        self.cmdInit()
        self.hcmd.gaitType = GaitType.TROT  # GaitType 1
    def click_GaitTypeCombo_CLIMB_STAIR(self):
        self.cmdInit()
        self.hcmd.gaitType = GaitType.CLIMB_STAIR  # GaitType 2
    def click_GaitTypeCombo_TROT_OBSTACLE(self):
        self.cmdInit()
        self.hcmd.gaitType = GaitType.TROT_OBSTACLE  # GaitType 3
