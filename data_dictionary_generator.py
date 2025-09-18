import pandas as pd
import os

# === Step 1: Load Dataset ===
DATA_PATH = "your_dataset.csv"  # Replace with your actual dataset path
df = pd.read_csv(DATA_PATH)

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

dictionary_lines = []
for col in df.columns:
    dtype = infer_dtype(df[col].dtype)
    example = df[col].dropna().iloc[0] if not df[col].dropna().empty else "N/A"
    dictionary_lines.append(f"    - *{col}* → {dtype} (e.g., {example})  # TODO: Add description")

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
    with open(README_PATH, "w") as f:
        f.write("## Project Overview\n\n")

with open(README_PATH, "a") as f:
    f.write("\n" + readme_section)

print("✅ Data dictionary appended to README.md")