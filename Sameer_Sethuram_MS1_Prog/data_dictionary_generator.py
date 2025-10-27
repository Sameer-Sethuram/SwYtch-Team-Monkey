import pandas as pd
from fredapi import Fred
import os

# === Step 1: Load Dataset ===
DATA_PATH = "combined_dataset.csv"  # Replace with your actual dataset path
df = pd.read_csv(DATA_PATH)

# FredAPI key
fred = Fred(api_key="778bb312df08b720918f5475f1581512")

# === Step 2: Generate Data Dictionary ===
def infer_dtype(dtype):
    if pd.api.types.is_string_dtype(dtype):
        return "String"
    elif pd.api.types.is_numeric_dtype(dtype):
        return "Numeric"
    elif pd.api.types.is_bool_dtype(dtype):
        return "Boolean"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "Datetime"
    else:
        return "Other"

lookup_df = pd.read_csv("fred_series_lookup.csv", names=["series_id", "column_name"])
name_to_id = dict(zip(lookup_df["column_name"], lookup_df["series_id"]))

def extract_series_id(readable_name):
    return name_to_id.get(readable_name, None)

def get_description(col_name):
    series_id = extract_series_id(col_name)
    return name_to_id.get(series_id, "TODO: Add description")

def get_fred_metadata(series_id):
    try:
        info = fred.get_series_info(series_id)
        title = info.get("title", "Unknown Title")
        notes = info.get("notes", "No description available.")
        return title, notes
    except Exception as e:
        return "⚠️ Not found", f"Error: {e}"

dictionary_lines = []

for col in df.columns:
    dtype = infer_dtype(df[col].dtype)
    example = df[col].dropna().iloc[0] if not df[col].dropna().empty else "N/A"

    series_id = extract_series_id(col)
    if series_id:
        title, notes = get_fred_metadata(series_id)
        description = f"**{title}**: {notes}"
    else:
        description = "TODO: Add description"

    dictionary_lines.append(f"    - *{col}* → {dtype} (e.g., {example})  \n      {description}")

# === Step 3: Format README Section ===
readme_section = f"""
### **2. Documenting Data Properties (Data Dictionary)**

- ***General* →** Create a simple data dictionary: a table of columns, data types, example values, and short descriptions. This will help you spot gaps, duplicates, or unclear fields.
- ***Your Dataset Example* →**
{chr(10).join(dictionary_lines)}
"""

# === Step 4: Append to README.md ===
README_PATH = "README.md"

if not os.path.exists(README_PATH):
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write("## Project Overview\n\n")

with open(README_PATH, "a", encoding="utf-8") as f:
    f.write("\n" + readme_section)

print("✅ Data dictionary appended to README.md")