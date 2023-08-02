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
        time.sleep(0.5)
        data = self.conn.getData()
        for paket in data:
            self.hstate.parseData(paket)

            # self.highstate_info = f"footForce:\t\t{self.hstate.footForce}\n" \
            #                       f"bodyHeight:\t\t{self.hstate.bodyHeight}\n" \
            #                       f"position:\t\t{self.hstate.position}\n"

            self.highstate_info = f"footForce:\t\t{self.hstate.footForce}\n" \
                f"bodyHeight:\t\t{self.hstate.bodyHeight}\n"

            self.hstate_bodyHeight = self.hstate.bodyHeight

            self.hstate_bms_SOC = self.hstate.bms.SOC

            self.hstate_footforce = self.hstate.footForce


    def sendCmd(self):
        self.cmd_bytes = self.hcmd.buildCmd(debug=False)
        self.conn.send(self.cmd_bytes)
        # print(self.hcmd.mode)

        self.cmdInit()

    def click_N(self,vel_0):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.VEL_WALK # mode 2
        self.hcmd.velocity = [vel_0, 0]  # -1  ~ +1
        print("walk 앞")

    def click_S(self,vel_0):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.VEL_WALK  # mode 2
        self.hcmd.velocity = [vel_0, 0]  # -1  ~ +1
        print("walk 뒤")

    def click_W(self,vel_1):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.VEL_WALK  # mode 2
        self.hcmd.velocity = [0, vel_1]  # -1  ~ +1
        print("walk 좌")

    def click_E(self,vel_1):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.VEL_WALK  # mode 2
        self.hcmd.velocity = [0, vel_1]  # -1  ~ +1
        print("walk 우")

    def click_Stop(self):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.IDLE
        self.hcmd.velocity = [0,0]  # -1  ~ +1
        self.hcmd.yawSpeed = 0
        print("STOP")

    def click_L(self,yawspeed_value):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.VEL_WALK
        self.hcmd.yawSpeed = yawspeed_value
        print("Click L")

    def click_R(self,yawspeed_value):
        self.cmdInit()
        self.hcmd.mode = MotorModeHigh.VEL_WALK
        self.hcmd.yawSpeed = yawspeed_value
        print("Click R")

