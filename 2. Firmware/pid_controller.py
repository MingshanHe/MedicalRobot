from lineactuator import *
import os
import math
import time
from loguru import logger

class PID:
    def __init__(self, kp, ki, kd, setpoint=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self._prev_error = 0
        self._integral = 0

    def compute(self, measurement):
        error = self.setpoint - measurement
        self._integral += error
        derivative = error - self._prev_error
        self._prev_error = error
        return self.kp * error + self.ki * self._integral + self.kd * derivative

class Controller:
    def __init__(self) -> None:
        logger.add(os.getcwd() + '\\test.log')
        logger.info('Initialization Two Line Actuators: X_controller and Y_controller')
        self.X_controller = X_LineActuator("COM12", 57600, 1, "CURRENT-BASED-POSITION", 80, "COM12", 57600, 2, "CURRENT-BASED-POSITION", 80)
        self.Y_controller = Y_LineActuator("COM12", 57600, 0, "CURRENT-BASED-POSITION", 80, "COM12", 57600, 3, "CURRENT-BASED-POSITION", 80)
        self.X = None
        self.Y = None
        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.p4 = None
        self.desired_position_x = 0.0
        self.desired_position_y = 0.0

        # PID controllers for X and Y axes
        self.pid_x = PID(kp=1.0, ki=0.05, kd=0.1)
        self.pid_y = PID(kp=1.0, ki=0.05, kd=0.1)

    def calibration(self):
        current = 50
        p1, p2 = self.X_controller.calibration(-current, -current)
        p3, p4 = self.Y_controller.calibration(current, current)
        logger.info(f"Calibration Result: X_controller Initial Position ({p1}, {p2}); Y_controller Initial Position ({p3}, {p4})")
        logger.info(f"Calibration Finished")
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.X = 0
        self.Y = 0

    def move(self, x, y):
        theta = math.atan2(y, x)
        r = math.sqrt(x**2 + y**2)
        xy_2_m = 4096 / (2 * math.pi * 2.84)
        p1 = self.p1 - r * math.cos(theta) * xy_2_m
        p2 = self.p2 + r * math.cos(theta) * xy_2_m
        p3 = self.p3 + r * math.sin(theta) * xy_2_m
        p4 = self.p4 - r * math.sin(theta) * xy_2_m

        self.X_controller.move(int(p1), int(p2))
        self.Y_controller.move(int(p3), int(p4))

    def disable(self):
        self.X_controller.disable()
        self.Y_controller.disable()

    def control_motors(self, ax, ay):
        control_signal_x = self.pid_x.compute(ax)
        control_signal_y = self.pid_y.compute(ay)
        self.move(control_signal_x, control_signal_y)
