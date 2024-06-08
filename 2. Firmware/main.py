from pid_controller import Controller
from imu_read import read_imu_data
from threading import Thread
import time

def main():
    controller = Controller()
    controller.calibration()
    imu_thread = Thread(target=read_imu_data, args=(controller,))
    imu_thread.start()

    control_loop_frequency = 300  # Hz
    control_loop_period = 1.0 / control_loop_frequency

    try:
        while True:
            start_time = time.time()
            
            elapsed_time = time.time() - start_time
            sleep_time = control_loop_period - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        controller.disable()
        imu_thread.join()

if __name__ == "__main__":
    main()