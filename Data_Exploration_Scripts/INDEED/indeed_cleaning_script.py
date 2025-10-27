# data cleaning file for linkedin data

import os
import pandas as pd
import psutil

def detect_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.csv':
        return 'csv'
    elif ext == '.json':
        return 'json'
    elif ext == '.parquet':
        return 'parquet'
    else:
        return None


def get_metadata(df):
    return {
        'shape': df.shape,
        'columns': list(df.columns),
        'dtypes': df.dtypes.astype(str).to_dict()
    }

def load_data(file_path, **kwargs):
    file_type = detect_file_type(file_path)
    if not file_type:
        print(f"Unsupported file type for: {file_path}")
        return None, None

    try:
        # Monitor memory before loading
        mem_before = psutil.Process().memory_info().rss
        if file_type == 'csv':
            df = pd.read_csv(file_path, **kwargs)
        elif file_type == 'json':
            df = pd.read_json(file_path, **kwargs)
        elif file_type == 'parquet':
            df = pd.read_parquet(file_path, **kwargs)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        # Validate data integrity
        if df.empty:
            print("Warning: Loaded dataframe is empty.")
        metadata = get_metadata(df)

        # Monitor memory after loading
        mem_after = psutil.Process().memory_info().rss
        print(f"Memory used for loading: {(mem_after - mem_before)/1024**2:.2f} MB")

        return df, metadata
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None, None
    

def clean_data(df):
    get_metadata(df)

    if 'countryCode' in df.columns:
        df=df.drop('countryCode', axis=1);

    if 'countryName' in df.columns:
        df=df.drop('countryName', axis=1);

    if 'postingType' in df.columns:
        df=df.drop('postingType', axis=1);

    return df

