from actuator import *
from motor import *

class X_LineActuator(Actuator):
    def __init__(self, _PORT1_, _BAUDRATE1_, _MOTOR_ID1_, _MODE1_, _CURRENT_LIMIT1_, _PORT2_, _BAUDRATE2_, _MOTOR_ID2_, _MODE2_, _CURRENT_LIMIT2_):
        super().__init__(_PORT1_, _BAUDRATE1_, _MOTOR_ID1_, _MODE1_, _CURRENT_LIMIT1_, _PORT2_, _BAUDRATE2_, _MOTOR_ID2_, _MODE2_, _CURRENT_LIMIT2_)

    def calibration(self, c1, c2):
        p1, p2 = Actuator.calibration(self, c1, c2)
        return p1, p2
    
    def move(self, p1, p2):
        Actuator.move(self, p1, p2)
        
class Y_LineActuator(Actuator):
    def __init__(self, _PORT1_, _BAUDRATE1_, _MOTOR_ID1_, _MODE1_, _CURRENT_LIMIT1_, _PORT2_, _BAUDRATE2_, _MOTOR_ID2_, _MODE2_, _CURRENT_LIMIT2_):
        super().__init__(_PORT1_, _BAUDRATE1_, _MOTOR_ID1_, _MODE1_, _CURRENT_LIMIT1_, _PORT2_, _BAUDRATE2_, _MOTOR_ID2_, _MODE2_, _CURRENT_LIMIT2_)
        
    def calibration(self, c1, c2):
        p1, p2 = Actuator.calibration(self, c1, c2)
        return p1, p2
    def move(self, p1, p2):
        Actuator.move(self, p1, p2)