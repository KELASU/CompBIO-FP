
def adjust_parameters_by_environment(temperature, r, K):
    if temperature > 37:
        r *= 0.9  # Slower growth in higher temperatures
        K *= 0.8
    elif temperature < 35:
        r *= 1.1  # Faster growth in colder temperatures
    return r, K
