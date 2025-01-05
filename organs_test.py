import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def create_ellipsoid(center, radii, resolution=50):
    """Generates points for an ellipsoid."""
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    x = radii[0] * np.outer(np.cos(u), np.sin(v)) + center[0]
    y = radii[1] * np.outer(np.sin(u), np.sin(v)) + center[1]
    z = radii[2] * np.outer(np.ones_like(u), np.cos(v)) + center[2]
    return x, y, z

def plot_brain(ax):
    """Approximates a brain using overlapping ellipsoids."""
    radii1 = [1.2, 1, 1.2]  # Left hemisphere
    radii2 = [1.2, 1, 1.2]  # Right hemisphere
    x1, y1, z1 = create_ellipsoid([-0.8, 0, 0], radii1)
    x2, y2, z2 = create_ellipsoid([0.8, 0, 0], radii2)
    ax.plot_surface(x1, y1, z1, color='pink', alpha=0.7)
    ax.plot_surface(x2, y2, z2, color='pink', alpha=0.7)

def plot_lungs(ax):
    """Approximates lungs using two ellipsoids."""
    radii1 = [0.9, 1.2, 1.5]  # Left lung
    radii2 = [0.9, 1.2, 1.5]  # Right lung
    x1, y1, z1 = create_ellipsoid([-1.2, 0, 0], radii1)
    x2, y2, z2 = create_ellipsoid([1.2, 0, 0], radii2)
    ax.plot_surface(x1, y1, z1, color='lightblue', alpha=0.7)
    ax.plot_surface(x2, y2, z2, color='lightblue', alpha=0.7)

def plot_liver(ax):
    """Approximates the liver using a single flattened ellipsoid."""
    radii = [2, 1.2, 0.8]  # Ellipsoid dimensions
    x, y, z = create_ellipsoid([0, -1.5, 0], radii)
    ax.plot_surface(x, y, z, color='brown', alpha=0.7)

# Create a 3D plot
fig = plt.figure(figsize=(18, 6))

# Brain
ax1 = fig.add_subplot(131, projection='3d')
plot_brain(ax1)
ax1.set_title("Brain")
ax1.set_box_aspect([1, 1, 1])  # Equal aspect ratio

# Lungs
ax2 = fig.add_subplot(132, projection='3d')
plot_lungs(ax2)
ax2.set_title("Lungs")
ax2.set_box_aspect([1, 1, 1])  # Equal aspect ratio

# Liver
ax3 = fig.add_subplot(133, projection='3d')
plot_liver(ax3)
ax3.set_title("Liver")
ax3.set_box_aspect([1, 1, 1])  # Equal aspect ratio

# Show plots
plt.tight_layout()
plt.show()
