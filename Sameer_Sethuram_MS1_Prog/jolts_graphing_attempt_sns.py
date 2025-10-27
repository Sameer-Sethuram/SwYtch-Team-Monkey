import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your formatted dataset
jolts_df = pd.read_csv('jolts_formatted.csv')
jolts_df['date'] = pd.to_datetime(jolts_df['date'], errors='coerce')

# Step 1: Define exact column labels or use precise keyword filters
target_features = [
    'Quits: Total nonfarm - Rate in Percent, Monthly, Seasonally Adjusted (All size classes)',
    'Hires: Total nonfarm - Rate in Percent, Monthly, Seasonally Adjusted (All size classes)',
    'Job Openings: Total nonfarm - Rate in Percent, Monthly, Seasonally Adjusted (All size classes)',
    'Layoffs and Discharges: Total nonfarm - Rate in Percent, Monthly, Seasonally Adjusted (All size classes)',
    'Total Separations: Total nonfarm - Rate in Percent, Monthly, Seasonally Adjusted (All size classes)'
]

# Step 2: Confirm columns exist
available_features = [col for col in jolts_df.columns if col in target_features]

if not available_features:
    print("❌ No matching columns found.")
else:
    print(f"✅ Plotting {len(available_features)} features:")
    for col in available_features:
        print(" -", col)

    # Step 3: Melt and plot
    melted_df = jolts_df[['date'] + available_features].melt(id_vars='date', var_name='Metric', value_name='Value')

    plt.figure(figsize=(14, 7))
    sns.lineplot(data=melted_df, x='date', y='Value', hue='Metric')
    plt.title("Selected JOLTS Metrics Over Time", fontsize=16)
    plt.xlabel("Date")
    plt.ylabel("Rate (%)")
    plt.legend(title="Metric", loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()