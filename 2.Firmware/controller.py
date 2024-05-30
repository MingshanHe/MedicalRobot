from motor import Motor
class XController():
    def __init__(self, _PORT1_, _BAUDRATE1_, _MOTOR_ID1_, _MODE1_, _CURRENT_LIMIT1_, 
                        _PORT2_, _BAUDRATE2_, _MOTOR_ID2_, _MODE2_, _CURRENT_LIMIT2_):
        self.Motor1 = Motor(_PORT1_, _BAUDRATE1_, _MOTOR_ID1_, _MODE1_, _CURRENT_LIMIT1_)
        self.Motor2 = Motor(_PORT2_, _BAUDRATE2_, _MOTOR_ID2_, _MODE2_, _CURRENT_LIMIT2_)
    def move(self,p1, p2):
        
        self.Motor1.currentPosition()
        print(self.Motor1.POSITION)
        p1 - self.Motor1.POSTION
        self.Motor1.moveCurrentbasedPosition(Motor1.POSITION+2000)
        Motor2.currentPosition()
        print(Motor2.POSITION)
        Motor2.moveCurrentbasedPosition(Motor2.POSITION+2000)