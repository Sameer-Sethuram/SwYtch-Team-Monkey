import os
import re
from fredapi import Fred
import pandas as pd

# 🔑 Set your FRED API key
API_KEY = "778bb312df08b720918f5475f1581512"  # Replace with your actual key
fred = Fred(api_key=API_KEY)

# 📁 Create folder if it doesn't exist
def ensure_folder(path):
    os.makedirs(path, exist_ok=True)

# 🔍 Regex patterns for different JOLTS types
patterns = {
    'Hires': re.compile(r'^JTS\d+HIL$'),
    'Quits': re.compile(r'^JTS\d+QUR$'),
    'Openings': re.compile(r'^JTS\d+JOL$'),
    'Separations': re.compile(r'^JTS\d+SEP$'),
    'Layoffs': re.compile(r'^JTS\d+LAY$')
}

# 📦 Discover and filter series by type
def discover_series_by_type():
    search_results = fred.search('JOLTS')  # Broad keyword search
    grouped = {key: [] for key in patterns}

    for _, row in search_results.iterrows():
        series_id = row['id']
        title = row['title']
        for key, regex in patterns.items():
            if regex.match(series_id):
                grouped[key].append((series_id, title))
                break

    return grouped


# 📥 Download series and save to CSV
def download_series_grouped(grouped_series, base_folder):
    ensure_folder(base_folder)
    failed = []

    for group, series_list in grouped_series.items():
        group_folder = os.path.join(base_folder, group)
        ensure_folder(group_folder)

        for series_id, title in series_list:
            try:
                print(f"📥 Downloading {title} ({series_id})...")
                data = fred.get_series(series_id)
                df = pd.DataFrame(data, columns=[title])
                df.index.name = 'Date'
                file_path = os.path.join(group_folder, f"{series_id}.csv")
                df.to_csv(file_path)
                print(f"✅ Saved to {file_path}")
            except Exception as e:
                print(f"❌ Failed: {title} ({series_id}) — {e}")
                failed.append((group, series_id, title))

    if failed:
        print("\n⚠️ Failed downloads:")
        for group, series_id, title in failed:
            print(f" - [{group}] {title} ({series_id})")

# 🚀 Main execution
if __name__ == "__main__":
    target_folder = "JOLTS_By_Type"  # Change this to your desired folder path
    print(f"\n📂 Saving JOLTS data to: {target_folder}\n")

    grouped_series = discover_series_by_type()
    if grouped_series:
        download_series_grouped(grouped_series, target_folder)
    else:
        print("⚠️ No series found or failed to retrieve category.")

    print("\n🏁 All downloads attempted.")