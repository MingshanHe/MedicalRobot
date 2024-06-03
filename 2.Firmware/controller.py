from actuator import *
from motor import *

class controller(Actuator):
    def __init__(self, _PORT1_, _BAUDRATE1_, _MOTOR_ID1_, _MODE1_, _CURRENT_LIMIT1_, _PORT2_, _BAUDRATE2_, _MOTOR_ID2_, _MODE2_, _CURRENT_LIMIT2_):
        super().__init__(_PORT1_, _BAUDRATE1_, _MOTOR_ID1_, _MODE1_, _CURRENT_LIMIT1_, _PORT2_, _BAUDRATE2_, _MOTOR_ID2_, _MODE2_, _CURRENT_LIMIT2_)