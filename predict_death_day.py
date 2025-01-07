
def predict_death_day(age, tumor_type, organ, initial_volume, max_volume, mathlogic):
    """
    Predicts the estimated day of death based on the tumor's growth curve.
    - age: Patient's age.
    - tumor_type: Malignant tumor type.
    - organ: Organ where the tumor is located.
    - initial_volume: Starting volume of the tumor.
    - max_volume: Critical volume for the organ.

    Returns:
        Estimated day of death.
    """
    # Age factor (younger patients resist more)
    age_factor = 1 + (age - 50) / 100  # Assume base resistance at age 50

    # Growth rate adjustment based on tumor type
    if organ not in TUMOR_TYPES or tumor_type not in TUMOR_TYPES[organ]:
        raise ValueError(f"Invalid organ or tumor type: {organ}, {tumor_type}")
    
    carrying_capacity = TUMOR_TYPES[organ][tumor_type]["carrying_capacity"]
    adjusted_rate = 0.05 / age_factor  # Baseline growth rate (modifiable)

    # Calculate days to reach critical volume
    death_day = 0
    volume = initial_volume
    while volume < max_volume:
        volume = mathlogic(death_day, initial_volume, carrying_capacity, adjusted_rate)
        death_day += 1

    return death_day
