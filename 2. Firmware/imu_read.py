import serial
import time

def read_imu_data(port='COM11', baudrate=57600):
# def read_imu_data(controller, port='COM11', baudrate=57600):
    ser = serial.Serial(port, baudrate)
    time.sleep(2)

    last_x, last_y = 0, 0
    control_loop_frequency = 300  # Hz
    control_loop_period = 1.0 / control_loop_frequency

    while True:
        start_time = time.time()
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(line)  # For debugging
            try:
                parts = line.split(',')
                x = float(parts[0])
                y = float(parts[1])
                print(f'X: {x}, Y: {y}')

                dx = x - last_x
                dy = y - last_y
                print(f'dX: {dx}, dY: {dy}')

                # controller.control_motors(dx, dy)

                last_x, last_y = x, y
            except Exception as e:
                print("Error parsing:", line, e)

        elapsed_time = time.time() - start_time
        sleep_time = control_loop_period - elapsed_time
        if sleep_time > 0:
            time.sleep(sleep_time)

if __name__ == "__main__":
    read_imu_data(port='COM11', baudrate=57600)