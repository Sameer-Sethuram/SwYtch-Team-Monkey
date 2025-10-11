import pandas as pd

jolts_df = pd.read_csv('jolts_formatted.csv')

print(f"\n🔢 Total columns in dataset (excluding 'date'): {len(jolts_df.columns) - 1}")

# 1. Filter by State
state_filter = 'in Arizona'
state_columns = [col for col in jolts_df.columns if state_filter in col]
print(f"\n🟦 Columns for {state_filter}: {len(state_columns)} found")
print("Sample:", state_columns[:5])

# 2. Filter by Industry
industry_filter = 'Retail trade'
industry_columns = [col for col in jolts_df.columns if industry_filter in col]
print(f"\n🟩 Columns for {industry_filter}: {len(industry_columns)} found")
print("Sample:", industry_columns[:5])

# 3. Filter by Size Class
size_filter = '(10 to 49 employees)'
size_columns = [col for col in jolts_df.columns if size_filter in col]
print(f"\n🟨 Columns for {size_filter}: {len(size_columns)} found")
print("Sample:", size_columns[:5])

# 4. Filter by Data Element
element_filter = 'Quits:'
quits_columns = [col for col in jolts_df.columns if col.startswith(element_filter)]
print(f"\n🟥 Columns for {element_filter.strip()}: {len(quits_columns)} found")
print("Sample:", quits_columns[:5])

# 5. Combined Filter: Quits in Arizona for 10 to 49 Employees
combined_columns = [
    col for col in jolts_df.columns
    if 'Quits:' in col and 'in Arizona' in col and '(10 to 49 employees)' in col
]
print(f"\n🧪 Quits in Arizona for 10 to 49 employees: {len(combined_columns)} found")
print("Sample:", combined_columns[:5])

# 6. Group by Seasonal Adjustment
seasonally_adjusted = [col for col in jolts_df.columns if not 'Not Seasonally Adjusted' in col]
not_seasonally_adjusted = [col for col in jolts_df.columns if 'Not Seasonally Adjusted' in col]

print(f"\n🌤️ Seasonally Adjusted columns: {len(seasonally_adjusted)} found")
print("Sample:", seasonally_adjusted[:5])

print(f"\n🌥️ Not Seasonally Adjusted columns: {len(not_seasonally_adjusted)} found")
print("Sample:", not_seasonally_adjusted[:5])

print(len(jolts_df.columns))