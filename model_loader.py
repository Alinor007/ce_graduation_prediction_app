"""
model_loader.py
Responsible for loading and caching trained model artifacts from disk.
"""

import os
import joblib
import streamlit as st

from config import MODEL_FILES


MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")


def _model_path(filename: str) -> str:
    return os.path.join(MODEL_DIR, filename)


def _all_required_files() -> list[str]:
    return [
        filename
        for registry in MODEL_FILES.values()
        for filename in registry.values()
    ]


def missing_files() -> list[str]:
    """Return a list of required .pkl files that are not yet on disk."""
    return [f for f in _all_required_files() if not os.path.exists(_model_path(f))]


@st.cache_resource
def load_all_models() -> dict:
    """
    Load all model artifacts for all three feature sets.
    Returns a nested dict:  { model_id: { algo_name | 'imputer' | 'scaler': object } }
    Raises FileNotFoundError if any required file is missing.
    """
    missing = missing_files()
    if missing:
        raise FileNotFoundError(f"Missing model files: {missing}")

    return {
        model_id: {
            key: joblib.load(_model_path(filename))
            for key, filename in registry.items()
        }
        for model_id, registry in MODEL_FILES.items()
    }
