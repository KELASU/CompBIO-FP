import numpy as np

def logistic_growth(N0, r, K, t):

    if N0 <= 0 or K <= 0 or r <= 0:
        raise ValueError("N0, K, and r must be positive values.")
    return K / (1 + ((K - N0) / N0) * np.exp(-r * t))

def gompertz_growth(N0, r, K, t):

    if N0 <= 0 or K <= 0 or r <= 0:
        raise ValueError("N0, K, and r must be positive values.")
    return K * np.exp(-((K - N0) / N0) * np.exp(-r * t))

def predict_tumor_size(N0, r, K, model, t):

    if model == "Logistic":
        return logistic_growth(N0, r, K, t)
    elif model == "Gompertz":
        return gompertz_growth(N0, r, K, t)
    else:
        raise ValueError("Unknown model type.")
