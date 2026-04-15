#!/usr/bin/env python3
"""Regenerate EDA figures for the LaTeX paper. Run from repo root:
   python paper/generate_eda_figures.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATA_PATH = ROOT / "data" / "heart-disease.csv"
FIG_DIR = Path(__file__).resolve().parent / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

TARGET = "target"
LABEL_MAP = {0: "No disease (0)", 1: "Disease (1)"}


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.1)

    # --- Figure 1: class balance (matches notebook/eda.ipynb) ---
    plot_df = (
        df[TARGET]
        .map(LABEL_MAP)
        .value_counts()
        .reindex([LABEL_MAP[0], LABEL_MAP[1]])
        .rename("count")
        .reset_index()
        .rename(columns={TARGET: "class"})
    )
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    sns.barplot(
        data=plot_df,
        x="class",
        y="count",
        hue="class",
        palette="Set2",
        dodge=False,
        ax=ax,
        legend=False,
    )
    ax.set_xlabel("Target class")
    ax.set_ylabel("Count")
    ax.set_title("Class balance (Cleveland-style heart disease CSV)")
    for i, row in plot_df.iterrows():
        ax.text(i, row["count"] + 3, f"n = {int(row['count'])}", ha="center", fontsize=9)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(FIG_DIR / f"eda_class_balance.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # --- Figure 2: Pearson r vs target (numeric features) ---
    feature_cols = [c for c in df.columns if c != TARGET]
    corrs = []
    for col in feature_cols:
        s = df[[col, TARGET]].dropna()
        if len(s) > 1 and s[col].std() > 0:
            corrs.append((col, float(s[col].corr(s[TARGET]))))
    corrs.sort(key=lambda x: abs(x[1]), reverse=True)
    labels = [c for c, _ in corrs]
    values = [v for _, v in corrs]
    colors = ["#2c7fb8" if v >= 0 else "#e34a33" for v in values]

    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, values, color=colors, edgecolor="white", linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9)
    ax.axvline(0, color="0.35", linewidth=0.8)
    ax.set_xlabel("Pearson correlation with target")
    ax.set_title("Linear association of features with disease label ($n=303$)")
    ax.invert_yaxis()
    # Numeric labels at bar ends (same values as Table~\\ref{tab:corr} in the paper)
    ax.bar_label(
        bars,
        labels=[f"{v:.4f}" for v in values],
        fontsize=7.5,
        padding=3,
    )
    ax.margins(x=0.08)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(FIG_DIR / f"eda_feature_target_correlation.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # --- Figure 3: correlation matrix heatmap (numeric columns only) ---
    num_df = df[feature_cols].select_dtypes(include=[np.number])
    if num_df.shape[1] >= 2:
        cm = num_df.corr()
        fig, ax = plt.subplots(figsize=(7, 6))
        sns.heatmap(
            cm,
            ax=ax,
            cmap="RdBu_r",
            center=0,
            square=True,
            linewidths=0.3,
            cbar_kws={"shrink": 0.75, "label": "Pearson $r$"},
        )
        ax.set_title("Feature--feature correlation (numeric codings)")
        fig.tight_layout()
        for ext in ("pdf", "png"):
            fig.savefig(FIG_DIR / f"eda_correlation_matrix.{ext}", dpi=300, bbox_inches="tight")
        plt.close(fig)

    print("Wrote figures to", FIG_DIR)


if __name__ == "__main__":
    main()
