#!/usr/bin/env python3
"""Recompute mean |SHAP| aggregated to logical raw features and write reports/shap_global_summary.json.

Uses the saved XGBoost pipeline, the same stratified split as modeling (random_state=42),
and SHAP on the *training* rows only — matching paper/heart_risk_advisor_study.tex (Section~\\ref{sec:featimp}).

Run from repo root:
  python scripts/export_shap_global_summary.py
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import joblib
import numpy as np
import shap
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.preprocessing import (  # noqa: E402
    MODIFIABLE_FEATURES,
    NON_MODIFIABLE_FEATURES,
    load_heart_csv,
)

RANDOM_STATE = 42
MODEL_REL = Path("models/xgboost_pipeline.joblib")
DATA_REL = Path("data/heart-disease.csv")
OUT_REL = Path("reports/shap_global_summary.json")


def raw_base_name(fname: str) -> str:
    """Map sklearn output column name to logical raw UCI attribute.

    One-hot columns look like ``cp_1.0`` → group key ``cp``. Numeric/binary columns
    are single tokens (``sex``, ``oldpeak``, …) and map to themselves; their SHAP
    mass is not dropped.
    """
    return str(fname).split("_")[0]


def main() -> None:
    model_path = ROOT / MODEL_REL
    if not model_path.is_file():
        raise FileNotFoundError(f"Missing {model_path}; train in notebook/modeling.ipynb first.")

    np.random.seed(RANDOM_STATE)

    pipe = joblib.load(model_path)
    X, y = load_heart_csv(ROOT / DATA_REL)
    X_train, _X_test, y_train, _y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    prep = pipe.named_steps["prep"]
    X_train_t = prep.transform(X_train)
    feature_names = list(prep.get_feature_names_out())

    clf = pipe.named_steps["clf"]
    explainer = shap.TreeExplainer(clf)
    shap_values = explainer.shap_values(X_train_t)
    if isinstance(shap_values, list):
        shap_values = np.asarray(shap_values[1])

    abs_shap = np.abs(np.asarray(shap_values, dtype=np.float64))
    mean_abs_per_column = abs_shap.mean(axis=0)

    logical: dict[str, float] = defaultdict(float)
    for j, fname in enumerate(feature_names):
        logical[raw_base_name(fname)] += float(mean_abs_per_column[j])

    logical_sorted = sorted(logical.items(), key=lambda kv: kv[1], reverse=True)
    top5 = logical_sorted[:5]

    total_mass = sum(logical.values())
    modifiable = {f for f in MODIFIABLE_FEATURES}
    nonmod = {f for f in NON_MODIFIABLE_FEATURES}
    assert modifiable & nonmod == set()
    mass_mod = sum(logical.get(f, 0.0) for f in modifiable)
    mass_nm = sum(logical.get(f, 0.0) for f in nonmod)
    frac_mod = mass_mod / total_mass if total_mass > 0 else float("nan")

    report = {
        "meta": {
            "source": "scripts/export_shap_global_summary.py",
            "model": str(MODEL_REL),
            "split": "train_test_split test_size=0.2 random_state=42 stratify=y",
            "shap_rows": "training split only (same split as modeling notebook; matches paper SHAP table)",
            "shap": (
                "TreeExplainer on prep.transform(X_train); mean absolute SHAP per engineered column, "
                "then summed by logical raw feature: one-hot levels for cp, restecg, slope, thal share a "
                "prefix before '_'; numeric/binary columns (age, sex, trestbps, ...) are single columns "
                "and map to themselves."
            ),
        },
        "mean_abs_shap_top5_logical": [
            {"feature": name, "mean_abs_shap": round(val, 3)} for name, val in top5
        ],
        "shap_mass_modifiable_vs_fixed": {
            "fraction_modifiable_features": round(frac_mod, 4),
            "fraction_age_sex": round(1.0 - frac_mod, 4),
            "note": (
                "Sum of mean |SHAP| over logical features excluding {age, sex} "
                "divided by sum over all logical features."
            ),
        },
    }

    out_path = ROOT / OUT_REL
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        f.write("\n")

    print("Wrote", out_path)
    for row in report["mean_abs_shap_top5_logical"]:
        print(f"  {row['feature']}: {row['mean_abs_shap']}")
    print(f"  fraction_modifiable: {report['shap_mass_modifiable_vs_fixed']['fraction_modifiable_features']}")


if __name__ == "__main__":
    main()
