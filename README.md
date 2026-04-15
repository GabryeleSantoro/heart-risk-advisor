# Heart Risk Advisor

This project explores **supervised learning** for **cardiovascular risk estimation** from routine clinical and stress-test style variables. The goal is to relate a small set of patient measurements to a binary outcome that indicates whether angiographic heart disease is present—using the same kind of framing found in classic public benchmarks, not as a substitute for a doctor.

## What it is about

The core question is whether a model can learn patterns linking **demographics, blood pressure, cholesterol, ECG summaries, and exercise-test results** to a **disease / no-disease** label. The app is meant for **learning and demonstration**: it shows an estimated probability and tools that help interpret how the model uses the inputs, so limitations and uncertainty stay visible.

## What it is based on

The work is grounded in the widely used **UCI heart disease** tradition—tabular data with **thirteen input features** and a binary target derived from clinical follow-up (angiography). Values follow the usual coding for that family of datasets (including sentinel codes for unknown entries where applicable). Any insight applies to **this dataset and modelling setup**, not to individual medical decisions.

## What kind of model it uses

Predictions come from a **gradient-boosted decision tree** classifier (**XGBoost**), preceded by standard preprocessing (handling missing codes, scaling numeric fields, and encoding categorical variables). That choice balances flexibility on tabular data with interpretability hooks compatible with common explanation methods. The project is **not** validated for clinical deployment; treat outputs as **research-style estimates** only.

A small **local web interface** is included if you want to explore predictions and explanations interactively.
