"""KDD-3 Transformation (transformation.py).

Konversi Likert -> numerik, agregasi indikator per variabel (rata-rata),
encoding target. Signature acuan: SPESIFIKASI §8.4.
"""

from __future__ import annotations

import pandas as pd

from .constants import (
    FEATURE_COLUMNS,
    FEATURE_ITEM_MAP,
    LIKERT_ITEM_COLUMNS,
    TARGET_COLUMN,
)


def encode_likert(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    """Ubah jawaban Likert (SS..STS) menjadi numerik 5..1 sesuai ``mapping``.

    Toleran bila kolom sudah numerik (dibiarkan apa adanya). Nilai teks di luar
    ``mapping`` menjadi NaN (ditangani di preprocessing).
    """
    df = df.copy()
    for col in LIKERT_ITEM_COLUMNS:
        if col not in df.columns:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            continue
        df[col] = df[col].map(lambda v: mapping.get(str(v).strip().upper(), None))
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def aggregate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Agregasi item q1..q11 menjadi 7 kolom fitur via **rata-rata** (mean).

    Menjaga skala tetap 1..5 walau jumlah item beda (2 vs 1). Kolom target
    dipertahankan bila ada.
    """
    df = df.copy()
    out = pd.DataFrame(index=df.index)
    for feature, items in FEATURE_ITEM_MAP.items():
        cols = [c for c in items if c in df.columns]
        out[feature] = df[cols].mean(axis=1)
    if TARGET_COLUMN in df.columns:
        out[TARGET_COLUMN] = df[TARGET_COLUMN].values
    return out


def encode_target(df: pd.DataFrame, target_map: dict) -> pd.DataFrame:
    """Encode kelas target menjadi 0/1 (tidak teratur / teratur).

    Toleran bila target sudah numerik 0/1.
    """
    df = df.copy()
    if TARGET_COLUMN not in df.columns:
        return df
    if pd.api.types.is_numeric_dtype(df[TARGET_COLUMN]):
        df[TARGET_COLUMN] = df[TARGET_COLUMN].astype(int)
        return df
    df[TARGET_COLUMN] = (
        df[TARGET_COLUMN].map(lambda v: target_map.get(str(v).strip().lower(), None))
    )
    df[TARGET_COLUMN] = pd.to_numeric(df[TARGET_COLUMN], errors="coerce").astype("Int64")
    return df


def split_features_target(df: pd.DataFrame) -> tuple:
    """Pisahkan DataFrame menjadi (X, y) memakai FEATURE_COLUMNS & TARGET_COLUMN."""
    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].astype(int).copy()
    return X, y
