from lineactuator import *
from threading import Thread
import os 
import time
from loguru import logger
import math

class Controller:
    def __init__(self) -> None:
        logger.add(os.getcwd()  + '\\test.log')
        logger.info('Initialization Two Line Actuators: X_controller and Y_controller')
        self.X_controller = X_LineActuator("COM12",57600,1,"CURRENT-BASED-POSITION",80,"COM12",57600,2,"CURRENT-BASED-POSITION",80)
        self.Y_controller = Y_LineActuator("COM12",57600,0,"CURRENT-BASED-POSITION",80,"COM12",57600,3,"CURRENT-BASED-POSITION",80)
        self.X = None
        self.Y = None
        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.p4 = None
    
    def calibration(self):
        current = 50
        p1, p2 = self.X_controller.calibration(-current,-current) # 25 desired
        p3, p4 = self.Y_controller.calibration(current,current)
        logger.info(f"Calibration Result: X_controller Initial Position ({p1}, {p2}); Y_controller Initial Position ({p3},{p4})")
        logger.info(f"Calibration Finished")
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.X = 0
        self.Y = 0
        
    def move(self, x, y):
        # TODO: x, y => P1, P2, P3, P4
        theta = math.atan2(y, x)
        r = math.sqrt(x**2 + y**2)           
        xy_2_m = 4096/(2*math.pi*2.84)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        p1 = self.p1 - r*math.cos(theta)*xy_2_m
        p2 = self.p2 + r*math.cos(theta)*xy_2_m

        p3 = self.p3 + r*math.sin(theta)*xy_2_m
        p4 = self.p4 - r*math.sin(theta)*xy_2_m
        
        self.X_controller.move(int(p1), int(p2))
        self.Y_controller.move(int(p3), int(p4))
        # self.X_controller.move(0,0)

    def disable(self):
        self.X_controller.disable()
        self.Y_controller.disable()
       
def main():
    controller = Controller()
    controller.calibration()
    controller.move(4,4)
    time.sleep(1)
    controller.move(-2,-2)
    time.sleep(1)
    controller.move(0,0)
    controller.disable()
if __name__ == "__main__":
    main()