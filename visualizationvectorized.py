import pyvista as pv
import numpy as np
from scipy.spatial import KDTree

def load_organ_model(organ):
    """Loads a 3D organ model based on user selection."""
    organ_files = {
        "Lungs": "assets/lungs.stl",
        "Liver": "assets/liver.stl",
        "Brain": "assets/brain.stl",
    }
    file_path = organ_files.get(organ)
    if not file_path:
        raise ValueError(f"Organ '{organ}' not recognized.")
    return pv.read(file_path)

def grow_tumor_next_to_existing(organ_model, tumor_points, tumor_size, max_growth):
    bounds = organ_model.bounds
    num_points = 10  # Reduced number of points per iteration to speed up the process
    new_tumor_points = []

    # If there are existing tumor points, spread out from them
    if tumor_points.shape[0] > 0:
        for point in tumor_points:
            new_points = np.random.uniform(
                low=(point[0] - max_growth, point[1] - max_growth, point[2] - max_growth),
                high=(point[0] + max_growth, point[1] + max_growth, point[2] + max_growth),
                size=(num_points, 3)
            )
            # Filter points inside the organ's boundaries
            for new_point in new_points:
                if bounds[0] <= new_point[0] <= bounds[1] and bounds[2] <= new_point[1] <= bounds[3] and bounds[4] <= new_point[2] <= bounds[5]:
                    new_tumor_points.append(new_point)
    
    # If there are no existing tumor points, start with random points within the organ
    if len(new_tumor_points) == 0:
        new_tumor_points = np.random.uniform(
            low=(bounds[0], bounds[2], bounds[4]),
            high=(bounds[1], bounds[3], bounds[5]),
            size=(num_points, 3)
        )
    
    new_tumor_points = np.array(new_tumor_points)

    # Use KDTree to ensure new points are inside the organ surface, but only query a subset of points
    if new_tumor_points.shape[0] > 0:
        organ_surface = organ_model.points
        kdtree = KDTree(organ_surface)
        distances, _ = kdtree.query(new_tumor_points, k=10)  # Limit query to 10 nearest neighbors
        growth_threshold = max_growth * (tumor_size / 2)

        inside_mask = distances[:, 0] <= growth_threshold  # Check if within the growth threshold

        tumor_points_inside = new_tumor_points[inside_mask]
        return tumor_points_inside
    else:
        return np.array([])  # Return empty if no tumor points are generated

def visualize_tumor_growth(tumor_sizes, organ_model, max_growth):
    """Interactive visualization of tumor growth over time."""
    plotter = pv.Plotter()
    plotter.add_mesh(organ_model, color="lightblue", opacity=0.2, label="Organ")

    tumor_points = np.array([]).reshape(0, 3)  # Start with no tumor points

    for size in tumor_sizes:
        # Grow the tumor by adding new points near the existing ones
        tumor_points_inside = grow_tumor_next_to_existing(organ_model, tumor_points, size, max_growth)
        tumor_points = np.vstack([tumor_points, tumor_points_inside])  # Add new points to the tumor

        if tumor_points_inside.size > 0:
            tumor_cloud = pv.PolyData(tumor_points_inside)
            tumor_cloud["TumorSize"] = [size] * len(tumor_points_inside)
            plotter.add_mesh(tumor_cloud, color="red", opacity=0.8, label="Tumor")

    plotter.add_legend()
    plotter.show()
