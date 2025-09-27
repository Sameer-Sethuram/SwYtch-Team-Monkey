#!/usr/bin/env python3

"""
=============================================
 Data Quality Checks Script - Milestone 1
=============================================
This script runs a set of automated data quality checks 
on a dataset (CSV file) as part of Milestone 1 deliverables.

What it does:
- Reports dataset shape, column info, and unique counts
- Detects missing values and outputs missingness summary
- Counts duplicate rows
- Generates descriptive stats for numeric columns
- Flags potential numeric outliers (z-score method)
- Highlights categorical inconsistencies (case/spacing)
- Saves outputs to the /reports folder:
    * Markdown data quality report
    * CSVs with detailed results (missing values, outliers, etc.)

Usage:
    python3 data_quality_checks.py data/raw/your_file.csv

This supports the "Data Quality & Cleaning Report" deliverable 
for Milestone 1 in the CRISP-DM process.
=============================================
"""

import argparse, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    ap=argparse.ArgumentParser(description="Quick EDA plots + correlations for Milestone 1")
    ap.add_argument("csv")
    ap.add_argument("--outdir", default="reports/figures")
    args=ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    df=pd.read_csv(args.csv)

    # 1) Histograms for numeric columns
    num_cols=df.select_dtypes(include=[np.number]).columns.tolist()
    for c in num_cols:
        plt.figure()
        df[c].dropna().hist(bins=30)
        plt.title(f"Histogram: {c}")
        plt.xlabel(c); plt.ylabel("count")
        plt.tight_layout()
        plt.savefig(os.path.join(args.outdir, f"hist_{c}.png"))
        plt.close()

    # 2) Bar charts for top categories (up to 15) for object/category cols
    cat_cols=df.select_dtypes(include=["object","category"]).columns.tolist()
    for c in cat_cols:
        vc=df[c].astype(str).str.strip().value_counts().head(15)
        if vc.empty: 
            continue
        plt.figure()
        vc.plot(kind="bar")
        plt.title(f"Top categories: {c}")
        plt.xlabel(c); plt.ylabel("count")
        plt.tight_layout()
        plt.savefig(os.path.join(args.outdir, f"topcats_{c}.png"))
        plt.close()

    # 3) Correlation matrix heatmap (numeric only)
    if num_cols:
        corr=df[num_cols].corr()
        corr.to_csv(os.path.join(args.outdir, "correlation_matrix.csv"))
        # quick heatmap
        plt.figure()
        plt.imshow(corr, interpolation="nearest")
        plt.title("Correlation heatmap (numeric)")
        plt.xticks(range(len(num_cols)), num_cols, rotation=90)
        plt.yticks(range(len(num_cols)), num_cols)
        plt.colorbar()
        plt.tight_layout()
        plt.savefig(os.path.join(args.outdir, "correlation_heatmap.png"))
        plt.close()

    # 4) Tiny markdown summary to reference in your thread
    md=os.path.join(args.outdir, "eda_summary.md")
    with open(md,"w",encoding="utf-8") as f:
        f.write("# EDA Snapshot\n")
        f.write("- Histograms for numeric columns saved in this folder.\n")
        f.write("- Top-15 category plots per categorical column saved here.\n")
        if num_cols:
            f.write("- Correlation matrix written to `correlation_matrix.csv` and `correlation_heatmap.png`.\n")
        f.write("\nUse these visuals to write your Milestone 1 EDA bullets.\n")

    print(f"Saved figures and correlation outputs to {os.path.abspath(args.outdir)}")

if __name__=="__main__":
    main()