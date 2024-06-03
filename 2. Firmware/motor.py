from dynamixel_sdk import * # Uses Dynamixel SDK library
import csv
import os

PROTOCOL_VERSION            = 2.0     
BAUDRATE                    = 57600
PORT                        = 'COM12'
 
# Initialize PortHandler instance
portHandler = PortHandler(PORT)
# Initialize PacketHandler instance
packetHandler = PacketHandler(PROTOCOL_VERSION)
# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()
# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()


class Motor:
    
    def __init__(self, _PORT_, _BAUDRATE_, _MOTOR_ID_, _MODE_, _CURRENT_LIMIT_):

        self.PORT = _PORT_
        self.BAUDRATE = _BAUDRATE_
        self.MOTOR_ID = _MOTOR_ID_
        self.MODE = _MODE_
        self.CURRENT_LIMIT = _CURRENT_LIMIT_

        
        self.initParams()

        # Define Dynamixel Mode
        result, error = self.write(1, self.ADDR_PRO_OPERATING_MODE, self.MODEdic[self.MODE])
        if error==0:
            print("[MOTOR ID: %03d]: Operating mode changed." %(self.MOTOR_ID))
        # Enable Dynamixel Torque
        result, error = self.write(1, self.ADDR_PRO_TORQUE_ENABLE, 1)
        if error==0:
            print("[MOTOR ID: %03d]: Motor has been successfully enabled."%(self.MOTOR_ID))
            
    def initParams(self):
        # Control table address
        self.ADDR_PRO_TORQUE_ENABLE      = 64               
        self.ADDR_PRO_OPERATING_MODE     = 11
        self.ADDR_PRO_GOAL_POSITION      = 116
        self.ADDR_PRO_PRESENT_POSITION   = 132
        self.ADDR_PRO_GOAL_CURRENT       = 102
        self.ADDR_PRO_PRESENT_CURRENT    = 126
        self.ADDR_PRO_GOAL_VELOCITY      = 104
        self.ADDR_PRO_PRESENT_VELOCITY   = 128
        # Mode
        self.MODEdic = {"CURRENT": 0, "VELOCITY": 1, "POSITION": 3, "EXTENDED-POSITION": 4,"CURRENT-BASED-POSITION": 5}
        # Params
        self.CURRENT = 0
        self.POSITION = 0
        self.VELOCITY = 0


    def changeMode(self, _MODE_):
        self.TorqueDisable()
        result, error = self.write(1, self.ADDR_PRO_OPERATING_MODE, self.MODEdic[_MODE_])
        if error==0:
            print("[MOTOR ID: %03d]: Operating mode changed." %(self.MOTOR_ID))
        self.TorqueEnable()
            
    def read(self, _byte_, _addr_):
        if _byte_ == 1:
            data, result, error = packetHandler.read1ByteTxRx(portHandler, self.MOTOR_ID, _addr_)
        elif _byte_ == 4:
            data, result, error = packetHandler.read4ByteTxRx(portHandler, self.MOTOR_ID, _addr_)
        if result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(result))
        elif error != 0:
            print("%s" % packetHandler.getRxPacketError(error))
        return data, result, error

    def write(self, _byte_, _addr_, _value_):
        if _byte_ == 1:
            result, error = packetHandler.write1ByteTxRx(portHandler, self.MOTOR_ID, _addr_, _value_)
        elif _byte_ == 2:
            result, error = packetHandler.write2ByteTxRx(portHandler, self.MOTOR_ID, _addr_, _value_)
        elif _byte_ == 4:
            result, error = packetHandler.write4ByteTxRx(portHandler, self.MOTOR_ID, _addr_, _value_)
        if result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(result))
        elif error != 0:
            print("%s" % packetHandler.getRxPacketError(error))
        return result, error

    def currentPosition(self):
        position, result, error = self.read(4, self.ADDR_PRO_PRESENT_POSITION)
        if position > 2147483647:
                position = position - 4294967296
        self.POSITION = position
        return self.POSITION

    def currentCurrent(self):
        current, result, error = self.read(4, self.ADDR_PRO_PRESENT_CURRENT)
        self.CURRENT = current
        return self.CURRENT

    def currentVelocity(self):
        velocity, dx_comm_result, dx_error = self.read(4, self.ADDR_PRO_PRESENT_VELOCITY)
        self.VELOCITY = velocity
        return self.VELOCITY

    def movePosition(self,position):
        result, error = self.write(4, self.ADDR_PRO_GOAL_POSITION, position)
            
    def moveCurrent(self,current):
        result, error = self.write(2, self.ADDR_PRO_GOAL_CURRENT, current)

    def moveVelocity(self,velocity):
        result, error = self.write(4, self.ADDR_PRO_GOAL_VELOCITY, velocity)

    def TorqueEnable(self):
        result, error = self.write(1, self.ADDR_PRO_TORQUE_ENABLE, 1)
        print("[MOTOR ID: %03d]: Torque Enabled" % (self.MOTOR_ID))

    def TorqueDisable(self):
        result, error = self.write(1, self.ADDR_PRO_TORQUE_ENABLE, 0)
        print("[MOTOR ID: %03d]: Torque Disabled" % (self.MOTOR_ID))