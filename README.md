# 2024 Spring Medical Robot Project
![Project Overview](https://github.com/dn0908/24-1_MedicalRobotProject/assets/94898107/eac5be34-a4ea-4aff-9291-83d0139e3387)

  
## Project Description

Reducing a surgeon’s tremor is crucial for improving surgical outcomes and decreasing operative time. Traditional robotic systems enhance accuracy but have limitations like large range of motion and high inertia. Our project aims to develop a lightweight, handheld surgical robot to mitigate these issues.

### Approach:
1. **Manipulator Design:** 
   - 2 DOF CDPR(Cable-driven Parallel Robot) actuator.
   - Flexible transmission.

2. **Control System:** 
   - Feedback control loop with IMU sensor.
   - IMU for tremor record, data sent for manipulator control.
    
3. **Simulation:** 
   - Simulation for...


  
## 1. Hardware

### Components
![Device Setup](https://github.com/dn0908/24-1_MedicalRobotProject/assets/94898107/76d03af7-3476-41e7-9ba6-e97054d1a286)


| Component    | Description                                                                                       |
|--------------|---------------------------------------------------------------------------------------------------|
| **Sensor**   | 6-axis IMU (accelerometers & gyroscopes)                                                          |
| **Actuation**| Dynamixel XL330-M288-T <br> Bowden-cable transmission <br> (sheath : incompressible extension spring, liner : teflon tube, cable : braided Dyneema) |
| **Parts**    | 3D printed parts  

  
## 2. Firmware
This section provides an overview of the firmware used to control the actuators with IMU data.
![image](https://github.com/dn0908/24-1_MedicalRobotProject/assets/94898107/c038872f-b11c-475c-882e-7445bb3f8efd)



### Features
- **Control Code:** Developed using Dynamixel SDK (Python) and MPU 6050 + Arduino nano for serial communication.
- **Motion Analysis:** Utilizes accelerometer data for detailed motion analysis.
- **PID Control:** Implements PID control algorithms for precise actuation.

### Code Overview

```python
# Sample code snippet
import dynamixel_sdk as dxl
import serial

# Initialize serial communication for IMU
ser = serial.Serial('/dev/COM11', 9600)

# Initialize Dynamixel SDK
port_num = dxl.PortHandler('/dev/ttyCOM12')
packet_handler = dxl.PacketHandler(1.0)
```

  
## 3. Simulation
    Vision
