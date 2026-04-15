# Dataset: `heart-disease.csv`

This dataset is a **tabular heart-disease** dataset of the [UCI Heart Disease (Cleveland)](https://archive.ics.uci.edu/ml/datasets/heart+Disease) study: one row per patient, **13 input attributes** plus a **binary target**. The working copy here contains **303** rows and **14** columns; values are stored as **numbers** (integers or floats). Some public variants encode missing entries as `?`—**this file has no `?` tokens**, but a few columns still use **sentinel codes** (e.g. `ca = 4`, rare `thal = 0`) that often mean “unknown” in the original UCI coding. Treat those explicitly during preprocessing.

Below, **type** means how you should model the column in code:

- **Continuous numeric** — real-valued measurements; often scaled for distance-based models.
- **Binary** — two levels encoded as **0 / 1**.
- **Ordinal / categorical (integer-coded)** — discrete codes with a fixed small set of values; one-hot encoding is usually appropriate for linear models and tree ensembles (trees can use raw integers, but naming the levels still matters for reporting).

---

## Target


| Column     | Meaning                                                    | Type                 | Values in this file                                                                     |
| ---------- | ---------------------------------------------------------- | -------------------- | --------------------------------------------------------------------------------------- |
| **target** | Presence of heart disease (label used for classification). | **Binary** (integer) | **0** = no disease, **1** = disease. Roughly **138 / 165** split (no ≈ 46%, yes ≈ 54%). |


---

## Input features (13 predictors)

### Demographics


| Column  | Meaning                            | Type                             | Values / range in this file     |
| ------- | ---------------------------------- | -------------------------------- | ------------------------------- |
| **age** | Age in **years**.                  | **Continuous numeric** (integer) | **29–77** (41 distinct values). |
| **sex** | Biological sex (dataset encoding). | **Binary** (integer)             | **0** = female, **1** = male.   |


### Chest pain and resting cardiovascular measures


| Column       | Meaning                                      | Type                                    | Values / range in this file                                                                                                                      |
| ------------ | -------------------------------------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **cp**       | **Chest pain type** (Angina classification). | **Categorical** (integer codes **0–3**) | **0** = typical angina, **1** = atypical angina, **2** = non-anginal pain, **3** = asymptomatic. (Counts in this file: 0→143, 1→50, 2→87, 3→23.) |
| **trestbps** | **Resting blood pressure** on admission.     | **Continuous numeric** (integer)        | **mm Hg**; **94–200** in this file.                                                                                                              |
| **chol**     | **Serum cholesterol**.                       | **Continuous numeric** (integer)        | **mg/dL**; **126–564** here.                                                                                                                     |


### Blood sugar and ECG


| Column      | Meaning                                                                                                                                | Type                                    | Values / range in this file                                                                                                                                                                               |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **fbs**     | **Fasting blood sugar** test: whether fasting glucose is above a common clinical threshold (historically **> 120 mg/dL** in UCI docs). | **Binary** (integer)                    | **0** = false (not high), **1** = true (high).                                                                                                                                                            |
| **restecg** | **Resting ECG** pattern.                                                                                                               | **Categorical** (integer codes **0–2**) | **0** = normal, **1** = ST–T wave abnormality (e.g. T-wave inversions, ST depression/elevation), **2** = left ventricular hypertrophy or other Estes-criteria patterns (here only **4** rows coded as 2). |


### Exercise test and induced ischemia


| Column      | Meaning                                                                                                               | Type                                    | Values / range in this file                                                             |
| ----------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | --------------------------------------------------------------------------------------- |
| **thalach** | **Maximum heart rate** achieved during exercise test.                                                                 | **Continuous numeric** (integer)        | **bpm**; **71–202** here.                                                               |
| **exang**   | **Exercise-induced angina** (chest pain brought on by the test).                                                      | **Binary** (integer)                    | **0** = no, **1** = yes.                                                                |
| **oldpeak** | **ST depression** induced by exercise **relative to rest** (degree of horizontal/downsloping ST change vs. baseline). | **Continuous numeric** (float)          | **0.0–6.2**; higher values often reflect more exercise-induced ischemia on the tracing. |
| **slope**   | **Slope of the peak exercise ST segment** on the ECG.                                                                 | **Categorical** (integer codes **0–2**) | **0** = upsloping, **1** = flat, **2** = downsloping.                                   |


### Angiography-related (fluoroscopy)


| Column   | Meaning                                                                                              | Type                                    | Values / range in this file                                                                                                                                                                                                                                                          |
| -------- | ---------------------------------------------------------------------------------------------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **ca**   | **Number of major vessels** (0–3) showing significant disease on **fluoroscopy**-guided angiography. | **Categorical / count** (integer)       | **0–4** in this file. Clinically the count is **0–3**; **4** appears **5** times and in UCI lineage often marks **missing** or “not assessed” rather than “four vessels”—**verify and impute or filter** as you would for missing data.                                              |
| **thal** | **Thallium stress** (perfusion) result—blood flow pattern under stress.                              | **Categorical** (integer codes **0–3**) | Common interpretation for this encoding: **1** = normal, **2** = fixed defect, **3** = reversible defect; **0** is rare (**2** rows) and usually treated as **unknown** / missing relative to the other categories. (This column is **not** a continuous dose; keep it categorical.) |


---

## Quick reference: column order

`age`, `sex`, `cp`, `trestbps`, `chol`, `fbs`, `restecg`, `thalach`, `exang`, `oldpeak`, `slope`, `ca`, `thal`, `target`

---

## Practical notes for modeling

1. **Categorical vs numeric:** Treat **cp**, **restecg**, **slope**, **thal**, and usually **ca** as categorical for encoding and explanation (SHAP, counterfactuals), even though they are stored as numbers.
2. **Sentinels:** Pay special attention to `**ca == 4`** and `**thal == 0**`; align handling with your EDA and imputation strategy.
3. **Class balance:** The outcome is only mildly imbalanced; still use stratified splits and report metrics beyond accuracy (e.g. F1, ROC-AUC).
4. **Units:** Clinical units above follow standard UCI descriptions (**mm Hg**, **mg/dL**, **bpm**); keep them explicit in plots and in the app so results stay interpretable.

