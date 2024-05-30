from Motor import *
from threading import Thread
import os 
import time


    

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

MOTOR1 = Motor(1,"CURRENT-BASED-POSITION",80)
MOTOR2 = Motor(2,"CURRENT-BASED-POSITION",80)


SaveDataFlag = True
dt = 10

def Grasp_Position(goalposition1, goalposition2):
    dx1_present_position = MOTOR1.currentPosition()
    dx2_present_position = MOTOR1.currentPosition()
    
    MOTOR1.movePosition(goalposition1)
    MOTOR2.movePosition(goalposition2)  
    
def Grasp():
    # Grasp_Position_L = 6000
    # Grasp_Position_R = 6000
    Grasp_Position_L = 5000
    Grasp_Position_R = 6000
    MOTOR1.movePosition(Grasp_Position_L)
    MOTOR2.movePosition(Grasp_Position_R)  
    SaveData()

def SaveData():
    start_time = time.time()
    while (time.time() - start_time)<dt:
        MOTOR1.currentCurrent()
        MOTOR1.currentPosition()
        MOTOR1.currentVelocity()
        MOTOR2.currentCurrent()
        MOTOR2.currentPosition()
        MOTOR2.currentVelocity()
        MOTOR1.saveData()
        MOTOR2.saveData()

    
def main():
    while 1:
        print("PressCommand:")
        cmd = getch()
        print(cmd)
        if(cmd == 'Q'):
            MOTOR1.TorqueDisable()
            MOTOR2.TorqueDisable()
            break
        elif(cmd == '1'):
            # global SaveDataFlag
            # SaveDataFlag= False
            # p1 = MOTOR1.currentPosition()
            # p2 = MOTOR2.currentPosition()
            # print("now:" ,p1,p2)  
            Grasp()
            
        elif(cmd == '2'):
            p1 = MOTOR1.currentPosition()
            p2 = MOTOR2.currentPosition()
            Grasp()


    # t1.end()
if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
# i = 1000
# while (i>0):
#     # CURRENT MODE
    
#     # MOTOR1.moveCurrent(100)
#     # MOTOR2.moveCurrent(100)
#     # MOTOR1.currentCurrent()
#     # MOTOR2.currentCurrent()
#     # MOTOR1.currentPosition()
#     # MOTOR2.currentPosition()
    
#     # VELOCITY MODE
    
#     # MOTOR1.moveVelocity(10)
#     # MOTOR2.moveVelocity(10)
#     # MOTOR1.currentCurrent()
#     # MOTOR1.currentVelocity()
#     # MOTOR1.currentPosition()
#     # MOTOR2.currentCurrent()
#     # MOTOR2.currentVelocity()
#     # MOTOR2.currentPosition()
    
#     # CURRENT-BASED POSITION MODE
#     MOTOR1.moveCurrentbasedPosition(100)
#     MOTOR2.moveCurrentbasedPosition(100)
    
    
    
#     MOTOR1.saveData()
#     MOTOR2.saveData()
#     i=i-1
# MOTOR1.TorqueDisable()
# MOTOR2.TorqueDisable()

# MOTOR1.changeMode("POSITION")
# MOTOR2.changeMode("POSITION")    
# MOTOR1.TorqueEnable()
# MOTOR2.TorqueEnable()
# position1 =  MOTOR1.currentPosition()
# position2 =  MOTOR2.currentPosition()

# i = 1000
# while (i>0):
#     # CURRENT MODE
#     # MOTOR1.moveCurrent(50)
#     # MOTOR2.moveCurrent(50)
#     # MOTOR1.currentCurrent()
#     # MOTOR2.currentCurrent()
#     # VELOCITY MODE
#     # MOTOR1.moveVelocity(10)
#     # MOTOR2.moveVelocity(10)
#     # MOTOR1.currentCurrent()
#     # MOTOR1.currentVelocity()
#     # MOTOR1.currentPosition()
#     # MOTOR2.currentCurrent()
#     # MOTOR2.currentVelocity()
#     # MOTOR2.currentPosition()
#     #POSITION

#     MOTOR1.movePosition(position1)
#     MOTOR2.movePosition(position2)
    
#     MOTOR1.saveData()
#     MOTOR2.saveData()
#     i=i-1 
    
# MOTOR1.currentPosition()
# MOTOR2.currentPosition()


# MOTOR1.TorqueDisable()
# MOTOR2.TorqueDisable()