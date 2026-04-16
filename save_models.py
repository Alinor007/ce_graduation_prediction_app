# ============================================================
#  save_models.py
#  Run this script IN YOUR JUPYTER NOTEBOOK (add as a new cell
#  at the very end) to export your trained models.
#
#  After running, you will see 5 .pkl files created.
#  Copy ALL of them to the same folder as app.py.
# ============================================================

import joblib
import os

# ── Save all three trained models ──────────────────────────────
#    These variable names must match what's in your notebook.
#    If you named them differently, update the variable names below.

joblib.dump(rf_model,  'model_rf.pkl')    # Random Forest
joblib.dump(lr_model,  'model_lr.pkl')    # Logistic Regression
joblib.dump(dt_model,  'model_dt.pkl')    # Decision Tree

# ── Save the preprocessors ─────────────────────────────────────
#    These were fitted on your training data.
#    They MUST be saved so the app scales new inputs the same way.

joblib.dump(imputer,   'imputer.pkl')     # SimpleImputer (fills missing values)
joblib.dump(scaler,    'scaler.pkl')      # StandardScaler (normalizes features)

# ── Confirm ────────────────────────────────────────────────────
files = ['model_rf.pkl', 'model_lr.pkl', 'model_dt.pkl',
         'imputer.pkl', 'scaler.pkl']

print("✅ Files saved successfully!\n")
for f in files:
    size = os.path.getsize(f)
    print(f"   {f:20s}  ({size/1024:.1f} KB)")

print("\n📁 Copy these 5 files into the same folder as app.py")
print("   Then run:  streamlit run app.py")
