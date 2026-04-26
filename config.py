"""
config.py
All constants, feature definitions, and lookup tables.
Must match CE_Graduation_Prediction_v3.ipynb exactly.
"""

# ── Algorithms ────────────────────────────────────────────────
ALGORITHMS = ["Random Forest", "Logistic Regression"]

# ── Raw feature columns ───────────────────────────────────────
SASE_COLS = ["SASE_GS", "SASE_MA", "SASE_LA", "SASE_SCI", "SASE_AP"]

GRADE_COLS = [
    "MAT060", "MAT070", "ENS161",
    "CVE155", "CVE151", "CVE161",
    "CVE195", "CVE196", "CVE111", "CVE112",
]

# All subjects use the same input behaviour:
# filled value = subject taken, left empty = not yet taken (treated as NaN by the model).
GRADE_COLS_LEFT  = ["MAT060", "MAT070", "ENS161", "CVE155", "CVE151"]
GRADE_COLS_RIGHT = ["CVE161", "CVE195", "CVE196", "CVE111", "CVE112"]

STRAND_COLS = [
    "STRAND_ABM", "STRAND_GAS", "STRAND_HUMSS",
    "STRAND_ICT", "STRAND_SPORTS", "STRAND_STEM", "STRAND_TVL",
]

RETAKE_COLS = ["TOTAL_RETAKES", "MAX_RETAKE", "AVG_GRADE", "HARD_FAILS"]

# ── Feature sets per model ────────────────────────────────────
FEATURES = {
    "1": SASE_COLS + ["SHS_GWA_NUM"] + STRAND_COLS,
    "2": GRADE_COLS + RETAKE_COLS + ["CGPA"],
    "3": SASE_COLS + ["SHS_GWA_NUM"] + STRAND_COLS + GRADE_COLS + RETAKE_COLS + ["CGPA"],
}

# ── Human-readable feature labels ────────────────────────────
FEATURE_LABELS = {
    "SASE_GS":       "SASE Total",
    "SASE_MA":       "SASE Math",
    "SASE_LA":       "SASE Language Arts",
    "SASE_SCI":      "SASE Science",
    "SASE_AP":       "SASE Abstract/Perceptual",
    "SHS_GWA_NUM":   "SHS GWA",
    "STRAND_STEM":   "Strand: STEM",
    "STRAND_ABM":    "Strand: ABM",
    "STRAND_GAS":    "Strand: GAS",
    "STRAND_HUMSS":  "Strand: HUMSS",
    "STRAND_TVL":    "Strand: TVL",
    "STRAND_ICT":    "Strand: ICT",
    "STRAND_SPORTS": "Strand: SPORTS",
    "MAT060":        "MAT060",
    "MAT070":        "MAT070",
    "ENS161":        "ENS161",
    "CVE155":        "CVE155",
    "CVE151":        "CVE151",
    "CVE161":        "CVE161",
    "CVE195":        "CVE195",
    "CVE196":        "CVE196",
    "CVE111":        "CVE111",
    "CVE112":        "CVE112",
    "CGPA":          "CGPA",
    "TOTAL_RETAKES": "Total Retakes",
    "MAX_RETAKE":    "Max Single Retake",
    "AVG_GRADE":     "Average Grade",
    "HARD_FAILS":    "Hard Fails (3.00)",
}

# ── SHS lookup tables ─────────────────────────────────────────
GWA_OPTIONS = {
    "80–85": 82.5,
    "81–85": 83.0,
    "86–90": 88.0,
    "91–93": 92.0,
    "91–95": 93.0,
    "96–99": 97.5,
    "96–100": 98.0,
}

ALL_STRANDS = ["STEM", "ABM", "GAS", "HUMSS", "TVL", "ICT", "SPORTS"]

# ── Model file registry ───────────────────────────────────────
MODEL_FILES = {
    "1": {
        "Random Forest":       "model_1_rf.pkl",
        "Logistic Regression": "model_1_lr.pkl",
        "imputer":             "imputer_1.pkl",
        "scaler":              "scaler_1.pkl",
    },
    "2": {
        "Random Forest":       "model_2_rf.pkl",
        "Logistic Regression": "model_2_lr.pkl",
        "imputer":             "imputer_2.pkl",
        "scaler":              "scaler_2.pkl",
    },
    "3": {
        "Random Forest":       "model_3_rf.pkl",
        "Logistic Regression": "model_3_lr.pkl",
        "imputer":             "imputer_3.pkl",
        "scaler":              "scaler_3.pkl",
    },
}

EXPORT_SNIPPET = """\
import joblib, os
os.makedirs('model', exist_ok=True)

# Model 1 — SASE + GWA + Strand
joblib.dump(models_1['Random Forest'],       'model/model_1_rf.pkl')
joblib.dump(models_1['Logistic Regression'], 'model/model_1_lr.pkl')
joblib.dump(imp1, 'model/imputer_1.pkl')
joblib.dump(scl1, 'model/scaler_1.pkl')

# Model 2 — Critical Grades + CGPA + Retakes
joblib.dump(models_2['Random Forest'],       'model/model_2_rf.pkl')
joblib.dump(models_2['Logistic Regression'], 'model/model_2_lr.pkl')
joblib.dump(imp2, 'model/imputer_2.pkl')
joblib.dump(scl2, 'model/scaler_2.pkl')

# Model 3 — Combined
joblib.dump(models_3['Random Forest'],       'model/model_3_rf.pkl')
joblib.dump(models_3['Logistic Regression'], 'model/model_3_lr.pkl')
joblib.dump(imp3, 'model/imputer_3.pkl')
joblib.dump(scl3, 'model/scaler_3.pkl')

print("✅ All 12 files saved to model/")
"""
