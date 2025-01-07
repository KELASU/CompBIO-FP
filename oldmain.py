from ui import get_user_inputs
from simulation import predict_tumor_size
from visualizationvectorized import visualize_tumor_growth, load_organ_model
from tumor_data import TUMOR_TYPES
import numpy as np
import matplotlib.pyplot as plt

def main():
    user_inputs = get_user_inputs(TUMOR_TYPES)
    if not user_inputs:
        print("Error: Missing user inputs!")
        return

    N0 = user_inputs["N0"]
    r = user_inputs["r"]
    organ = user_inputs["organ"]
    tumor_type = user_inputs["tumor_type"]
    logic_model = user_inputs["growth_model"]

    K = TUMOR_TYPES[organ][tumor_type]["carrying_capacity"]
    t = np.linspace(0, 10, 10)
    tumor_sizes = predict_tumor_size(N0, r, K, logic_model , t)

    organ_model = load_organ_model(organ)
    visualize_tumor_growth(tumor_sizes / K, organ_model, max_growth=1.0)

    plt.plot(t, tumor_sizes)
    plt.xlabel("Days")
    plt.ylabel("Tumor Size")
    plt.title("Tumor Growth Over Time")
    plt.savefig("tumor_growth.png")

if __name__ == "__main__":
    main()
