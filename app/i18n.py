"""UI strings for the Streamlit app (EN / IT / DE / FR)."""

from __future__ import annotations

from typing import Any

LANGS: tuple[str, ...] = ("en", "it", "de", "fr")

# Native names for the language switcher (independent of current UI language).
LANG_DISPLAY: dict[str, str] = {
    "en": "English",
    "it": "Italiano",
    "de": "Deutsch",
    "fr": "Français",
}


def lang_option_label(code: str) -> str:
    return LANG_DISPLAY.get(code, code)

MESSAGES: dict[str, dict[str, str]] = {
    "en": {
        "page_title": "Heart Risk Advisor",
        "app_title": "Heart Risk Advisor",
        "caption": (
            "Research prototype: estimated probability of the UCI “heart disease” label from 13 inputs. "
            "Not medical advice; not for clinical decisions."
        ),
        "main_intro": (
            "**How to use this page:** set values in the **left sidebar** — the risk score and chart "
            "update as you go. The chart shows **which inputs pushed the estimate up or down** for this "
            "case. Below, you can **optionally** ask for example “what-if” changes (counterfactuals) that "
            "could lower the score, within the demo’s rules."
        ),
        "lang_label": "Language",
        "sidebar_header": "Patient inputs",
        "sidebar_help": "Change values here; the main area refreshes automatically.",
        "age": "Age (years)",
        "sex": "Sex",
        "sex_female": "Female",
        "sex_male": "Male",
        "cp": "Chest pain type (cp)",
        "cp_0": "Typical angina",
        "cp_1": "Atypical angina",
        "cp_2": "Non-anginal pain",
        "cp_3": "Asymptomatic",
        "trestbps": "Resting BP (mm Hg)",
        "chol": "Cholesterol (mg/dL)",
        "fbs": "Fasting blood sugar > 120 mg/dL",
        "yes_no_no": "No",
        "yes_no_yes": "Yes",
        "restecg": "Resting ECG",
        "restecg_0": "Normal",
        "restecg_1": "ST-T abnormality",
        "restecg_2": "LV hypertrophy",
        "thalach": "Max heart rate (thalach)",
        "exang": "Exercise angina",
        "oldpeak": "ST depression (oldpeak)",
        "slope": "ST slope",
        "slope_0": "Upsloping",
        "slope_1": "Flat",
        "slope_2": "Downsloping",
        "ca": "Major vessels colored (ca)",
        "thal": "Thal stress (thal)",
        "thal_0": "Unknown",
        "thal_1": "Normal",
        "thal_2": "Fixed defect",
        "thal_3": "Reversible defect",
        "help_age": (
            "Patient age in years. In many cardiovascular models, risk tends to increase with age "
            "(this dataset encodes age as in the original UCI table)."
        ),
        "help_sex": (
            "Sex as in the UCI Cleveland coding (0 = female, 1 = male). Used as an input feature; "
            "prevalence and patterns can differ between groups."
        ),
        "help_cp": (
            "Chest pain category from the clinical history: typical angina, atypical angina, non-anginal pain, "
            "or asymptomatic—Cleveland heart-study style labels."
        ),
        "help_trestbps": "Resting systolic blood pressure in millimetres of mercury (mm Hg), measured when the patient is calm.",
        "help_chol": "Serum cholesterol from a blood test, in mg/dL (milligrams per decilitre).",
        "help_fbs": (
            "Whether fasting blood sugar is greater than 120 mg/dL (1 = yes). A simple diabetes-related flag in this dataset."
        ),
        "help_restecg": (
            "Summary of the resting ECG: normal; ST–T wave abnormality; or possible left ventricular hypertrophy by voltage criteria."
        ),
        "help_thalach": (
            "Maximum heart rate achieved during an exercise stress test (beats per minute). Often lower when fitness or perfusion is limited."
        ),
        "help_exang": "Whether angina (chest pain) is brought on by exercise (1 = yes, 0 = no).",
        "help_oldpeak": (
            "ST depression induced by exercise relative to rest (in mm). Larger values can reflect ischemia on the stress test."
        ),
        "help_slope": (
            "Slope of the peak exercise ST segment: upsloping, flat, or downsloping—part of the stress-test interpretation."
        ),
        "help_ca": (
            "Number of major vessels coloured by fluoroscopy that show significant disease (0–3). "
            "In UCI coding, 4 means “unknown”, not a fourth vessel."
        ),
        "help_thal": (
            "Thallium stress-test category: normal perfusion; fixed defect; reversible defect; or unknown—reflects blood flow in the heart muscle."
        ),
        "predicted_risk": "Estimated risk",
        "risk_caption": "Model probability for disease label = 1 — band: **{band}**.",
        "band_low": "lower concern",
        "band_mid": "moderate",
        "band_high": "higher concern",
        "shap_title": "What drove this estimate? (SHAP)",
        "shap_caption": "Each bar shows how much a feature increased or decreased the score for the values you entered.",
        "dice_section": "Optional: “what-if” suggestions",
        "dice_lead": (
            "Generates up to **three example scenarios** where only certain inputs are changed (per the project’s "
            "modifiable list). Use this to explore the model — not as treatment advice."
        ),
        "dice_button": "Generate three counterfactual suggestions (DiCE)",
        "dice_spinner": "Running DiCE (may take a few seconds)…",
        "dice_error": "DiCE failed: {err}",
        "dice_empty": "No feature changes in returned counterfactuals (try again or adjust inputs).",
        "dice_caption": (
            "Immutable features for this demo: **{immutable}**. "
            "“Modifiable” follows the project split (clinical judgment still required)."
        ),
        "err_missing_model": "Train the model first (missing {path}).",
        "col_cf": "CF",
        "col_feature": "Feature",
        "col_from": "From",
        "col_to": "To",
        "col_recourse": "Adjustable in demo",
        "col_p_after": "P(disease) after",
        "mod_yes": "Modifiable",
        "mod_no": "Non-modifiable",
    },
    "it": {
        "page_title": "Consulente rischio cardiaco",
        "app_title": "Consulente rischio cardiaco",
        "caption": (
            "Prototipo di ricerca: probabilità stimata per l’etichetta «heart disease» del dataset UCI, "
            "da 13 variabili cliniche. Non è consulenza medica né ad uso clinico."
        ),
        "main_intro": (
            "**Come muoversi:** imposta i valori nella **barra laterale sinistra** — il punteggio di rischio "
            "e il grafico si aggiornano mentre modifichi. Il grafico indica **quali variabili hanno spinto "
            "l’esito verso l’alto o il basso** per questo caso. Più sotto puoi **facoltativamente** chiedere "
            "esempi di modifiche «e se…» (controfattuali) che potrebbero abbassare il punteggio, nei limiti della demo."
        ),
        "lang_label": "Lingua",
        "sidebar_header": "Dati del paziente",
        "sidebar_help": "Modifica qui i valori: l’area principale si aggiorna da sola.",
        "age": "Età (anni)",
        "sex": "Sesso",
        "sex_female": "Femmina",
        "sex_male": "Maschio",
        "cp": "Tipo di dolore toracico (cp)",
        "cp_0": "Angina tipica",
        "cp_1": "Angina atipica",
        "cp_2": "Dolore non anginoso",
        "cp_3": "Asintomatico",
        "trestbps": "Pressione arteriosa a riposo (mm Hg)",
        "chol": "Colesterolo (mg/dL)",
        "fbs": "Glicemia a digiuno > 120 mg/dL",
        "yes_no_no": "No",
        "yes_no_yes": "Sì",
        "restecg": "ECG a riposo",
        "restecg_0": "Normale",
        "restecg_1": "Anomalie ST-T",
        "restecg_2": "Ipertrofia VS",
        "thalach": "Frequenza cardiaca massima (thalach)",
        "exang": "Angina da sforzo",
        "oldpeak": "Depressione ST (oldpeak)",
        "slope": "Pendenza ST",
        "slope_0": "Ascendente",
        "slope_1": "Piatta",
        "slope_2": "Discendente",
        "ca": "Vasi principali colorati (ca)",
        "thal": "Test da sforzo al tallio (thal)",
        "thal_0": "Sconosciuto",
        "thal_1": "Normale",
        "thal_2": "Difetto fisso",
        "thal_3": "Difetto reversibile",
        "help_age": (
            "Età del paziente in anni. Nei modelli cardiovascolari il rischio tende spesso ad aumentare con l’età "
            "(qui come nel dataset UCI originale)."
        ),
        "help_sex": (
            "Sesso secondo la codifica Cleveland (0 = femmina, 1 = maschio). È un ingresso del modello; "
            "prevalenza e andamenti possono differire tra i gruppi."
        ),
        "help_cp": (
            "Categoria del dolore toracico dall’anamnesi: angina tipica o atipica, dolore non anginoso o assenza di sintomi—etichette stile studio di Cleveland."
        ),
        "help_trestbps": "Pressione arteriosa sistolica a riposo in mm Hg (millimetri di mercurio), misurata a riposo.",
        "help_chol": "Colesterolo sierico da emocromo, in mg/dL (milligrammi per decilitro).",
        "help_fbs": (
            "Se la glicemia a digiuno supera 120 mg/dL (1 = sì). Nel dataset è un indicatore semplice legato al metabolismo glucidico."
        ),
        "help_restecg": (
            "Sintesi dell’ECG a riposo: tracciato normale; anomalie ST-T; o segni suggestivi di ipertrofia ventricolare sinistra."
        ),
        "help_thalach": (
            "Frequenza cardiaca massima raggiunta durante un test da sforzo (battiti/min). Spesso più bassa se la capacità "
            "all’esercizio o la perfusione sono limitate."
        ),
        "help_exang": "Se compare angina (dolore toracico) durante lo sforzo (1 = sì, 0 = no).",
        "help_oldpeak": (
            "Depressione del tratto ST durante lo sforzo rispetto al riposo (in mm). Valori più alti possono indicare ischemia al test."
        ),
        "help_slope": (
            "Pendenza del tratto ST al picco dello sforzo: ascendente, piatta o discendente—fa parte dell’interpretazione del test."
        ),
        "help_ca": (
            "Numero di vasi coronarici principali che alla fluoroscopia mostrano stenosi rilevante (0–3). "
            "Nella codifica UCI, 4 significa «sconosciuto», non un quarto vaso."
        ),
        "help_thal": (
            "Esito del test da sforzo al tallio: perfusione normale; difetto fisso; difetto reversibile; o sconosciuto—legato al flusso nel miocardio."
        ),
        "predicted_risk": "Rischio stimato",
        "risk_caption": "Probabilità del modello per etichetta malattia = 1 — fascia: **{band}**.",
        "band_low": "preoccupazione minore",
        "band_mid": "moderata",
        "band_high": "maggiore preoccupazione",
        "shap_title": "Cosa ha pesato di più? (SHAP)",
        "shap_caption": "Ogni barra indica quanto una variabile ha spinto il punteggio verso l’alto o il basso, con i valori attuali.",
        "dice_section": "Facoltativo: scenari «e se…»",
        "dice_lead": (
            "Genera fino a **tre esempi** in cui cambiano solo alcuni ingressi (secondo l’elenco «modificabili» del progetto). "
            "Serve per esplorare il modello, non come indicazione terapeutica."
        ),
        "dice_button": "Genera tre suggerimenti controfattuali (DiCE)",
        "dice_spinner": "Esecuzione DiCE in corso (alcuni secondi)…",
        "dice_error": "DiCE non riuscito: {err}",
        "dice_empty": "Nessuna modifica alle variabili nei controfattuali restituiti (riprova o cambia i valori).",
        "dice_caption": (
            "Variabili fisse in questa demo: **{immutable}**. "
            "«Modificabile» segue la suddivisione del progetto (serve sempre giudizio clinico)."
        ),
        "err_missing_model": "Addestrare prima il modello (manca {path}).",
        "col_cf": "CF",
        "col_feature": "Variabile",
        "col_from": "Da",
        "col_to": "A",
        "col_recourse": "Modificabile in demo",
        "col_p_after": "P(malattia) dopo",
        "mod_yes": "Modificabile",
        "mod_no": "Non modificabile",
    },
    "de": {
        "page_title": "Herzrisiko-Assistent",
        "app_title": "Herzrisiko-Assistent",
        "caption": (
            "Forschungsprototyp: geschätzte Wahrscheinlichkeit für das UCI-Label „Herzerkrankung“ aus 13 Merkmalen. "
            "Keine medizinische Beratung; nicht für klinische Entscheidungen."
        ),
        "main_intro": (
            "**So nutzen Sie die Seite:** Tragen Sie Werte in der **linken Seitenleiste** ein — Risiko und Diagramm "
            "aktualisieren sich währenddessen. Das Diagramm zeigt, **welche Merkmale die Schätzung nach oben oder unten "
            "gedrückt** haben. Unten können Sie **optional** „Was-wäre-wenn“-Beispiele (kontrafaktisch) erzeugen, die den "
            "Score innerhalb der Demo-Regeln senken könnten."
        ),
        "lang_label": "Sprache",
        "sidebar_header": "Patienteneingaben",
        "sidebar_help": "Werte hier ändern; der Hauptbereich aktualisiert sich automatisch.",
        "age": "Alter (Jahre)",
        "sex": "Geschlecht",
        "sex_female": "Weiblich",
        "sex_male": "Männlich",
        "cp": "Brustschmerztyp (cp)",
        "cp_0": "Typische Angina",
        "cp_1": "Atypische Angina",
        "cp_2": "Nicht-anginöse Schmerzen",
        "cp_3": "Asymptomatisch",
        "trestbps": "Ruhe-Blutdruck (mm Hg)",
        "chol": "Cholesterin (mg/dL)",
        "fbs": "Nüchternblutzucker > 120 mg/dL",
        "yes_no_no": "Nein",
        "yes_no_yes": "Ja",
        "restecg": "Ruhe-EKG",
        "restecg_0": "Normal",
        "restecg_1": "ST-T-Auffälligkeiten",
        "restecg_2": "LV-Hypertrophie",
        "thalach": "Maximale Herzfrequenz (thalach)",
        "exang": "Belastungsangina",
        "oldpeak": "ST-Senkung (oldpeak)",
        "slope": "ST-Neigung",
        "slope_0": "Aufsteigend",
        "slope_1": "Flach",
        "slope_2": "Absteigend",
        "ca": "Angefärbte Hauptgefäße (ca)",
        "thal": "Thallium-Stresstest (thal)",
        "thal_0": "Unbekannt",
        "thal_1": "Normal",
        "thal_2": "Fixierter Defekt",
        "thal_3": "Reversibler Defekt",
        "help_age": (
            "Alter des Patienten in Jahren. In kardiovaskulären Modellen steigt das Risiko oft mit dem Alter "
            "(wie in der ursprünglichen UCI-Tabelle)."
        ),
        "help_sex": (
            "Geschlecht nach Cleveland-Kodierung (0 = weiblich, 1 = männlich). Merkmal im Modell; "
            "Häufigkeiten können zwischen Gruppen variieren."
        ),
        "help_cp": (
            "Brustschmerz-Kategorie aus der Anamnese: typische/atypische Angina, nicht-anginöse Schmerzen oder asymptomatisch—Cleveland-Labels."
        ),
        "help_trestbps": "Ruhe-Systolendruck in mmHg (Millimeter Quecksilbersäule), gemessen in Ruhe.",
        "help_chol": "Serumcholesterin aus Blutwert, in mg/dL (Milligramm pro Deziliter).",
        "help_fbs": (
            "Ob Nüchternblutzucker > 120 mg/dL (1 = ja). Im Datensatz ein einfacher Stoffwechsel-/Diabetes-Indikator."
        ),
        "help_restecg": (
            "Kurzbeschreibung des Ruhe-EKGs: normal; ST-T-Veränderungen; oder Hinweise auf LV-Hypertrophie."
        ),
        "help_thalach": (
            "Maximale Herzfrequenz im Belastungstest (Schläge/min). Oft niedriger bei eingeschränkter Belastbarkeit oder Perfusion."
        ),
        "help_exang": "Ob Belastungsangina auftritt (1 = ja, 0 = nein).",
        "help_oldpeak": (
            "ST-Senkung unter Belastung gegenüber Ruhe (in mm). Höhere Werte können Ischämie im Stresstest widerspiegeln."
        ),
        "help_slope": (
            "Neigung des ST-Segments unter Spitzenbelastung: aufsteigend, flach oder absteigend—Teil der Testinterpretation."
        ),
        "help_ca": (
            "Anzahl der Hauptkoronargefäße mit relevanten Veränderungen in der Fluoroskopie (0–3). "
            "In der UCI-Kodierung bedeutet 4 „unbekannt“, nicht ein viertes Gefäß."
        ),
        "help_thal": (
            "Kategorie des Thallium-Stresstests: normale Perfusion; fixierter Defekt; reversibler Defekt; oder unbekannt—bezogen auf Myokarddurchblutung."
        ),
        "predicted_risk": "Geschätztes Risiko",
        "risk_caption": "Modellwahrscheinlichkeit für Krankheitslabel = 1 — Stufe: **{band}**.",
        "band_low": "geringere Besorgnis",
        "band_mid": "mittel",
        "band_high": "höhere Besorgnis",
        "shap_title": "Was hat diese Schätzung beeinflusst? (SHAP)",
        "shap_caption": "Jeder Balken zeigt, wie stark ein Merkmal den Score mit Ihren aktuellen Werten nach oben oder unten verschoben hat.",
        "dice_section": "Optional: „Was-wäre-wenn“-Vorschläge",
        "dice_lead": (
            "Erzeugt bis zu **drei Beispielszenarien**, in denen nur bestimmte Eingaben geändert werden (gemäß der "
            "„modifizierbaren“ Liste des Projekts). Zur Modell-Exploration — keine Therapieempfehlung."
        ),
        "dice_button": "Drei kontrafaktische Vorschläge erzeugen (DiCE)",
        "dice_spinner": "DiCE läuft (einige Sekunden)…",
        "dice_error": "DiCE fehlgeschlagen: {err}",
        "dice_empty": "Keine Merkmalsänderungen in den kontrafaktischen Vorschlägen (erneut versuchen oder Eingaben anpassen).",
        "dice_caption": (
            "In dieser Demo unveränderliche Merkmale: **{immutable}**. "
            "„Modifizierbar“ folgt der Projektteilung (klinisches Urteil erforderlich)."
        ),
        "err_missing_model": "Modell zuerst trainieren (fehlt {path}).",
        "col_cf": "KF",
        "col_feature": "Merkmal",
        "col_from": "Von",
        "col_to": "Nach",
        "col_recourse": "In der Demo anpassbar",
        "col_p_after": "P(Krankheit) danach",
        "mod_yes": "Modifizierbar",
        "mod_no": "Nicht modifizierbar",
    },
    "fr": {
        "page_title": "Conseiller risque cardiaque",
        "app_title": "Conseiller risque cardiaque",
        "caption": (
            "Prototype de recherche : probabilité estimée pour l’étiquette UCI « maladie cardiaque », "
            "à partir de 13 variables. Pas un avis médical ; pas pour décisions cliniques."
        ),
        "main_intro": (
            "**Comment utiliser la page :** saisissez les valeurs dans la **barre latérale gauche** — le score et le "
            "graphique se mettent à jour au fur et à mesure. Le graphique montre **quels facteurs ont tiré l’estimation "
            "vers le haut ou le bas** pour ce cas. Plus bas, vous pouvez **facultativement** demander des exemples « et si » "
            "(contrefactuels) susceptibles d’abaisser le score, dans les limites de la démo."
        ),
        "lang_label": "Langue",
        "sidebar_header": "Données patient",
        "sidebar_help": "Modifiez les valeurs ici ; la zone principale se met à jour automatiquement.",
        "age": "Âge (ans)",
        "sex": "Sexe",
        "sex_female": "Féminin",
        "sex_male": "Masculin",
        "cp": "Type de douleur thoracique (cp)",
        "cp_0": "Angor typique",
        "cp_1": "Angor atypique",
        "cp_2": "Douleur non angineuse",
        "cp_3": "Asymptomatique",
        "trestbps": "Tension au repos (mm Hg)",
        "chol": "Cholestérol (mg/dL)",
        "fbs": "Glycémie à jeun > 120 mg/dL",
        "yes_no_no": "Non",
        "yes_no_yes": "Oui",
        "restecg": "ECG au repos",
        "restecg_0": "Normal",
        "restecg_1": "Anomalies ST-T",
        "restecg_2": "Hypertrophie VG",
        "thalach": "Fréquence cardiaque max (thalach)",
        "exang": "Angine d’effort",
        "oldpeak": "Dépression ST (oldpeak)",
        "slope": "Pente du ST",
        "slope_0": "Ascendante",
        "slope_1": "Plate",
        "slope_2": "Descendante",
        "ca": "Gros vaisseaux colorés (ca)",
        "thal": "Scintigraphie au thallium (thal)",
        "thal_0": "Inconnu",
        "thal_1": "Normal",
        "thal_2": "Défaut fixe",
        "thal_3": "Défaut réversible",
        "help_age": (
            "Âge du patient en années. Dans beaucoup de modèles cardiovasculaires, le risque augmente souvent avec l’âge "
            "(comme dans la table UCI d’origine)."
        ),
        "help_sex": (
            "Sexe selon le codage Cleveland (0 = féminin, 1 = masculin). Variable du modèle; la prévalence peut différer selon les groupes."
        ),
        "help_cp": (
            "Catégorie de douleur thoracique à l’interrogatoire : angor typique ou atypique, douleur non angineuse ou asymptomatique—libellés type Cleveland."
        ),
        "help_trestbps": "Tension artérielle systolique au repos en mmHg (millimètres de mercure), mesurée au calme.",
        "help_chol": "Cholestérol sérique issu d’une prise de sang, en mg/dL (milligrammes par décilitre).",
        "help_fbs": (
            "Indique si la glycémie à jeun dépasse 120 mg/dL (1 = oui). Dans ce jeu de données, indicateur simple lié au métabolisme du glucose."
        ),
        "help_restecg": (
            "Synthèse de l’ECG au repos : tracé normal ; anomalies ST-T ; ou signes d’hypertrophie ventriculaire gauche."
        ),
        "help_thalach": (
            "Fréquence cardiaque maximale atteinte pendant un test d’effort (battements/min). Souvent plus basse si l’effort ou la perfusion est limité."
        ),
        "help_exang": "Présence d’angine à l’effort (1 = oui, 0 = non).",
        "help_oldpeak": (
            "Dépression du segment ST à l’effort par rapport au repos (en mm). Des valeurs plus élevées peuvent traduire une ischémie à l’épreuve."
        ),
        "help_slope": (
            "Pente du segment ST au pic d’effort : ascendante, plate ou descendante—élément d’interprétation du test."
        ),
        "help_ca": (
            "Nombre de gros vaisseaux coronaires montrant une atteinte notable à la fluoroscopie (0–3). "
            "Dans le codage UCI, 4 signifie « inconnu », pas un quatrième vaisseau."
        ),
        "help_thal": (
            "Catégorie de scintigraphie au thallium : perfusion normale ; défaut fixe ; défaut réversible ; ou inconnu—liée au flux myocardique."
        ),
        "predicted_risk": "Risque estimé",
        "risk_caption": "Probabilité du modèle pour l’étiquette maladie = 1 — niveau : **{band}**.",
        "band_low": "préoccupation moindre",
        "band_mid": "modérée",
        "band_high": "préoccupation plus élevée",
        "shap_title": "Qu’est-ce qui a le plus influencé ce score ? (SHAP)",
        "shap_caption": "Chaque barre indique dans quelle mesure une variable a poussé le score vers le haut ou le bas avec les valeurs actuelles.",
        "dice_section": "Facultatif : scénarios « et si »",
        "dice_lead": (
            "Génère jusqu’à **trois exemples** où seuls certains champs changent (selon la liste « modifiables » du projet). "
            "À visée d’exploration du modèle — pas comme recommandation de traitement."
        ),
        "dice_button": "Générer trois suggestions contrefactuelles (DiCE)",
        "dice_spinner": "Exécution de DiCE (quelques secondes)…",
        "dice_error": "Échec de DiCE : {err}",
        "dice_empty": "Aucun changement de variable dans les contrefactuels renvoyés (réessayez ou modifiez les valeurs).",
        "dice_caption": (
            "Variables immuables dans cette démo : **{immutable}**. "
            "« Modifiable » suit la répartition du projet (jugement clinique requis)."
        ),
        "err_missing_model": "Entraîner d’abord le modèle (manque {path}).",
        "col_cf": "CF",
        "col_feature": "Variable",
        "col_from": "De",
        "col_to": "À",
        "col_recourse": "Ajustable en démo",
        "col_p_after": "P(maladie) après",
        "mod_yes": "Modifiable",
        "mod_no": "Non modifiable",
    },
}


def tr(lang: str, key: str, **kwargs: Any) -> str:
    """Return translated string; fallback English; supports ``{placeholders}``."""
    table = MESSAGES.get(lang) or MESSAGES["en"]
    s = table.get(key) or MESSAGES["en"].get(key) or key
    if kwargs:
        return s.format(**kwargs)
    return s


def mod_tag_text(lang: str, feature: str, modifiable_features: tuple[str, ...]) -> str:
    if feature in modifiable_features:
        return "🟢 " + tr(lang, "mod_yes")
    return "🔴 " + tr(lang, "mod_no")
