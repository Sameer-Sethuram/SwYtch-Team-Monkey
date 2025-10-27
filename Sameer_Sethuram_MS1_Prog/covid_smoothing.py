import pandas as pd
import numpy as np

# === Step 1: Load and clean original dataset ===
jolts = pd.read_csv('jolts_cleaned.csv')  # Replace with actual path

# Ensure 'date' is string for filtering
jolts['date'] = jolts['date'].astype(str)

# Separate rows with month 13
yearly_sums = jolts[jolts['date'].str.contains(r'-13-', na=False)].copy()

# Keep only valid months
jolts = jolts[~jolts['date'].str.contains(r'-13-', na=False)].copy()

# Convert 'date' to datetime and set as index
jolts['date'] = pd.to_datetime(jolts['date'])
jolts.set_index('date', inplace=True)

# === Step 2: Define COVID window ===
covid_start = pd.to_datetime('2020-03-01')
covid_end = pd.to_datetime('2021-06-01')
covid_mask = (jolts.index >= covid_start) & (jolts.index <= covid_end)
covid_indices = np.where(covid_mask)[0]

# === Step 3: Apply linear interpolation across COVID window ===
smoothed_jolts = jolts.copy()

for col in jolts.columns:
    # Get start and end values
    start_val = jolts.loc[covid_start, col]
    end_val = jolts.loc[covid_end, col]

    # Create linear interpolation
    num_points = covid_mask.sum()
    interpolated = np.linspace(start_val, end_val, num_points)

    # Replace COVID-era values with interpolated line
    smoothed_jolts.iloc[covid_indices, smoothed_jolts.columns.get_loc(col)] = interpolated

# === Step 4: Round values to one decimal place ===
rounded = smoothed_jolts.round(1)

# === Step 5: Reformat to match original structure ===
rounded_reset = rounded.reset_index()
rounded_reset.insert(0, 'index', range(1, len(rounded_reset) + 1))

# === Step 6: Save final output ===
rounded_reset.to_csv('jolts_smoothed.csv', index=False)