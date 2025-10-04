import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

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
covid_mask = (jolts.index >= '2020-03-01') & (jolts.index <= '2021-06-01')

# === Step 3: Smooth COVID-era data via regression-based imputation ===
smoothed_jolts = jolts.copy()

for col in jolts.columns:
    # Train on pre-COVID data
    pre_covid = jolts.loc[jolts.index < '2020-03-01']
    X_train = np.arange(len(pre_covid)).reshape(-1, 1)
    y_train = pre_covid[col].values

    model = LinearRegression().fit(X_train, y_train)

    # Predict for COVID period
    covid_idx = np.arange(len(pre_covid), len(pre_covid) + covid_mask.sum()).reshape(-1, 1)
    predicted = model.predict(covid_idx)

    # Replace COVID values with predicted
    smoothed_jolts.loc[covid_mask, col] = predicted

# === Step 4: Normalize features ===
scaler = StandardScaler()
scaled_array = scaler.fit_transform(smoothed_jolts)
smoothed_jolts_scaled = pd.DataFrame(scaled_array, columns=smoothed_jolts.columns, index=smoothed_jolts.index)

# === Step 5: Round values to one decimal place ===
rounded = smoothed_jolts_scaled.copy()
rounded = rounded.round(1)

# === Step 6: Reformat to match original structure ===
rounded_reset = rounded.reset_index()
rounded_reset.insert(0, 'index', range(1, len(rounded_reset) + 1))

# === Step 7: Save final output ===
rounded_reset.to_csv('jolts_smoothed.csv', index=False)