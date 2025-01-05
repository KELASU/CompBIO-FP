from ui import get_user_inputs
from simulation import simulate_growth, adjust_parameters_by_environment
from visualization import visualize_tumor_on_organ

if __name__ == "__main__":
    # Get user inputs
    inputs = get_user_inputs()

    # Unpack inputs
    N0 = inputs["N0"]
    r = inputs["r"]
    K = inputs["K"]
    temperature = inputs["temperature"]
    organ = inputs["organ"]

    # Adjust parameters for environmental conditions
    r, K = adjust_parameters_by_environment(temperature, r, K)

    # Simulate tumor growth
    tumor_sizes, _ = simulate_growth("gompertz", N0, r, K, 100)
    

    # Visualize tumor growth
    visualize_tumor_on_organ(tumor_sizes, organ)

