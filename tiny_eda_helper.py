#!/usr/bin/env python3

"""
=============================================
 Tiny EDA Helper Script - Milestone 1
=============================================
This script generates a quick exploratory data analysis (EDA)
snapshot for a dataset (CSV file) to support Milestone 1.

What it does:
- Produces summary statistics (numeric & categorical)
- Creates histograms for numeric columns
- Creates bar plots of top categories for categorical columns
- Calculates correlations between numeric columns
- Saves correlation matrix & heatmap
- Writes a short Markdown file summarizing the results
- Outputs saved in the /reports/eda folder

Usage:
    python3 tiny_eda_helper.py data/raw/your_file.csv

This supports the "EDA Summary" and "Preliminary Correlation 
Analysis" deliverables for Milestone 1 in the CRISP-DM process.
=============================================
"""

import argparse, os
import pandas as pd
import matplotlib.pyplot as plt

def main():
    ap = argparse.ArgumentParser(description="Tiny EDA helper for Milestone 1")
    ap.add_argument("csv", help="Path to dataset CSV")
    ap.add_argument("--outdir", default="reports/eda", help="Output folder for charts & summary")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    df = pd.read_csv(args.csv)

    # --- 1. Quick summary stats ---
    summary_path = os.path.join(args.outdir, "summary_stats.csv")
    df.describe(include="all").to_csv(summary_path)
    print(f"[✓] Saved summary stats → {summary_path}")

    # --- 2. Histograms for numeric columns ---
    num_cols = df.select_dtypes(include="number").columns.tolist()
    for col in num_cols:
        plt.figure()
        df[col].dropna().hist(bins=30)
        plt.title(f"Histogram: {col}")
        plt.xlabel(col); plt.ylabel("count")
        plt.tight_layout()
        out = os.path.join(args.outdir, f"hist_{col}.png")
        plt.savefig(out)
        plt.close()
        print(f"[✓] Saved histogram → {out}")

    # --- 3. Top categories for categorical columns ---
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    for col in cat_cols:
        vc = df[col].astype(str).str.strip().value_counts().head(10)
        if vc.empty: 
            continue
        plt.figure()
        vc.plot(kind="bar")
        plt.title(f"Top categories: {col}")
        plt.xlabel(col); plt.ylabel("count")
        plt.tight_layout()
        out = os.path.join(args.outdir, f"topcats_{col}.png")
        plt.savefig(out)
        plt.close()
        print(f"[✓] Saved category plot → {out}")

    # --- 4. Correlation heatmap (numeric only) ---
    if num_cols:
        corr = df[num_cols].corr()
        corr_path = os.path.join(args.outdir, "correlation_matrix.csv")
        corr.to_csv(corr_path)
        plt.figure(figsize=(6, 5))
        plt.imshow(corr, cmap="coolwarm", interpolation="nearest")
        plt.xticks(range(len(num_cols)), num_cols, rotation=90)
        plt.yticks(range(len(num_cols)), num_cols)
        plt.colorbar()
        plt.title("Correlation heatmap")
        plt.tight_layout()
        out = os.path.join(args.outdir, "correlation_heatmap.png")
        plt.savefig(out)
        plt.close()
        print(f"[✓] Saved correlation heatmap → {out}")

    # --- 5. Mini summary markdown ---
    md_path = os.path.join(args.outdir, "eda_summary.md")
    with open(md_path, "w") as f:
        f.write("# EDA Snapshot\n")
        f.write("- Summary stats in `summary_stats.csv`\n")
        f.write("- Histograms per numeric column\n")
        f.write("- Top-10 categories per categorical column\n")
        f.write("- Correlation matrix & heatmap for numeric cols\n")
    print(f"[✓] Wrote summary → {md_path}")

if __name__ == "__main__":
    main()