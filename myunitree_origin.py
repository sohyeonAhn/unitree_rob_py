import sys
import time
import math
import threading

sys.path.append('../unitree_legged_sdk/lib/python/amd64')
import robot_interface as sdk

class myunitree:
    def __init__(self):

        i = 0

    def sendCmd(self):
        self.udp.SetSend(self.cmd)
        self.udp.Send()
        print(self.cmd.mode)

    def connect(self):

        HIGHLEVEL = 0xee

        self.udp = sdk.UDP(HIGHLEVEL, 8080, "192.168.123.220", 8082)

        self.cmd = sdk.HighCmd()
        self.state = sdk.HighState()
        self.udp.InitCmdData(self.cmd)

        self.cmdInit()

    def cmdInit(self): # 구조체 값

        self.cmd.mode = 0  # 0:idle, default stand      1:forced stand     2:walk continuously
        self.cmd.gaitType = 0
        self.cmd.speedLevel = 0
        self.cmd.footRaiseHeight = 0
        self.cmd.bodyHeight = 0
        self.cmd.euler = [0.0, 0.0, 0.0]
        self.cmd.velocity = [0.0, 0.0]
        self.cmd.yawSpeed = 0.0
        self.cmd.reserve = 0

    def click_N(self):
        self.cmdInit()
        self.cmd.mode = 2
        self.cmd.velocity[0] = float(0.2)

    def click_S(self):
        self.cmdInit()
        self.cmd.mode = 2
        self.cmd.velocity[0] = -0.2

    def click_W(self):
        self.cmdInit()
        self.cmd.mode = 2
        self.cmd.velocity[1] = 0.2

    def click_E(self):
        self.cmdInit()
        self.cmd.mode = 2
        self.cmd.velocity[1] = -0.2

    def click_Stop(self):
        self.cmdInit()
        self.cmd.mode = 0
        self.cmd.velocity[0] = 0
        self.cmd.velocity[1] = 0
        self.cmd.yawSpeed = 0

    def mode6(self):
        self.cmdInit()
        self.cmd.mode = 6

