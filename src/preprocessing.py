"""Preprocessing and feature engineering for the UCI-style heart disease CSV."""

from __future__ import annotations

from pathlib import Path
from typing import Final

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

TARGET_COLUMN: Final[str] = "target"

FEATURE_COLUMNS: Final[tuple[str, ...]] = (
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
)

# Numeric / binary columns: median imputation + scaling (per project roadmap).
NUMERIC_FEATURES: Final[tuple[str, ...]] = (
    "age",
    "sex",
    "trestbps",
    "chol",
    "fbs",
    "thalach",
    "exang",
    "oldpeak",
    "ca",
)

# Integer-coded categoricals: mode imputation + one-hot (Phase 2 spec).
CATEGORICAL_ONEHOT_FEATURES: Final[tuple[str, ...]] = (
    "cp",
    "restecg",
    "slope",
    "thal",
)

# For DiCE / counterfactual constraints: do not treat these as actionable knobs.
NON_MODIFIABLE_FEATURES: Final[tuple[str, ...]] = ("age", "sex")

MODIFIABLE_FEATURES: Final[tuple[str, ...]] = tuple(
    c for c in FEATURE_COLUMNS if c not in NON_MODIFIABLE_FEATURES
)


def _replace_uci_sentinels(X: pd.DataFrame) -> pd.DataFrame:
    """Map UCI lineage unknown codes to NaN: ``ca == 4``, ``thal == 0``."""
    if not isinstance(X, pd.DataFrame):
        raise TypeError(
            "Expected a pandas DataFrame with columns 'ca' and 'thal'. "
            f"Got {type(X).__name__}."
        )
    out = X.copy()
    if "ca" in out.columns:
        out.loc[out["ca"] == 4, "ca"] = np.nan
    if "thal" in out.columns:
        out.loc[out["thal"] == 0, "thal"] = np.nan
    return out


def _sentinel_transformer() -> FunctionTransformer:
    return FunctionTransformer(
        _replace_uci_sentinels,
        validate=False,
        feature_names_out="one-to-one",
    )


def _one_hot_encoder() -> OneHotEncoder:
    return OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False,
    )


def build_preprocessing_pipeline(
    *,
    with_sentinel_cleaner: bool = True,
) -> Pipeline:
    """Return a ``Pipeline`` of (optional) sentinel cleaning + ``ColumnTransformer``.

    Input **X** to ``fit`` / ``transform`` should be a **DataFrame** with the
    feature columns used in training (typically ``FEATURE_COLUMNS``). The
    returned pipeline uses ``set_output(transform="pandas")`` so transforms
    return DataFrames when the sklearn/pandas versions support it.
    """
    numeric_pipe = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipe = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", _one_hot_encoder()),
        ]
    )

    column_transformer = ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, list(NUMERIC_FEATURES)),
            ("cat", categorical_pipe, list(CATEGORICAL_ONEHOT_FEATURES)),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

    steps: list[tuple[str, object]] = []
    if with_sentinel_cleaner:
        steps.append(("sentinels", _sentinel_transformer()))
    steps.append(("features", column_transformer))

    pipe = Pipeline(steps)
    pipe.set_output(transform="pandas")
    return pipe


def load_heart_csv(
    path: str | Path,
    *,
    na_values: tuple[str, ...] = ("?",),
) -> tuple[pd.DataFrame, pd.Series]:
    """Load CSV with explicit missing tokens; return ``(X, y)`` with typed columns."""
    p = Path(path)
    raw = pd.read_csv(p, na_values=list(na_values))
    if TARGET_COLUMN not in raw.columns:
        raise ValueError(f"Expected column {TARGET_COLUMN!r} in {p}")
    missing = [c for c in FEATURE_COLUMNS if c not in raw.columns]
    if missing:
        raise ValueError(f"Missing feature column(s): {missing}")
    X = raw.loc[:, list(FEATURE_COLUMNS)].copy()
    y = raw[TARGET_COLUMN].copy()
    return X, y
