import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

# Load the Excel file
file_path = 'tumorgrowth.xlsx'  # Replace with your file path
tumor_data = pd.ExcelFile(file_path)

# Read the data from the relevant sheet
data = tumor_data.parse("OriginalData")

# Clean column names by stripping extra spaces
data.columns = data.columns.str.strip()

# Rename the 'Unnamed: 0' column to 'Day'
data.rename(columns={'Unnamed: 0': 'Day'}, inplace=True)

# Print the column names to verify
print("Columns in data:", data.columns)

# Extract the Day column and the control values for each sample (columns 2 to 8)
control_data = data[['Day', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8']]

# Convert Day to numeric and drop rows with NaN values
control_data.loc[:, 'Day'] = pd.to_numeric(control_data['Day'], errors='coerce')
control_data = control_data.dropna(subset=['Day'])

# Print the first few rows of the cleaned data
print(control_data.head())

# Define the Logistic and Gompertz models
def logistic_growth_fit(t, N0, r, K):
    t = np.asarray(t)  # Ensure t is treated as an array
    return K / (1 + ((K - N0) / N0) * np.exp(-r * t))

def gompertz_growth_fit(t, N0, r, K):
    t = np.asarray(t)  # Ensure t is treated as an array
    return K * np.exp(-np.exp(r * (np.log(K / N0) - t)))

# List of sample columns (from 'Unnamed: 2' to 'Unnamed: 8')
samples = ['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8']

# Loop through each sample and fit the models
for sample in samples:
    # Extract the tumor size values for the current sample
    sample_data = control_data[['Day', sample]].dropna()  # Remove rows with NaN values
    days = sample_data['Day'].values
    control_values = sample_data[sample].values
    
    # Ensure 'days' is an array of floats
    days = np.asarray(days, dtype=np.float64)

    # Initial guesses for the model parameters
    initial_N0 = control_values[0]  # Initial tumor size (start of the data)
    initial_K = max(control_values)  # Maximum size of the tumor
    initial_r = (np.log(control_values[-1]) - np.log(control_values[0])) / (days[-1] - days[0])  # Estimate growth rate
    
    # Fit the Logistic model
    try:
        logistic_params, _ = curve_fit(logistic_growth_fit, days, control_values, p0=[initial_N0, initial_r, initial_K], maxfev=10000)
    except RuntimeError as e:
        print(f"Logistic fit failed for Sample {sample}: {e}")
        continue
    
    # Fit the Gompertz model
    try:
        gompertz_params, _ = curve_fit(gompertz_growth_fit, days, control_values, p0=[initial_N0, initial_r, initial_K], maxfev=10000)
    except RuntimeError as e:
        print(f"Gompertz fit failed for Sample {sample}: {e}")
        continue
    
    # Generate a smooth curve for predictions
    continuous_days = np.linspace(min(days), max(days), 500)
    logistic_values = logistic_growth_fit(continuous_days, *logistic_params)
    gompertz_values = gompertz_growth_fit(continuous_days, *gompertz_params)
    
    # Calculate R² and MSE for both models
    logistic_r2 = r2_score(control_values, logistic_growth_fit(days, *logistic_params))
    gompertz_r2 = r2_score(control_values, gompertz_growth_fit(days, *gompertz_params))
    
    logistic_mse = mean_squared_error(control_values, logistic_growth_fit(days, *logistic_params))
    gompertz_mse = mean_squared_error(control_values, gompertz_growth_fit(days, *gompertz_params))
    
    # Print the results for comparison
    print(f"Results for Sample {sample}:")
    print(f"  Logistic Model R²: {logistic_r2:.4f}, MSE: {logistic_mse:.4f}")
    print(f"  Gompertz Model R²: {gompertz_r2:.4f}, MSE: {gompertz_mse:.4f}")
    
    # Plot the data and the model fits
    plt.figure(figsize=(10, 6))
    plt.scatter(days, control_values, color='black', label=f"Control Data (Sample {sample})", zorder=5)
    plt.plot(continuous_days, logistic_values, label="Logistic Model (Curve)", color='blue')
    plt.plot(continuous_days, gompertz_values, label="Gompertz Model (Curve)", color='green')
    plt.xlabel("Days")
    plt.ylabel("Tumor Size")
    plt.title(f"Tumor Growth: Sample {sample} - Control Data vs Models")
    plt.legend()
    plt.grid()
    plt.show()
