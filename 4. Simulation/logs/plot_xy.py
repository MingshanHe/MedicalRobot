import numpy as np
import matplotlib.pyplot as plt

# Initialize lists to store x and y values
x_values = []
y_values = []

# Open and read the file line by line
with open('/home/biorobotics/IsaacGym_Tutorial/logs/2024-06-05.17:36:14/transitions/base_transition.txt', 'r') as file:
    for line in file:
        x, y = map(float, line.strip().split(','))
        x_values.append(x)
        y_values.append(y)

plt.scatter(x_values, y_values, color='blue',label='Base Traj')

x_values = []
y_values = []

# Open and read the file line by line
with open('/home/biorobotics/IsaacGym_Tutorial/logs/2024-06-05.17:36:14/transitions/tip_transition.txt', 'r') as file:
    for line in file:
        x, y = map(float, line.strip().split(','))
        x_values.append(x)
        y_values.append(y)

plt.scatter(x_values, y_values, color='red',label='Tip Traj')
# Adding labels and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Scatter Plot of (x, y)')
plt.legend()
# Show the plot
plt.grid(True)
plt.show()
