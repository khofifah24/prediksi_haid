"""Inferensi data baru (predictor.py).

Signature acuan: SPESIFIKASI §8.9.
"""

from __future__ import annotations

import pandas as pd

from .constants import FEATURE_COLUMNS, TARGET_LABELS


def predict_single(model, features: dict) -> int:
    """Prediksi satu kasus (dict 7 fitur) -> 0 | 1.

    Kolom disusun ulang sesuai ``FEATURE_COLUMNS`` agar konsisten dengan model.
    """
    row = pd.DataFrame([{col: features.get(col) for col in FEATURE_COLUMNS}])
    return int(model.predict(row)[0])


def predict_batch(model, df: pd.DataFrame) -> pd.Series:
    """Prediksi banyak baris sekaligus -> Series label 0/1."""
    X = df[FEATURE_COLUMNS].copy()
    preds = model.predict(X)
    return pd.Series(preds, index=df.index, name="prediksi").astype(int)


def label_prediction(pred: int) -> str:
    """Ubah kode 0/1 menjadi label manusiawi ('Tidak Teratur'/'Teratur')."""
    return TARGET_LABELS[int(pred)]
