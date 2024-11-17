import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Parameters
N0 = 1e3  # Initial tumor size
K = 1e9   # Carrying capacity
r = 0.2   # Growth rate
time_steps = 100  # Total time steps

def logistic_growth(N0, r, K, t):
    return K / (1 + (K / N0 - 1) * np.exp(-r * t))

def gompertz_growth(N0, r, K, t):
    return K * np.exp(-np.exp(r * (np.log(K) - np.log(N0)) * np.exp(-r * t)))

time = np.linspace(0, 50, time_steps)
tumor_sizes_logistic = logistic_growth(N0, r, K, time)
tumor_sizes_gompertz = gompertz_growth(N0, r, K, time)

max_size = np.max([tumor_sizes_logistic, tumor_sizes_gompertz])
normalized_sizes_logistic = (tumor_sizes_logistic / max_size) * 10
normalized_sizes_gompertz = (tumor_sizes_gompertz / max_size) * 10

def create_sphere(radius):
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
    return x, y, z

fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122, projection='3d')

for ax in [ax1, ax2]:
    ax.set_xlim([-12, 12])
    ax.set_ylim([-12, 12])
    ax.set_zlim([-12, 12])

ax1.set_title("Logistic Growth")
ax2.set_title("Gompertz Growth")

def init():
    ax1.cla()
    ax2.cla()
    ax1.set_title("Logistic Growth")
    ax1.set_xlim([-12, 12])
    ax1.set_ylim([-12, 12])
    ax1.set_zlim([-12, 12])
    ax2.set_title("Gompertz Growth")
    ax2.set_xlim([-12, 12])
    ax2.set_ylim([-12, 12])
    ax2.set_zlim([-12, 12])
    return []

def update(frame):
    ax1.cla() 
    ax2.cla() 

    # Reset titles and limits
    ax1.set_title("Logistic Growth")
    ax1.set_xlim([-12, 12])
    ax1.set_ylim([-12, 12])
    ax1.set_zlim([-12, 12])

    ax2.set_title("Gompertz Growth")
    ax2.set_xlim([-12, 12])
    ax2.set_ylim([-12, 12])
    ax2.set_zlim([-12, 12])

    x, y, z = create_sphere(normalized_sizes_logistic[frame])
    ax1.plot_surface(x, y, z, color='blue', alpha=0.7)
    
    x, y, z = create_sphere(normalized_sizes_gompertz[frame])
    ax2.plot_surface(x, y, z, color='red', alpha=0.7)

    return []

ani = FuncAnimation(fig, update, frames=len(time), init_func=init, interval=100)

plt.show()

