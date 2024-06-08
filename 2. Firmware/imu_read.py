import serial
import time

def read_imu_data(controller, port='/dev/COM11', baudrate=57600):
    ser = serial.Serial(port, baudrate)
    time.sleep(2)  # wait for connection
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()

            print(line)

            try:
                parts = line.split()
                ax = float(parts[1])
                ay = float(parts[3])
                az = float(parts[5])
                print(f'aX: {ax}, aY: {ay}, aZ: {az}')
                controller.control_motors(ax, ay)
                
            except Exception as e:
                print("Error parsing:", line, e)