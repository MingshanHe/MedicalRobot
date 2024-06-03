from controller import *
from threading import Thread
import os 
import time

class 
    def initControllers():
    my_car = controller("COM7",57600,1,"CURRENT-BASED-POSITION",80,"COM7",57600,2,"CURRENT-BASED-POSITION",80)
def main():
    # XActuator("COM7",57600,1,"CURRENT-BASED-POSITION",80,"COM7",57600,2,"CURRENT-BASED-POSITION",80)
    # XActuator.initParams()

    my_car = controller("COM7",57600,1,"CURRENT-BASED-POSITION",80,"COM7",57600,2,"CURRENT-BASED-POSITION",80)
    my_car.move_T(2000,1000)

    # t1.end()
if __name__ == "__main__":
    main()