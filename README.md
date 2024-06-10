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



# References

**[1]** Taylor, R., Jensen, P., Whitcomb, L., Barnes, A., Kumar, R., Stoianovici, D., ... & Kavoussi, L. (1999). A steady-hand robotic system for microsurgical augmentation. **The International Journal of Robotics Research**, *18*(12), 1201-1210.

**[2]** Roizenblatt, M., Edwards, T. L., & Gehlbach, P. L. (2018). Robot-assisted vitreoretinal surgery: current perspectives. **Robotic Surgery: Research and Reviews**, 1-11.

**[3]** Nasab, M. H. A. (Ed.). (2019). *Handbook of robotic and image-guided surgery*. Elsevier.

**[4]** Miller, J., Braun, M., Bilz, J., Matich, S., Neupert, C., Kunert, W., & Kirschniak, A. (2021). Impact of haptic feedback on applied intracorporeal forces using a novel surgical robotic system—a randomized cross-over study with novices in an experimental setup. **Surgical endoscopy**, *35*, 3554-3563.

**[5]** MacLachlan, R. A., Becker, B. C., Tabares, J. C., Podnar, G. W., Lobes, L. A., & Riviere, C. N. (2011). Micron: an actively stabilized handheld tool for microsurgery. **IEEE** **Transactions** **on** **Robotics**, *28*(1), 195-212.

**[6]** Yang, S., MacLachlan, R. A., & Riviere, C. N. (2014). Manipulator design and operation of a six-degree-of-freedom handheld tremor-canceling microsurgical instrument. **IEEE/ASME transactions on mechatronics**, *20*(2), 761-772.

**[7]** Zhang, T., Gong, L., Wang, S., & Zuo, S. (2020). Hand-held instrument with integrated parallel mechanism for active tremor compensation during microsurgery. **Annals of Biomedical Engineering**, *48*, 413-425.

**[8]** González-Rodríguez, A., Martín-Parra, A., Juárez-Pérez, S., Rodríguez-Rosa, D., Moya-Fernández, F., Castillo-García, F. J., & Rosado-Linares, J. (2023, May). Dynamic model of a novel planar cable driven parallel robot with a single cable loop. **Actuators** (Vol. 12, No. 5, p. 200). MDPI.

**[9]** W. J. E. Teskey, M. Elhabiby, and N. El-Sheimy, “Inertial sensing to determine movement disorder motion present before and after treatment”, **Sensors**, vol. *12, no.* 3, pp. 3512-3527, Mar., 2012, DOI: 10.3390/s120303512

**[10]** D. Lau, K. Bhalerao, D. Oetomo, and S. K. Halgamuge, "On the task specific evaluation and optimisation of cable-driven manipulators”, **Advances** **in reconfigurable mechanisms and** **robots***,* pp. 707-716, Springer London.

**[11]** J. Townsend, N. Koep, and S. Weichwald, “Pymanopt: A Python Toolbox for Optimization on Manifolds using Automatic Differentiation”, **Journal of Machine Learning Research**, vol. 17, no. 137, pp. 1-5, 2016, DOI: http://jmlr.org/papers/v17/16-177.html.

**[12]** V. Mnih, K. Kavukcuoglu, D. Silver, A. Graves, I. Antonoglou, D. Wierstra, and M. Riedmiller, “Playing Atari with Deep Reinforcement Learning”, **Arxiv**, Sep., 2012, DOI: 10.48550/arXiv.1312.5602.

**[13]** V. Mnih, K. Kavukcuoglu, D. Silver, A. A Rusu, J. Veness, M. G Bellemare, A. Graves, M. Riedmiller, A. K Fidjeland, G. Ostrovski, S. Petersen, C. Beattie, A. Sadik, I. Antonoglou, H. King, D. Kumaran, D. Wierstra, S. Legg, and D. Hassabis, “Human-level control through deep reinforcement learning”, **Nature**, vol. 518, no. 7540, pp. 529-533, Feb., 2015, DOI: 10.1038/nature14236.