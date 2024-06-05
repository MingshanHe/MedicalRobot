import numpy as np
import matplotlib.pyplot as plt

# Initialize lists to store the errors
error1 = []
error2 = []

# Read the file and store the values in the lists
with open('/home/biorobotics/IsaacGym_Tutorial/logs/2024-06-05.17:36:14/transitions/error.txt', 'r') as file:
    for line in file:
        e1, e2 = map(float, line.strip().split(','))
        error1.append(e1)
        error2.append(e2)


# Create a list of indices for the x-axis
indices = list(range(len(error1)))

# Plot the data as a scatter plot
plt.figure(figsize=(10, 6))

plt.scatter(indices, error1, marker='o', linestyle='-', color='blue', label='Error 1: Base to Desired Traj')
plt.scatter(indices, error2, marker='x', linestyle='-', color='red', label='Error 2: Tip Compensate to Desired Traj')

# Adding labels and title
plt.xlabel('Index')
plt.ylabel('Error Value')
plt.title('Error Values Over Time')
plt.legend()

# Show the plot
plt.grid(True)
plt.show()