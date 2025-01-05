import pyvista as pv
import numpy as np
from scipy.spatial import distance

def create_tumor_mesh(size, density_gradient=False):
    """Creates a tumor mesh (sphere) with an optional density gradient."""
    sphere = pv.Sphere(radius=size)
    if density_gradient:
        sphere["density"] = np.linspace(0, 1, sphere.n_points)
    return sphere

def load_organ_model(organ):
    """Loads a 3D organ model based on user selection."""
    organ_files = {
        "Lungs": "assets/lungs.stl",
        "Liver": "assets/liver.stl",
        "Brain": "assets/brain.stl",
    }
    file_path = organ_files.get(organ)
    if file_path is None:
        raise ValueError(f"Organ '{organ}' not recognized.")
    return pv.read(file_path)


def grow_tumor_within_organ(organ_model, tumor_growth, max_growth, randomness=0.1):
    """Simulate tumor growth constrained within the organ model."""
    tumor_points = organ_model.points.copy()
    center = tumor_points.mean(axis=0)

    # Create a density array
    densities = []

    for i in range(len(tumor_points)):
        vector = tumor_points[i] - center
        growth_factor = tumor_growth / max_growth
        noise = randomness * np.random.uniform(-1, 1, size=3)
        new_point = center + vector * growth_factor + noise

        # Constrain the tumor to grow slightly out of bounds
        if distance.euclidean(center, new_point) <= max_growth:
            tumor_points[i] = new_point
        densities.append(growth_factor)  # Assign density based on growth factor

    # Create PolyData with density as a scalar
    tumor_mesh = pv.PolyData(tumor_points)
    tumor_mesh["density"] = densities  # Assign density array
    return tumor_mesh



def normalize_tumor_sizes(tumor_sizes, organ_bounds):
    """
    Scales tumor sizes to fit within the organ bounds.

    Parameters:
        tumor_sizes (list): Original tumor sizes.
        organ_bounds (tuple): Bounds of the organ model.

    Returns:
        list: Scaled tumor sizes.
    """
    max_bound = max(organ_bounds[1::2])  # Get the maximum bound (X, Y, Z)
    max_tumor_size = max(tumor_sizes)   # Get the largest tumor size
    scale_factor = max_bound / max_tumor_size

    return [size * scale_factor for size in tumor_sizes]

def visualize_tumor_on_organ(tumor_sizes, organ):
    organ_model = load_organ_model(organ)
    organ_bounds = organ_model.bounds
    print(f"Organ Bounds: {organ_bounds}")  # Debug

    plotter = pv.Plotter()
    plotter.add_mesh(organ_model, color="lightblue", opacity=0.2)

    max_growth = max(organ_bounds[1::2])

    # Add tumors
    for i, size in enumerate(tumor_sizes):
        tumor_growth = grow_tumor_within_organ(organ_model, size, max_growth)
        plotter.add_mesh(
            tumor_growth,
            scalars="density",
            cmap="hot",
            opacity=0.8,
            name=f"Tumor-{i}",
        )

    plotter.show()

