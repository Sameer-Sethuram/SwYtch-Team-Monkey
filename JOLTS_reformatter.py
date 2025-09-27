### ***** THIS SCRIPT IS FOR MAPPING THE COLUMN NAMES IN JOLTS DATASET TO READABLE COLUMN NAMES ***** ###
import pandas as pd
import re

# Lookup dictionaries (partial examples — you can expand these)
data_element_map = {
    'HI': 'Hires',
    'JO': 'Job Openings',
    'QU': 'Quits',
    'LD': 'Layoffs and Discharges',
    'TS': 'Total Separations',
    'OS': 'Other separations',
    'UN': 'Unemployment rate',
    'UO': 'UO	Unemployed persons per job opening ratio'
}

rate_level_map = {
    'R': 'Rate in Percent',
    'L': 'Level in Thousands'
}

seasonal_map = {
    'S': 'Seasonally Adjusted',
    'U': 'Not Seasonally Adjusted'
}


industry_map = {}
with open(r"C:\Users\samee\OneDrive\Desktop\SwYtch Team Monkey\mapping\jt.industry.txt", 'r') as f:
    lines = f.readlines()

    for line in lines:
        if line.strip() == '' or line.startswith('industry_code'):
            continue

        fields = line.strip().split('\t')
        industry_code = fields[0]
        industry_text = fields[1]

        industry_map[industry_code] = industry_text

def decode_series_id(series_id):
    # Strip prefix if needed
    if series_id.startswith('JT') or series_id.startswith('JT'):
        series_id = series_id[2:]

    seasonal = series_id[0]
    industry_code = series_id[1:7]
    data_element_code = series_id[-3:-1]
    rate_level_code = series_id[-1]

    # Build label
    element = data_element_map.get(data_element_code, data_element_code)
    industry = industry_map.get(industry_code, f"Industry {industry_code}")
    rate_level = rate_level_map.get(rate_level_code, rate_level_code)
    seasonal_adj = seasonal_map.get(seasonal, seasonal)

    label = f"{element}: {industry} - {rate_level}, Monthly, {seasonal_adj}"
    return label

jolts_df = pd.read_csv(r"C:\Users\samee\OneDrive\Desktop\SwYtch Team Monkey\jolts_compiled_wide_unformatted.csv")

# Apply decode_series_id to all columns except 'date'
jolts_df.columns = [
    decode_series_id(col) if col != 'date' else col
    for col in jolts_df.columns
]

print(jolts_df.columns)

jolts_df.to_csv('jolts_formatted')