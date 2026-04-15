"""Local Streamlit demo: predict risk, SHAP waterfall, optional DiCE suggestions."""

from __future__ import annotations

import sys
from pathlib import Path

import dice_ml
import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import shap
import streamlit as st
from dice_ml import Dice, Model
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.i18n import LANGS, lang_option_label, mod_tag_text, tr
from src.preprocessing import (
    FEATURE_COLUMNS,
    MODIFIABLE_FEATURES,
    NON_MODIFIABLE_FEATURES,
    TARGET_COLUMN,
    load_heart_csv,
)

CONTINUOUS_FOR_DICE = [
    "age",
    "trestbps",
    "chol",
    "thalach",
    "oldpeak",
    "sex",
    "fbs",
    "exang",
]
RANDOM_STATE = 42
MODEL_REL = Path("models") / "xgboost_pipeline.joblib"


def coerce_int_float(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for c in FEATURE_COLUMNS:
        if c == "oldpeak":
            out[c] = out[c].astype(float)
        else:
            out[c] = out[c].astype(int)
    return out


def align_query_to_training_dtypes(
    df: pd.DataFrame, train_with_target: pd.DataFrame
) -> pd.DataFrame:
    ref = train_with_target.drop(columns=[TARGET_COLUMN])
    out = df.copy()
    for c in FEATURE_COLUMNS:
        if ref[c].dtype.name == "category":
            cats = [str(x) for x in ref[c].cat.categories]
            out[c] = pd.Categorical(out[c].astype(int).astype(str), categories=cats)
        else:
            out[c] = out[c].astype(ref[c].dtype)
    return out


@st.cache_resource
def load_pipeline():
    path = PROJECT_ROOT / MODEL_REL
    if not path.is_file():
        raise FileNotFoundError()
    return joblib.load(path)


@st.cache_data
def dice_training_bundle() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Raw training frame for `dice_ml.Data`, plus DiCE-typed copy (category columns)."""
    data_path = PROJECT_ROOT / "data" / "heart-disease.csv"
    X, y = load_heart_csv(data_path)
    X = coerce_int_float(X)
    X_train, _, y_train, _ = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    df_train = pd.concat([X_train, y_train.rename(TARGET_COLUMN)], axis=1)
    d = dice_ml.Data(
        dataframe=df_train,
        continuous_features=CONTINUOUS_FOR_DICE,
        outcome_name=TARGET_COLUMN,
    )
    return df_train, d.data_df


def dice_training_frame() -> pd.DataFrame:
    return dice_training_bundle()[0]


@st.cache_resource
def tree_explainer(_pipe_version: int):
    pipe = load_pipeline()
    return shap.TreeExplainer(pipe.named_steps["clf"])


st.set_page_config(page_title="Heart Risk Advisor", layout="wide")

with st.sidebar:
    st.radio(
        tr(st.session_state.get("lang", "en"), "lang_label"),
        options=list(LANGS),
        horizontal=True,
        format_func=lang_option_label,
        key="lang",
    )
    lang = st.session_state.lang

    st.header(tr(lang, "sidebar_header"))
    st.caption(tr(lang, "sidebar_help"))
    age = st.slider(tr(lang, "age"), 25, 85, 55, help=tr(lang, "help_age"))
    sex = st.selectbox(
        tr(lang, "sex"),
        options=[0, 1],
        format_func=lambda x: tr(lang, "sex_female") if x == 0 else tr(lang, "sex_male"),
        help=tr(lang, "help_sex"),
    )
    cp = st.selectbox(
        tr(lang, "cp"),
        options=[0, 1, 2, 3],
        format_func=lambda x: tr(lang, f"cp_{x}"),
        help=tr(lang, "help_cp"),
    )
    trestbps = st.slider(tr(lang, "trestbps"), 90, 210, 130, help=tr(lang, "help_trestbps"))
    chol = st.slider(tr(lang, "chol"), 120, 600, 240, help=tr(lang, "help_chol"))
    fbs = st.selectbox(
        tr(lang, "fbs"),
        options=[0, 1],
        format_func=lambda x: tr(lang, "yes_no_no") if x == 0 else tr(lang, "yes_no_yes"),
        help=tr(lang, "help_fbs"),
    )
    restecg = st.selectbox(
        tr(lang, "restecg"),
        options=[0, 1, 2],
        format_func=lambda x: tr(lang, f"restecg_{x}"),
        help=tr(lang, "help_restecg"),
    )
    thalach = st.slider(tr(lang, "thalach"), 70, 210, 150, help=tr(lang, "help_thalach"))
    exang = st.selectbox(
        tr(lang, "exang"),
        options=[0, 1],
        format_func=lambda x: tr(lang, "yes_no_no") if x == 0 else tr(lang, "yes_no_yes"),
        help=tr(lang, "help_exang"),
    )
    oldpeak = st.slider(tr(lang, "oldpeak"), 0.0, 6.5, 1.0, 0.1, help=tr(lang, "help_oldpeak"))
    slope = st.selectbox(
        tr(lang, "slope"),
        options=[0, 1, 2],
        format_func=lambda x: tr(lang, f"slope_{x}"),
        help=tr(lang, "help_slope"),
    )
    ca = st.selectbox(
        tr(lang, "ca"),
        options=[0, 1, 2, 3, 4],
        help=tr(lang, "help_ca"),
    )
    thal = st.selectbox(
        tr(lang, "thal"),
        options=[0, 1, 2, 3],
        format_func=lambda x: tr(lang, f"thal_{x}"),
        help=tr(lang, "help_thal"),
    )

st.title(tr(lang, "app_title"))
st.caption(tr(lang, "caption"))
st.markdown(tr(lang, "main_intro"))

try:
    pipe = load_pipeline()
except FileNotFoundError:
    st.error(tr(lang, "err_missing_model", path=str(PROJECT_ROOT / MODEL_REL)))
    st.stop()

df_train_raw, df_train_typed = dice_training_bundle()

row = pd.DataFrame(
    [
        {
            "age": age,
            "sex": sex,
            "cp": cp,
            "trestbps": trestbps,
            "chol": chol,
            "fbs": fbs,
            "restecg": restecg,
            "thalach": thalach,
            "exang": exang,
            "oldpeak": oldpeak,
            "slope": slope,
            "ca": ca,
            "thal": thal,
        }
    ]
)
row = coerce_int_float(row)

prep = pipe.named_steps["prep"]
X_t = prep.transform(row)
feat_names = list(prep.get_feature_names_out())
proba = float(pipe.predict_proba(row)[0, 1])
risk_pct = proba * 100.0

if risk_pct < 40:
    band = tr(lang, "band_low")
    color = "#1b9e77"
elif risk_pct < 65:
    band = tr(lang, "band_mid")
    color = "#d95f02"
else:
    band = tr(lang, "band_high")
    color = "#7570b3"

c1, c2 = st.columns([1, 2])
with c1:
    st.subheader(tr(lang, "predicted_risk"))
    st.markdown(
        f"<div style='padding:16px;border-radius:8px;background:{color};color:white;"
        f"font-size:28px;font-weight:600;text-align:center'>{risk_pct:.1f}%</div>",
        unsafe_allow_html=True,
    )
    st.caption(tr(lang, "risk_caption", band=band))

expl = tree_explainer(0)
sv = expl.shap_values(X_t)
if isinstance(sv, list):
    sv = sv[1]
base = expl.expected_value
if hasattr(base, "__len__") and len(base) > 1:
    base = float(base.ravel()[-1])
else:
    base = float(base)

exp_plot = shap.Explanation(
    sv[0],
    base_values=base,
    data=X_t.iloc[0],
    feature_names=feat_names,
)
with c2:
    st.subheader(tr(lang, "shap_title"))
    st.caption(tr(lang, "shap_caption"))
    fig, ax = plt.subplots(figsize=(9, 5))
    shap.plots.waterfall(exp_plot, max_display=14, show=False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.divider()
st.subheader(tr(lang, "dice_section"))
st.markdown(tr(lang, "dice_lead"))
if st.button(tr(lang, "dice_button")):
    with st.spinner(tr(lang, "dice_spinner")):
        try:
            d = dice_ml.Data(
                dataframe=df_train_raw,
                continuous_features=CONTINUOUS_FOR_DICE,
                outcome_name=TARGET_COLUMN,
            )
            m = Model(model=pipe, backend="sklearn", model_type="classifier")
            exp_dice = Dice(d, m, method="random")
            query = align_query_to_training_dtypes(row, df_train_typed)
            cfs = exp_dice.generate_counterfactuals(
                query,
                total_CFs=3,
                desired_class="opposite",
                features_to_vary=list(MODIFIABLE_FEATURES),
                stopping_threshold=0.5,
                sample_size=5000,
                random_seed=42,
                verbose=False,
            )
            cf_df = cfs.cf_examples_list[0].final_cfs_df.reset_index(drop=True)
        except Exception as err:
            st.error(tr(lang, "dice_error", err=str(err)))
            st.stop()

    orig = query.iloc[0]
    rows_out = []
    for j in range(len(cf_df)):
        cf_row = cf_df.iloc[j].drop(labels=[TARGET_COLUMN], errors="ignore")
        aligned = align_query_to_training_dtypes(cf_row.to_frame().T, df_train_typed).iloc[0]
        p_after = float(pipe.predict_proba(aligned.to_frame().T)[0, 1])
        for f in FEATURE_COLUMNS:
            if str(orig[f]) != str(aligned[f]):
                rows_out.append(
                    {
                        tr(lang, "col_cf"): j + 1,
                        tr(lang, "col_feature"): f,
                        tr(lang, "col_from"): str(orig[f]),
                        tr(lang, "col_to"): str(aligned[f]),
                        tr(lang, "col_recourse"): mod_tag_text(
                            lang, f, MODIFIABLE_FEATURES
                        ),
                        tr(lang, "col_p_after"): round(p_after, 4),
                    }
                )
    if not rows_out:
        st.info(tr(lang, "dice_empty"))
    else:
        out = pd.DataFrame(rows_out)
        st.dataframe(out, width="stretch", hide_index=True)
        st.caption(
            tr(
                lang,
                "dice_caption",
                immutable=", ".join(NON_MODIFIABLE_FEATURES),
            )
        )
