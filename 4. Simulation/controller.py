class PIDcontroller():
    def __init__(self):
        self.P = 1
        self.I = 0
        self.D = 0
        
    def compute(self, pointsList, xb, yb):
        if (not pointsList[0]) and (xb >= -0.08) :
            error = -(yb-0)
            return 0, self.P*error
        elif (not pointsList[1]) and (yb >=-0.04):
            error = -(xb+0.08)
            return self.P*error, 0
        elif (not pointsList[2]) and (xb <=0.08):
            error = -(yb+0.04)
            return 0, self.P*error
        elif (not pointsList[3]) and  (yb >=-0.08):
            error = -(xb-0.08)
            return self.P*error, 0
        elif (not pointsList[4]) and (xb >=-0.08):
            error = -(yb+0.08)
            return 0, self.P*error
        else:
            return 0,0