import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameters for the organ (approximating it as an ellipsoid for simplicity)
a, b, c = 10, 7, 5  # axes lengths of the organ (e.g., lung, brain)

# Number of tumor points
n_points = 3000

# Simulate non-uniform tumor growth using spherical coordinates
theta = np.random.uniform(0, 2 * np.pi, n_points)
phi = np.random.uniform(0, np.pi, n_points)

# Radial growth pattern with varying growth rates
r = np.random.uniform(1, 3, n_points)  # Random radial distances (non-uniform)
r_growth = (r ** 2) * np.random.uniform(0.5, 1.5, n_points)  # Variable growth factor

# Spherical to Cartesian conversion
x = r_growth * np.sin(phi) * np.cos(theta)
y = r_growth * np.sin(phi) * np.sin(theta)
z = r_growth * np.cos(phi)

# Scale the tumor points to fit within the organ's boundary
x = x * a / np.max(np.abs(x))
y = y * b / np.max(np.abs(y))
z = z * c / np.max(np.abs(z))

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the tumor points with a bulging effect
ax.scatter(x, y, z, color='yellow', s=20, alpha=0.6)

# Set labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Set the viewing angle for better visualization of the 3D effect
ax.view_init(30, 30)

# Show plot
plt.show()
