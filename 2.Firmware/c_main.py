from controller import *
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

# MOTOR1 = Motor("COM7",57600,1,"CURRENT-BASED-POSITION",80)
 
def main():
    XController("COM7",57600,1,"CURRENT-BASED-POSITION",80,"COM7",57600,2,"CURRENT-BASED-POSITION",80)
    while 1:
        print("PressCommand:")
        cmd = getch()
        print(cmd)
        if(cmd == 'Q'):
            MOTOR1.TorqueDisable()
            break
        elif(cmd == '1'):
            MOTOR1.moveCurrent(100)
            
        elif(cmd == '2'):
            MOTOR1.currentPosition()
            print(MOTOR1.POSITION)
        elif(cmd == '3'):
            MOTOR1.movePosition(2000)
            print(MOTOR1.POSITION)
        elif(cmd == '4'):
            MOTOR1.currentPosition()
            print(MOTOR1.POSITION)
            MOTOR1.moveCurrentbasedPosition(MOTOR1.POSITION+2000)


    # t1.end()
if __name__ == "__main__":
    main()