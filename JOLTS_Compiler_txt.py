import pandas as pd
import re
from fredapi import Fred

def compile_jolts_dataset(file_path):
    # Initialize storage
    data_dict = {}  # series_id → {date_str: value}
    date_set = set()  # unique date strings

    with open(file_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        # Skip header or empty lines
        if line.strip() == '' or line.startswith('series_id'):
            continue

        # Split line into fields
        fields = line.strip().split()
        if len(fields) < 4:
            continue  # skip malformed lines

        series_id = fields[0]
        year = fields[1]
        period = fields[2]
        value = fields[3]

        # Handle M13 (annual summary) and monthly periods
        if period == 'M13':
            date_str = f"{year}-13-01"  # special placeholder for annual data
        elif re.match(r'^M(0[1-9]|1[0-2])$', period):
            month = period.replace('M', '').zfill(2)
            date_str = f"{year}-{month}-01"
        else:
            continue  # skip non-monthly and malformed periods

        # Store date
        date_set.add(date_str)

        # Store value
        if series_id not in data_dict:
            data_dict[series_id] = {}
        data_dict[series_id][date_str] = float(value)

    # Build DataFrame from all series at once
    series_frames = {sid: pd.Series(vals) for sid, vals in data_dict.items()}
    df = pd.DataFrame(series_frames)

    # Reindex to include all dates, sorted
    df = df.reindex(sorted(date_set))

    # Reset index to make 'date' a column
    df = df.reset_index().rename(columns={'index': 'date'})

    return df

# Example usage
jolts_df = compile_jolts_dataset(r'C:\Users\samee\OneDrive\Desktop\SwYtch Team Monkey\jt.data.1.AllItems.txt')
print(jolts_df.head())
print(jolts_df.shape)

# Optional: Save to CSV
jolts_df.to_csv('jolts_compiled_wide_unformatted.csv', index=False)