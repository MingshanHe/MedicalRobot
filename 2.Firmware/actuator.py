from motor import Motor
import time
class Actuator:
    def __init__(self, _PORT1_, _BAUDRATE1_, _MOTOR_ID1_, _MODE1_, _CURRENT_LIMIT1_, _PORT2_, _BAUDRATE2_, _MOTOR_ID2_, _MODE2_, _CURRENT_LIMIT2_):
        self.Motor1 = Motor(_PORT1_, _BAUDRATE1_, _MOTOR_ID1_, _MODE1_, _CURRENT_LIMIT1_)
        self.Motor2 = Motor(_PORT2_, _BAUDRATE2_, _MOTOR_ID2_, _MODE2_, _CURRENT_LIMIT2_)
        # self.make = make
        # self.model = model
        # self.engine = Engine(horsepower)  # 在Car类中初始化Engine类
    def calibration(self, c1, c2):
        self.Motor1.changeMode("CURRENT")
        self.Motor2.changeMode("CURRENT")
        start_time = time.time()
        while time.time()-start_time < 3:
            self.Motor1.moveCurrent(c1)
            self.Motor2.moveCurrent(c2)
        p1 = self.Motor1.currentPosition()
        p2 = self.Motor2.currentPosition()
        return p1, p2
    
    def move(self, p1, p2):
        self.Motor1.changeMode("EXTENDED-POSITION")
        self.Motor2.changeMode("EXTENDED-POSITION")
        self.Motor1.movePosition(p1)
        self.Motor2.movePosition(p2)
        
        
    def move_T(self, p1_d, p2_d):
        
        self.Motor1.currentPosition()
        p1 = self.Motor1.POSITION
        self.Motor2.currentPosition()
        p2 = self.Motor2.POSITION
        print(p1_d - p1)
        print(p2_d - p2)
        # if abs(p1_d - p1)> abs(p2_d - p2):
        delta_d1 = int((p1_d - p1)/abs(p1_d - p1)* 5500)
        delta_d2  = int((p2_d - p2)/abs(p1_d - p1)*5500)
        # else:
        # delta_d1 = int((p1_d - p1)/abs(p2_d - p2)*100)
        # delta_d2  = int((p2_d - p2)/abs(p2_d - p2)*100)
        
        # while abs(p1 - p1_d) > 200 and abs(p2 - p2_d)>200:
            
        self.Motor1.movePosition(self.Motor1.POSITION+delta_d1)
        self.Motor2.movePosition(self.Motor2.POSITION+delta_d2)
        self.Motor1.POSITION = self.Motor1.POSITION + delta_d1
        self.Motor2.POSITION = self.Motor2.POSITION + delta_d2
          
