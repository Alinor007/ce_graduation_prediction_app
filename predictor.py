"""
predictor.py
Pure prediction logic — no Streamlit, no UI concerns.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd

from config import ALGORITHMS, FEATURE_LABELS


@dataclass
class PredictionResult:
    label: int          # 0 = Delayed, 1 = On-Time
    prob_ontime: float  # probability of on-time graduation
    prob_delayed: float

    @property
    def is_ontime(self) -> bool:
        return self.label == 1

    @property
    def risk_level(self) -> str:
        if self.prob_ontime >= 0.70:
            return "low"
        if self.prob_ontime >= 0.45:
            return "moderate"
        return "high"


@dataclass
class AlgorithmResult:
    name: str
    result: PredictionResult


def _safe_impute(imputer, df: pd.DataFrame) -> np.ndarray:
    """
    Manually apply imputation using the fill statistics already stored inside
    the pickled SimpleImputer object (imputer.statistics_).

    This bypasses the sklearn _fill_dtype AttributeError that occurs when the
    .pkl was saved with a different sklearn version than the one installed locally.
    No re-fitting is done — the original training statistics are preserved exactly.
    """
    arr = df.values.astype(float).copy()
    fill_values = imputer.statistics_   # shape: (n_features,)
    for col_idx in range(arr.shape[1]):
        nan_mask = np.isnan(arr[:, col_idx])
        if nan_mask.any():
            arr[nan_mask, col_idx] = fill_values[col_idx]
    return arr


def _preprocess(model_bundle: dict, inputs: dict, features: list[str]) -> np.ndarray:
    """Impute and scale a raw input dict using the bundle's fitted transformers."""
    df = pd.DataFrame([inputs])[features]
    imputed = _safe_impute(model_bundle["imputer"], df)
    return model_bundle["scaler"].transform(imputed)


def predict(
    model_bundle: dict,
    inputs: dict,
    features: list[str],
    algorithm: str,
) -> PredictionResult:
    """Run a single algorithm and return a PredictionResult."""
    X = _preprocess(model_bundle, inputs, features)
    label = int(model_bundle[algorithm].predict(X)[0])
    probs = model_bundle[algorithm].predict_proba(X)[0]
    return PredictionResult(label=label, prob_ontime=probs[1], prob_delayed=probs[0])


def predict_all_algorithms(
    model_bundle: dict,
    inputs: dict,
    features: list[str],
) -> list[AlgorithmResult]:
    """Run every algorithm on the same input. Used for the comparison chart."""
    X = _preprocess(model_bundle, inputs, features)
    results = []
    for name in ALGORITHMS:
        label = int(model_bundle[name].predict(X)[0])
        probs = model_bundle[name].predict_proba(X)[0]
        results.append(
            AlgorithmResult(
                name=name,
                result=PredictionResult(
                    label=label,
                    prob_ontime=probs[1],
                    prob_delayed=probs[0],
                ),
            )
        )
    return results


def get_feature_importances(model_bundle: dict, features: list[str]) -> list[tuple[str, float]]:
    """Return (label, importance) pairs sorted ascending, for the RF importance chart."""
    rf = model_bundle["Random Forest"]
    pairs = [
        (FEATURE_LABELS.get(f, f), imp)
        for f, imp in zip(features, rf.feature_importances_)
    ]
    return sorted(pairs, key=lambda x: x[1])
