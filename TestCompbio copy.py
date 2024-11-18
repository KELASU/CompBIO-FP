import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Parameters
N0 = 1e3  # Initial tumor size
K = 1e7   # Carrying capacity
r = 0.3   # Growth rate
time_steps = 100  # Total time steps

def logistic_growth(N0, r, K, t):
    return K / (1 + (K / N0 - 1) * np.exp(-r * t))

def gompertz_growth(N0, r, K, t):
    return K * np.exp(-np.exp(r * (np.log(K / N0) - t)))

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

fig = plt.figure(figsize=(18, 6))
ax1 = fig.add_subplot(131, projection='3d')
ax2 = fig.add_subplot(132, projection='3d')
ax3 = fig.add_subplot(133)

for ax in [ax1, ax2]:
    ax.set_xlim([-12, 12])
    ax.set_ylim([-12, 12])
    ax.set_zlim([-12, 12])

ax1.set_title("Logistic Growth (3D)")
ax2.set_title("Gompertz Growth (3D)")
ax3.set_title("Tumor Growth Over Time")
ax3.set_xlabel("Time")
ax3.set_ylabel("Tumor Size")

logistic_line, = ax3.plot([], [], label="Logistic Growth", color="blue")
gompertz_line, = ax3.plot([], [], label="Gompertz Growth", color="red")

def init():
    ax1.cla()
    ax2.cla()
    
    ax1.set_title("Logistic Growth (3D)")
    ax1.set_xlim([-12, 12])
    ax1.set_ylim([-12, 12])
    ax1.set_zlim([-12, 12])

    ax2.set_title("Gompertz Growth (3D)")
    ax2.set_xlim([-12, 12])
    ax2.set_ylim([-12, 12])
    ax2.set_zlim([-12, 12])

    ax3.set_xlim([0, np.max(time)])
    ax3.set_ylim([0, np.max([tumor_sizes_logistic * 1.1, tumor_sizes_gompertz * 1.1])])
    ax3.legend(loc='lower right')

    logistic_line.set_data([], [])
    gompertz_line.set_data([], [])
    
    return [logistic_line, gompertz_line]

def update(frame):
    ax1.cla()
    ax1.set_title("Logistic Growth (3D)")
    ax1.set_xlim([-12, 12])
    ax1.set_ylim([-12, 12])
    ax1.set_zlim([-12, 12])
    x, y, z = create_sphere(normalized_sizes_logistic[frame])
    ax1.plot_surface(x, y, z, color='blue', alpha=0.7)

    ax2.cla()
    ax2.set_title("Gompertz Growth (3D)")
    ax2.set_xlim([-12, 12])
    ax2.set_ylim([-12, 12])
    ax2.set_zlim([-12, 12])
    x, y, z = create_sphere(normalized_sizes_gompertz[frame])
    ax2.plot_surface(x, y, z, color='red', alpha=0.7)

    logistic_line.set_data(time[:frame + 1], tumor_sizes_logistic[:frame + 1])
    gompertz_line.set_data(time[:frame + 1], tumor_sizes_gompertz[:frame + 1])

    return [logistic_line, gompertz_line]

ani = FuncAnimation(fig, update, frames=len(time), init_func=init, interval=100)

plt.show()
