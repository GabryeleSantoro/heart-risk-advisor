<div align="center">

# Heart Risk Advisor

**Supervised ML for cardiovascular risk estimation** — XGBoost on tabular clinical data, with SHAP and counterfactual tooling in a Streamlit demo.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-EC6608?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=for-the-badge)](./LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/GabryeleSantoro/heart-risk-advisor?style=for-the-badge)](https://github.com/GabryeleSantoro/heart-risk-advisor/commits)
[![Stars](https://img.shields.io/github/stars/GabryeleSantoro/heart-risk-advisor?style=for-the-badge&logo=github)](https://github.com/GabryeleSantoro/heart-risk-advisor)

</div>

---

## Table of contents

|                                         |                                              |
| :-------------------------------------- | :------------------------------------------- |
| [Overview](#overview)                   | [Dataset (EDA)](#dataset-eda)                |
| [Model & stack](#model--stack)          | [Model performance](#model-performance)      |
| [Architecture](#architecture)           | [Quick start](#quick-start)                  |
| [Project layout](#project-layout)       | [Disclaimer](#disclaimer)                    |

---

## Overview

This project explores **supervised learning** for **cardiovascular risk estimation** from routine clinical and stress-test style variables. The goal is to relate a small set of patient measurements to a binary outcome that indicates whether angiographic heart disease is present—using the same kind of framing found in classic public benchmarks, **not as a substitute for a doctor**.

### What it is about

The core question is whether a model can learn patterns linking **demographics, blood pressure, cholesterol, ECG summaries, and exercise-test results** to a **disease / no-disease** label. The app is meant for **learning and demonstration**: it shows an estimated probability and tools that help interpret how the model uses the inputs, so limitations and uncertainty stay visible.

### What it is based on

The work is grounded in the widely used **UCI heart disease** tradition—tabular data with **thirteen input features** and a binary target derived from clinical follow-up (angiography). Values follow the usual coding for that family of datasets (including sentinel codes for unknown entries where applicable). Any insight applies to **this dataset and modelling setup**, not to individual medical decisions.

<details>
<summary><strong>Dataset & codings (expand)</strong></summary>

Thirteen engineered input features plus a binary target; unknowns use the usual sentinel codes from that dataset family. See `data/heart-disease.csv` and `src/preprocessing.py` for column definitions and loading logic.

</details>

---

## Dataset (EDA)

Exploratory analysis lives in [`notebook/eda.ipynb`](notebook/eda.ipynb). A machine-readable summary is [`reports/eda_summary.json`](reports/eda_summary.json) — run the notebook through the **last cell** to regenerate it.

### Shape and label

| Quantity | Value |
| :-- | --: |
| Rows | 303 |
| Input features | 13 (binary target separate) |
| Duplicate rows | 1 |

The binary **target** codes **0** = no angiographic disease, **1** = disease present. The positive class is slightly more frequent (**165** vs **138**), i.e. about **54.5%** positive — a **mild** imbalance (absolute deviation from 50% ≈ **0.045**; positive:negative ratio ≈ **1.20**).

### Missing values and UCI sentinels

This copy of the CSV has **no `?` tokens** in the feature columns; preprocessing still treats `?` as missing when loading. Following the UCI convention, **unknown** is sometimes encoded as **`ca` = 4** (5 rows) and **`thal` = 0** (2 rows); [`src/preprocessing.py`](src/preprocessing.py) maps those codes to **NaN** before imputation.

### Linear association with the target (Pearson _r_)

On raw numeric codings, the strongest correlations with the label include exercise-related and angina signals (exact values in `eda_summary.json`):

| Feature | Approx. _r_ (vs target) |
| :-- | --: |
| `exang` (exercise angina) | −0.44 |
| `cp` (chest pain type) | +0.43 |
| `oldpeak` (ST depression) | −0.43 |
| `thalach` (max HR) | +0.42 |
| `ca` (vessels colored) | −0.39 |

These are **descriptive only** (mixed discrete/continuous codings); they do not replace modelling.

### Stratification and class weights

The EDA notebook checks a **stratified** train/test split (**25%** hold-out, `random_state=42`) so train and test positive rates stay near the global rate (~**54.6%** / ~**53.9%**). **Modelling** uses a **20%** test split with the same seed — see [Model performance](#model-performance). For reference, `sklearn.utils.class_weight` “balanced” weights are about **1.10** (class 0) and **0.92** (class 1).

---

## Model & stack

Predictions come from a **gradient-boosted decision tree** classifier (**XGBoost**), preceded by standard preprocessing (handling missing codes, scaling numeric fields, and encoding categorical variables). That choice balances flexibility on tabular data with interpretability hooks compatible with common explanation methods.

| Layer               | Choice                                           |
| :------------------ | :----------------------------------------------- |
| **Classifier**      | XGBoost (gradient-boosted trees)                 |
| **Explainability**  | SHAP (e.g. waterfall-style views in the app)     |
| **Counterfactuals** | DiCE (`dice-ml`) for “what-if” style suggestions |
| **UI**              | Streamlit (`app/app.py`)                         |
| **Notebooks**       | Exploratory and modelling work under `notebook/` |

The project is **not** validated for clinical deployment; treat outputs as **research-style estimates** only.

> [!WARNING]
> **Not medical advice.** This repository is for education and research. Do not use it for diagnosis, treatment, or any clinical decision.

> [!NOTE]
> Insights are specific to **this benchmark framing and preprocessing**. External validation would be required before any real-world use.

A small **local web interface** is included if you want to explore predictions and explanations interactively.

---

## Model performance

Metrics are produced in [`notebook/modeling.ipynb`](notebook/modeling.ipynb) and summarized in [`reports/model_benchmark.json`](reports/model_benchmark.json) (run the notebook through the **last cell** to regenerate that file).

**Experimental setup:** stratified train/test split (**242 / 61** rows, 80/20, `random_state=42`). Each model uses the shared preprocessing pipeline from `src/preprocessing.py`. The benchmark uses **5-fold stratified cross-validation** on the training fold only.

### Benchmark with default hyperparameters

Five models are compared with library defaults; ranking below is by **mean CV ROC-AUC** (higher is better). Values are means ± one standard deviation across folds.

| Rank | Model               | ROC-AUC (mean ± std) | F1 (mean ± std) |
| ---: | :------------------ | :------------------- | :-------------- |
|    1 | **SVM** (RBF)       | **0.896 ± 0.036**    | 0.825 ± 0.056   |
|    2 | Logistic regression | 0.889 ± 0.037        | 0.839 ± 0.069   |
|    3 | Random Forest     | 0.887 ± 0.041        | 0.830 ± 0.044   |
|    4 | **XGBoost**         | 0.872 ± 0.052        | 0.812 ± 0.073   |
|    5 | k-NN                | 0.870 ± 0.050        | 0.813 ± 0.052   |

`GridSearchCV` (scoring **ROC-AUC**, same CV splitter) is then run on the **top two** from this table—here **SVM** and **logistic regression**—to study sensitivity to hyperparameters.

### Tuned pipelines used in the repo

Both **XGBoost** and **logistic regression** are tuned with `GridSearchCV` and saved under `models/` (see the notebook). After tuning, **cross-validated ROC-AUC** on the training set is about **0.892** for the XGBoost pipeline and **0.899** for logistic regression (exact values and best parameters are in `model_benchmark.json`).

On the **held-out test set**, logistic regression achieves a higher **ROC-AUC** than XGBoost (**~0.930 vs ~0.858**) and slightly higher accuracy (**~0.820 vs ~0.787**). Despite that, the **Streamlit app uses the tuned XGBoost model** as the primary predictor: gradient-boosted trees align well with **SHAP** and **DiCE** for the interactive explanations in this project, while the saved logistic pipeline remains a strong **linear baseline** for comparison in the notebooks.

> [!NOTE]
> Single small test sets are noisy; the gap between CV and hold-out (and between models) should not be over-interpreted. Nothing here constitutes clinical validation.

---

## Architecture

```mermaid
flowchart LR
    D[("UCI heart-style tabular data")] --> P["Preprocess: scale, encode, missings"]
    P --> M["XGBoost classifier"]
    M --> O["P(heart disease)"]
    M --> S["SHAP explanations"]
    M --> C["DiCE counterfactuals"]
    O --> UI["Streamlit UI"]
    S --> UI
    C --> UI
```

---

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/app.py
```

<details>
<summary><strong>Dependencies at a glance</strong></summary>

`scikit-learn`, `xgboost`, `shap`, `dice-ml`, `pandas`, `matplotlib`, `seaborn`, `streamlit`, `kaggle` — see [`requirements.txt`](./requirements.txt) for the canonical list.

</details>

---

## Project layout

| Path        | Role                                                           |
| :---------- | :------------------------------------------------------------- |
| `app/`      | Streamlit UI and i18n                                          |
| `src/`      | Preprocessing and shared feature definitions                   |
| `data/`     | CSV used for training / demo                                   |
| `models/`   | Serialized model artifacts                                     |
| `notebook/` | Jupyter workflows (modelling, explainability, counterfactuals) |
| `reports/`  | Exported metrics: `model_benchmark.json`, `eda_summary.json`   |

---

## Disclaimer

This software is provided **as-is** for learning and demonstration. It does not replace professional medical judgment.
