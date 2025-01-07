import numpy as np
import matplotlib.pyplot as plt
from ui import get_user_inputs
from simulation import predict_tumor_size
from visualizationvectorized import visualize_tumor_growth, load_organ_model, normalize_tumor_sizes
from tumor_data import TUMOR_TYPES

def main():
    user_inputs = get_user_inputs(TUMOR_TYPES)
    if not user_inputs:
        print("Error: Missing user inputs!")
        return

    N0 = user_inputs["N0"]
    r = user_inputs["r"]
    organ = user_inputs["organ"]
    tumor_type = user_inputs["tumor_type"]

    # Validate inputs
    if N0 <= 0 or r <= 0:
        raise ValueError("Initial size and growth rate must be positive")

    K = TUMOR_TYPES[organ][tumor_type]["carrying_capacity"]
    print(f"N0: {N0}, r: {r}, K: {K}")

    # Simulate growth over 30 days
    t = np.linspace(0, 30, 30)
    tumor_sizes = predict_tumor_size(N0, r, K, "Gompertz", t)

    # Load organ model
    organ_model = load_organ_model(organ)

    # Normalize tumor sizes based on organ volume
    normalized_sizes = normalize_tumor_sizes(tumor_sizes, organ_model)

    print("Original Tumor Sizes:", tumor_sizes)
    print("Normalized Tumor Sizes:", normalized_sizes)

    # Pass normalized sizes to visualization
    visualize_tumor_growth(normalized_sizes, organ_model, max_growth=2.0)

    # Optional: Save tumor growth graph for reference
    plt.plot(t, tumor_sizes)
    plt.xlabel("Days")
    plt.ylabel("Tumor Size")
    plt.title("Tumor Growth Over Time")
    plt.savefig("tumor_growth.png")

if __name__ == "__main__":
    main()
