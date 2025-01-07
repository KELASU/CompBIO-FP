
def adjust_growth_rate_based_on_temperature(r, temperature):
    """Adjusts growth rate based on environmental temperature."""
    optimal_temp = 37  # Ideal human body temperature in Celsius
    adjustment_factor = 0.01  # Rate change per degree deviation
    return r * (1 - adjustment_factor * abs(optimal_temp - temperature))
