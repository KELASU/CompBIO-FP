import numpy as np
import pyvista as pv
from scipy.spatial import distance

def logistic_growth(N0, r, K, t):
    return K / (1 + (K / N0 - 1) * np.exp(-r * t))

def gompertz_growth(N0, r, K, t):
    return K * np.exp(-np.exp(r * (np.log(K / N0) - t)))

def adjust_parameters_by_environment(temperature, r, K):
    if temperature > 37:
        r *= 0.9
        K *= 0.8
    elif temperature < 35:
        r *= 1.1
    return r, K

def simulate_growth(model, N0, r, K, time_steps):
    time = np.linspace(0, 50, time_steps)
    if model == "logistic":
        return logistic_growth(N0, r, K, time), time
    elif model == "gompertz":
        return gompertz_growth(N0, r, K, time), time