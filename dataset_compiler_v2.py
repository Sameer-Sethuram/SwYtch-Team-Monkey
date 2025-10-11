import os
import pandas as pd
from fredapi import Fred

folder_path = r"C:\Users\samee\OneDrive\Desktop\SwYtch Team Monkey\Individual_Datasets"
x_axis_column = "observation_date"  # Replace with your actual x-axis column name
fred = Fred(api_key="778bb312df08b720918f5475f1581512")

merged_df = None

for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        temp_df = pd.read_csv(file_path)

        # Set x-axis column as index
        temp_df.set_index(x_axis_column, inplace=True)

        # Rename columns to reflect source file (optional)
        temp_df.columns = [f"{filename[:-4]}_{col}" for col in temp_df.columns]

        # Merge horizontally
        if merged_df is None:
            merged_df = temp_df
        else:
            merged_df = pd.merge(merged_df, temp_df, left_index=True, right_index=True, how="outer")

# Reset index if needed
merged_df.reset_index(inplace=True)

def extract_series_id(col_name):
    return col_name.split("_")[0]

series_ids = [extract_series_id(col) for col in merged_df.columns if col != "observation_date"]

# Create a dictionary of ID → Title
translated = {}
for series_id in series_ids:
    try:
        title = fred.get_series_info(series_id)['title']
        translated[series_id] = title
    except Exception as e:
        translated[series_id] = f"⚠️ Not found ({e})"

# Convert to DataFrame for easy viewing
df_translation = pd.DataFrame(list(translated.items()), columns=["Series ID", "Title"])
print(df_translation)

merged_df.columns = [
    translated.get(extract_series_id(col), col) if col != "observation_date" else col
    for col in merged_df.columns
]

print(merged_df.head())

merged_df.to_csv("combined_dataset.csv", index=False)
df_translation.to_csv("fred_series_lookup.csv", index=False)
