from dynamixel_sdk import * # Uses Dynamixel SDK library
import csv
import os

# Control table address
ADDR_PRO_TORQUE_ENABLE      = 64               
ADDR_PRO_OPERATING_MODE     = 11
ADDR_PRO_GOAL_POSITION      = 116
ADDR_PRO_PRESENT_POSITION   = 132
ADDR_PRO_GOAL_CURRENT       = 102
ADDR_PRO_PRESENT_CURRENT    = 126
ADDR_PRO_GOAL_VELOCITY      = 104
ADDR_PRO_PRESENT_VELOCITY   = 128
# Protocol version
PROTOCOL_VERSION            = 2.0     
# Default setting
BAUDRATE                    = 57600
DEVICENAME                  = 'COM7'
TORQUE_ENABLE               = 1
TORQUE_DISABLE              = 0            
DXL_MINIMUM_CURRENT_VALUE  = 100         
DXL_MAXIMUM_CURRENT_VALUE  = -100          
DXL_MOVING_STATUS_THRESHOLD = 1     
 



# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)

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
        self.CURRENT = 0
        self.POSITION = 0
        self.VELOCITY = 0

        self.MODEdic = {"CURRENT": 0, "POSITION": 3, "CURRENT-BASED-POSITION": 5, "VELOCITY": 1}
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, self.MOTOR_ID, ADDR_PRO_OPERATING_MODE, self.MODEdic[self.MODE])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("[MOTOR ID: %03d]: Operating mode changed to current control mode." %(self.MOTOR_ID))

        # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, self.MOTOR_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel has been successfully connected")

    def changeMode(self, MODE):
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, self.MOTOR_ID, ADDR_PRO_OPERATING_MODE, self.MODEdic[MODE])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("[MOTOR ID: %03d]: Operating mode changed to current control mode." %(self.MOTOR_ID))
    def read(self, _byte_, _addr_):
        if _byte_ == 1:
        #     data, dx_comm_result, dx_error = packetHandler.read1ByteTxRx(portHandler, self.MOTOR_ID, 132)
        # elif _byte_ == 4:
        data, dx_comm_result, dx_error = packetHandler.read4ByteTxRx(portHandler, self.MOTOR_ID, _addr_)
        return data, dx_comm_result, dx_error
    def write(self, _byte_, _addr_):
        if 
    def currentPosition(self):
        dx_present_position, dx_comm_result, dx_error = packetHandler.read4ByteTxRx(portHandler, self.MOTOR_ID, 132) # 132 : present position
        if dx_present_position > 2147483647:
                dx_present_position = dx_present_position - 4294967296
        if dx_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dx_comm_result))
        elif dx_error != 0:
            print("%s" % packetHandler.getRxPacketError(dx_error))

        # Read present position
        dx_position_before = dx_present_position
        
        dx_present_position, dx_comm_result, dx_error = packetHandler.read4ByteTxRx(portHandler, self.MOTOR_ID, 132) # 132 : present position
        if dx_present_position > 2147483647:
            dx_present_position = dx_present_position - 4294967296
        if dx_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dx_comm_result))
        elif dx_error != 0:
            print("%s" % packetHandler.getRxPacketError(dx_error))

        dx_position_after = dx_present_position
        # print("[MOTOR ID: %03d]: Present Position: %d." % (self.MOTOR_ID, dx_present_position))
        self.POSITION = dx_present_position
        return dx_present_position

    def currentCurrent(self):
        dx_present_current, dx_comm_result, dx_error = packetHandler.read4ByteTxRx(portHandler, self.MOTOR_ID, ADDR_PRO_PRESENT_CURRENT) # 132 : present position
        if dx_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dx_comm_result))
        elif dx_error != 0:
            print("%s" % packetHandler.getRxPacketError(dx_error))
        # print("[MOTOR ID: %03d]: Present Current: %d." % (self.MOTOR_ID, dx_present_current))
        self.CURRENT = dx_present_current
        return dx_present_current

    def currentVelocity(self):
        dx_present_velocity, dx_comm_result, dx_error = packetHandler.read4ByteTxRx(portHandler, self.MOTOR_ID, ADDR_PRO_PRESENT_VELOCITY) # 132 : present position
        if dx_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dx_comm_result))
        elif dx_error != 0:
            print("%s" % packetHandler.getRxPacketError(dx_error))
        # print("[MOTOR ID: %03d]: Present Current: %d." % (self.MOTOR_ID, dx_present_current))
        self.VELOCITY = dx_present_velocity
        return dx_present_velocity

    def moveCurrentbasedPosition(self, position):
        num1_dx2 = 0

        dx2_present_position = self.currentPosition()
        self.movePosition(position)

        while 1:
            # Read present position
            dx2_position_before = dx2_present_position
            dx2_present_position = self.currentPosition()
            dx2_position_after = dx2_present_position            
            
            print("[ID:%03d] DX2GoalPosition:%d DX2PresPosition:%d" % (self.MOTOR_ID, position, dx2_present_position))

            if abs(dx2_present_position-position) == 0:
                self.movePosition(dx2_present_position)
                break

            if abs(dx2_position_before - dx2_position_after) < 1:
                num1_dx2 += 1


            print("num1_dx : %d, before : %d, after : %d" % (num1_dx2, dx2_position_before, dx2_position_after))

            if num1_dx2 > 5:
                num1_dx2 = 0
                break
            

    def movePosition(self,position):
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, self.MOTOR_ID, ADDR_PRO_GOAL_POSITION, position)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
            
    def moveCurrent(self,current):
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, self.MOTOR_ID, ADDR_PRO_GOAL_CURRENT, current)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

    def moveVelocity(self,velocity):
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, self.MOTOR_ID, ADDR_PRO_GOAL_VELOCITY, velocity)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
                
                
    def TorqueEnable(self):
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, self.MOTOR_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("[MOTOR ID: %03d]: Torque Enabled" % (self.MOTOR_ID))

    def TorqueDisable(self):
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, self.MOTOR_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("[MOTOR ID: %03d]: Torque Disabled" % (self.MOTOR_ID))
            
            
            
    #Utilization
    def saveData(self):
        self.WRITER.writerow([self.CURRENT,self.VELOCITY, self.POSITION])