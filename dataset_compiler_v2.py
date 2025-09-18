import os
import pandas as pd

folder_path = "C:\Users\samee\OneDrive\Desktop\SwYtch Team Monkey\Individual_Datasets"
x_axis_column = "timestamp"  # Replace with your actual x-axis column name

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

print(merged_df.head())
