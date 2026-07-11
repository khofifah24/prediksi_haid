"""KDD-4 Data Mining — Decision Tree (model.py).

Bangun, latih, dan simpan ``DecisionTreeClassifier``.
Signature acuan: SPESIFIKASI §8.6.
"""

from __future__ import annotations

import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from .constants import RANDOM_STATE

# Argumen yang valid untuk DecisionTreeClassifier (menyaring kunci config asing).
_TREE_PARAMS = {
    "criterion",
    "max_depth",
    "min_samples_split",
    "min_samples_leaf",
    "max_features",
    "ccp_alpha",
    "class_weight",
    "random_state",
}


def build_model(params: dict) -> DecisionTreeClassifier:
    """Bangun DecisionTreeClassifier dari ``config['decision_tree']``.

    Kunci yang bukan argumen sah diabaikan; ``random_state`` default 42 bila
    tak diberikan.
    """
    clean = {k: v for k, v in (params or {}).items() if k in _TREE_PARAMS}
    clean.setdefault("random_state", RANDOM_STATE)
    return DecisionTreeClassifier(**clean)


def train_model(model: DecisionTreeClassifier, X_train, y_train) -> DecisionTreeClassifier:
    """Latih model pada data latih (``model.fit``)."""
    model.fit(X_train, y_train)
    return model


def get_feature_importance(
    model: DecisionTreeClassifier, feature_names: list[str]
) -> pd.DataFrame:
    """Kembalikan DataFrame {fitur, importance} terurut menurun."""
    df = pd.DataFrame(
        {"fitur": list(feature_names), "importance": model.feature_importances_}
    )
    return df.sort_values("importance", ascending=False).reset_index(drop=True)


def save_model(model: DecisionTreeClassifier, path: str) -> None:
    """Serialisasi model ke ``path`` (.joblib)."""
    from pathlib import Path

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)


def load_model(path: str) -> DecisionTreeClassifier:
    """Muat model terlatih dari ``path`` (.joblib)."""
    return joblib.load(path)
