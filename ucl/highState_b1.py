from ucl.enums import MotorModeHigh, GaitType, SpeedLevel
from enum import Enum
from ucl.common import float_to_hex, hex_to_float, encryptCrc, genCrc, byte_print
from ucl.complex import cartesian, led, bmsState, imu, motorState
import struct

class highState:
    def __init__(self): #highState len == 1087 / lowState len == 807
        self.head = bytearray(2)
        self.levelFlag = 0
        self.frameReserve = 0
        self.SN = bytearray(8)
        self.version = bytearray(8)
        self.bandWidth = bytearray(2)#2byte
        self.imu = imu([0.0,0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],0)
        self.motorstate = [motorState(0,0,0,0,0,0,0,0,0,[0,0])]*20
        self.bms = bmsState(0,0,0,0,0,0,[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.footForce = [bytes.fromhex('0000')]*4
        self.footForceEst = [bytes.fromhex('0000')]*4
        self.mode = MotorModeHigh.IDLE
        self.progress = 0.0
        self.gaitType = GaitType.IDLE
        self.footRaiseHeight = 0.0
        self.position = [0.0, 0.0, 0.0]
        self.bodyHeight = 0.0
        self.velocity = [0.0, 0.0,0.0]
        self.yawSpeed = 0.0
        self.rangeObstacle = bytearray(16)
        self.footPosition2Body = bytearray(48)
        self.footSpeed2Body = bytearray(48)
        #self.speedLevel = SpeedLevel.LOW_SPEED
        self.wirelessRemote = bytearray(40)
        self.reserve = bytearray(4)

    def dataToBmsState(self,data):
        version_h = data[0]
        version_l = data[1]
        bms_status = data[2]
        SOC = data[3]
        current = int.from_bytes(data[4:8], byteorder='little', signed=True)
        cycle = int.from_bytes(data[8:10], byteorder='little')
        BQ_NTC = [data[10], data[11],data[12], data[13],data[14], data[15],data[16], data[17]]
        MCU_NTC = [data[18], data[19],data[20], data[21],data[22], data[23],data[24], data[25]]
        cell_vol = [int.from_bytes(data[26:28], byteorder='little'), int.from_bytes(data[28:30], byteorder='little'), int.from_bytes(data[30:32], byteorder='little'), int.from_bytes(data[32:34], byteorder='little'), int.from_bytes(data[34:36], byteorder='little'),
                    int.from_bytes(data[36:38], byteorder='little'), int.from_bytes(data[38:40], byteorder='little'), int.from_bytes(data[40:42], byteorder='little'), int.from_bytes(data[42:44], byteorder='little'), int.from_bytes(data[44:46], byteorder='little'),
                    int.from_bytes(data[46:48], byteorder='little'), int.from_bytes(data[48:50], byteorder='little'), int.from_bytes(data[50:52], byteorder='little'), int.from_bytes(data[32:34], byteorder='little'), int.from_bytes(data[34:36], byteorder='little'),
                    int.from_bytes(data[56:58], byteorder='little'), int.from_bytes(data[58:60], byteorder='little'), int.from_bytes(data[60:62], byteorder='little'), int.from_bytes(data[62:64], byteorder='little'), int.from_bytes(data[64:66], byteorder='little'),
                    int.from_bytes(data[66:68], byteorder='little'), int.from_bytes(data[68:70], byteorder='little'), int.from_bytes(data[70:72], byteorder='little'), int.from_bytes(data[72:74], byteorder='little'), int.from_bytes(data[74:76], byteorder='little'),
                    int.from_bytes(data[76:78], byteorder='little'), int.from_bytes(data[78:80], byteorder='little'), int.from_bytes(data[80:82], byteorder='little'), int.from_bytes(data[82:84], byteorder='little'), int.from_bytes(data[84:86], byteorder='little')]
        return bmsState(version_h, version_l, bms_status, SOC, current, cycle, BQ_NTC, MCU_NTC, cell_vol)


    def dataToImu(self, data):
        quaternion = [hex_to_float(data[0:4]), hex_to_float(data[4:8]), hex_to_float(data[8:12]), hex_to_float(data[12:16])]
        gyroscope = [hex_to_float(data[16:20]), hex_to_float(data[20:24]), hex_to_float(data[24:28])]
        accelerometer = [hex_to_float(data[28:32]), hex_to_float(data[32:36]), hex_to_float(data[36:40])]
        rpy = [hex_to_float(data[40:44]), hex_to_float(data[44:48]), hex_to_float(data[48:52])]
        temperature = data[52]
        return imu(quaternion, gyroscope, accelerometer, rpy, temperature)

    def dataToMotorState(self, data):
        mode = data[0]
        q = hex_to_float(data[1:5])
        dq = hex_to_float(data[5:9])
        ddq = hex_to_float(data[9:13])
        tauEst = hex_to_float(data[13:17])
        q_raw = hex_to_float(data[17:21])
        dq_raw = hex_to_float(data[21:25])
        ddq_raw = hex_to_float(data[25:29])
        temperature = data[29]
        reserve = [int.from_bytes(data[30:34], byteorder='little', signed=False), int.from_bytes(data[34:38], byteorder='little', signed=False)]
        return motorState(mode, q, dq, ddq, tauEst, q_raw, dq_raw, ddq_raw, temperature, reserve)

    def parseData(self, data):
        self.head = hex(int.from_bytes(data[0:2], byteorder='little'))
        self.levelFlag = data[2]
        self.frameReserve = data[3]
        self.SN = data[4:12]
        self.version = data[12:20]
        self.bandWidth = int.from_bytes(data[20:22], byteorder='little')
        self.imu = self.dataToImu(data[22:75])
        self.motorstate=[]
        for i in range(20):
            self.motorstate.append(self.dataToMotorState(data[(i*38)+75:(i*38)+38+75]))
        # FIX FROM HERE!!!
        self.bms=self.dataToBmsState(data[835:921])
        self.footForce = [int.from_bytes(data[921:923], byteorder='little'), int.from_bytes(data[923:925], byteorder='little'), int.from_bytes(data[925:927], byteorder='little'), int.from_bytes(data[927:929], byteorder='little')]
        self.footForceEst = [int.from_bytes(data[929:931], byteorder='little'), int.from_bytes(data[931:933], byteorder='little'), int.from_bytes(data[933:935], byteorder='little'), int.from_bytes(data[935:937], byteorder='little')]
        self.mode = data[937]
        self.progress = hex_to_float(data[938:942])
        self.gaitType = data[942]
        self.footRaiseHeight = hex_to_float(data[943:947])
        self.position = [hex_to_float(data[947:951]), hex_to_float(data[951:955]), hex_to_float(data[955:959])]
        self.bodyHeight = hex_to_float(data[959:963])
        self.velocity = [hex_to_float(data[963:967]), hex_to_float(data[967:971]), hex_to_float(data[971:975])]
        self.yawSpeed = hex_to_float(data[975:979])
        self.rangeObstacle = [hex_to_float(data[979:983]), hex_to_float(data[983:987]), hex_to_float(data[987:991]), hex_to_float(data[991:995])]
        self.footPosition2Body = []
        for i in range(4):
            self.footPosition2Body.append(cartesian(hex_to_float(data[(i*12)+995:(i*12)+999]), hex_to_float(data[(i*12)+999:(i*12)+1003]), hex_to_float(data[(i*12)+1003:(i*12)+1007])))
        self.footSpeed2Body = []
        for i in range(4):
            self.footSpeed2Body.append(cartesian(hex_to_float(data[(i*12)+1043:(i*12)+1047]), hex_to_float(data[(i*12)+1047:(i*12)+1051]), hex_to_float(data[(i*12)+1051:(i*12)+1055])))
        self.wirelessRemote = data[1091:1131]
        self.reserve = data[1131:1135]
        self.crc = data[1135:1139]
