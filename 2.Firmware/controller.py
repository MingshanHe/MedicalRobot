from motor import Motor
class XController:
    def __init__(self, _PORT1_, _BAUDRATE1_, _MOTOR_ID1_, _MODE1_, _CURRENT_LIMIT1_, 
                        _PORT2_, _BAUDRATE2_, _MOTOR_ID2_, _MODE2_, _CURRENT_LIMIT2_):
        
        self.Motor1 = Motor(_PORT1_, _BAUDRATE1_, _MOTOR_ID1_, _MODE1_, _CURRENT_LIMIT1_)
        self.Motor2 = Motor(_PORT2_, _BAUDRATE2_, _MOTOR_ID2_, _MODE2_, _CURRENT_LIMIT2_)
    def movet(self):
        self.Motor2.moveCurrentbasedPosition(self.Motor2.POSITION+2000)
    def move(self, p1, p2):
        
        self.Motor1.currentPosition()
        print(self.Motor1.POSITION)
        # p1 = self.Motor1.POSITION
        # int((p1 - self.Motor1.POSTION)/100)
        self.Motor2.currentPosition()
        print(self.Motor2.POSITION)
        # p2 = self.Motor2.POSITION
        # int((p2 - self.Motor2.POSITION)/100)
        
        while abs(p1 - self.Motor1.POSTION) < 2 & abs(p2 - self.Motor2.POSITION) < 2:
            
            self.Motor1.moveCurrentbasedPosition(self.Motor1.POSITION+int((p1 - self.Motor1.POSTION)/100))
            self.Motor2.moveCurrentbasedPosition(self.Motor2.POSITION+int((p2 - self.Motor2.POSTION)/100))
            self.Motor1.currentPosition()
            self.Motor2.currentPosition()
        # Motor2.moveCurrentbasedPosition(Motor2.POSITION+2000)