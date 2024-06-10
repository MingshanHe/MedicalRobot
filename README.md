# 2024 Spring Medical Robot Project
<img src="5. Images/0_Device_Overview.png" alt="Project Overview" style="zoom:100%;" />




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
<img src="5. Images/1_Hardware_Setup.png" alt="Device Setup" style="zoom:100%;" />


| Component    | Description                                                                                       |
|--------------|---------------------------------------------------------------------------------------------------|
| **Sensor**   | 6-axis IMU (accelerometers & gyroscopes)                                                          |
| **Actuation**| Dynamixel XL330-M288-T <br> Bowden-cable transmission <br> (sheath : incompressible extension spring, liner : teflon tube, cable : braided Dyneema) |
| **Parts**    | 3D printed parts  


## 2. Firmware
This section provides an overview of the firmware used to control the actuators with IMU data.
![image](5. Images/2_Control_Diagram.png)



### Features
- **Control Code:** Developed using Dynamixel SDK (Python) and MPU 6050 + Arduino nano for serial communication.
- **Motion Analysis:** Utilizes accelerometer data for detailed motion analysis.
- **PID Control:** Implements PID control algorithms for precise actuation.

### Code Overview

```python
# To be updated

```


## 3. Simulation
This section involves simulating the device using the [Isaac Gym](https://developer.nvidia.com/isaac-gym) physics simulation engine by NVIDIA. The simulation allows the use of different control methods, including PID control, Reinforcement Learning (RL), and a Manifold-based control method.
### Scenario
The tremor cancellor robot were imported with URDF format file, and prismatic joints were added in base coordinate and tip coordinate. The gaussian noised movement of base coordinate simulated the hand tremor of human. And tip trajectory compensated the noise and hold the centor of tip within the desired trajectory.

### Control Method
#### 1) PID Control

$u(t) = K_pe(t)+K_i\int e(t)dt+K_p\frac{de}{dt}$

#### 2) Reinforcement Learning (Deep Q-Network) Control

<img src="5. Images/3_DQN.jpeg" alt="DQN" style="zoom:50%;" />

#### 3) Manifold-Based Control

<img src="5. Images/4_Manifold.png" alt="Manifold" style="zoom: 5%;" />

### Initialization
To initialize the simulation, create an instance of the Cancellor class. You need to specify whether to save data, which control method to use, and additional arguments if using RL.
```python
from cancellor import Cancellor
from argparse import Namespace

args = Namespace(num_envs=1, sim_device='cpu')
cancellor = Cancellor(_save_data_=True, _method_='RL', args=args)
```
### Running the simulation
The loopfunc method starts the simulation loop. If _save_data_ is set to True, the simulation data will be logged using the Logger class. The data includes base trajectory, tip trajectory, and error trajectory, which are saved in the logs directory. 
```bash
pip install requirement.txt
```

```bash
python main.py
```

