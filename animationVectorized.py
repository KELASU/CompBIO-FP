import pyvista as pv
import numpy as np
from scipy.spatial import KDTree
import time

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
    print(f"Loading organ model from: {file_path}")
    return pv.read(file_path)

def normalize_tumor_sizes(sizes, organ_model):
    """Normalize tumor sizes based on organ volume for visualization."""
    organ_volume = organ_model.volume
    max_allowed_volume = organ_volume * 0.3  # Max 30% of organ volume
    
    # Calculate scale factor
    max_size = np.max(sizes)
    scale_factor = max_allowed_volume / max_size if max_size > 0 else 1.0
    
    # Normalize sizes and ensure minimum visibility
    normalized_sizes = np.clip(sizes * scale_factor, 0.01, max_allowed_volume)
    return normalized_sizes

def grow_irregular_tumor_within_organ(organ_model, tumor_size, max_growth, initial_points=None):
    """Generates and grows a tumor inside the organ with growth proportional to tumor_size."""
    bounds = organ_model.bounds
    print(f"Organ bounds: {bounds}")
    num_points = 5000 + int(5000 * tumor_size)  # More points as the tumor grows
    print(f"Generating tumor with {num_points} points")

    if initial_points is None:  # Generate initial points for the first frame
        tumor_points = np.random.uniform(
            low=(bounds[0], bounds[2], bounds[4]),
            high=(bounds[1], bounds[3], bounds[5]),
            size=(num_points, 3)
        )
    else:  # Modify existing points as the tumor grows
        tumor_points = initial_points

    organ_surface = organ_model.points
    kdtree = KDTree(organ_surface)

    distances, _ = kdtree.query(tumor_points)

    # Adjust the growth threshold dynamically
    growth_threshold = max(0.1, max_growth * (tumor_size / 2))  # Ensure threshold is never too small
    inside_mask = distances <= growth_threshold

    # If no points are classified as inside, increase the threshold iteratively
    while np.sum(inside_mask) == 0 and growth_threshold < 10.0:  # Avoid infinite loop
        print(f"Warning: No points classified as inside. Increasing growth threshold from {growth_threshold}.")
        growth_threshold += 0.1  # Gradually increase the threshold
        inside_mask = distances <= growth_threshold

    tumor_points_inside = tumor_points[inside_mask]

    if len(tumor_points_inside) == 0:
        print("Critical: Failed to generate any tumor points inside the organ.")
        tumor_points_inside = np.array([[0, 0, 0]])  # Fallback to a dummy point

    tumor_cloud = pv.PolyData(tumor_points_inside)
    tumor_cloud["TumorSize"] = [tumor_size] * len(tumor_points_inside)
    return tumor_cloud, tumor_points_inside

def visualize_tumor_growth(tumor_sizes, organ_model, max_growth):
    """Animates tumor growth over time."""
    plotter = pv.Plotter()
    plotter.add_mesh(organ_model, color="lightblue", opacity=0.3, label="Organ")

    # Generate initial tumor with more points
    initial_tumor_mesh, points = grow_irregular_tumor_within_organ(
        organ_model, max(tumor_sizes[0], 0.1), max_growth  # Ensure minimum size
    )
    
    # Create denser initial surface
    cloud = pv.PolyData(initial_tumor_mesh.points)
    surface = cloud.delaunay_3d()
    
    if surface.n_cells > 0:
        tumor_mesh = surface.extract_surface()
        # Add tumor with increased visibility
        tumor_actor = plotter.add_mesh(
            tumor_mesh,
            color="darkred",
            opacity=1.0,
            label="Tumor",
            smooth_shading=True
        )
    
        # Animation loop with slower growth
        for size in tumor_sizes:
            new_tumor_mesh, points = grow_irregular_tumor_within_organ(
                organ_model,
                size,
                max_growth * 0.5,  # Reduce growth rate
                initial_points=points
            )
            
            if new_tumor_mesh.n_points >= 10:  # Increased minimum points
                new_cloud = pv.PolyData(new_tumor_mesh.points)
                new_surface = new_cloud.delaunay_3d()
                if new_surface.n_cells > 0:
                    extracted = new_surface.extract_surface()
                    tumor_mesh.points = extracted.points
                    tumor_mesh.faces = extracted.faces
            
            plotter.render()
            time.sleep(0.2)  # Slower animation
    
    plotter.camera_position = 'xy'  # Set default view
    plotter.show()