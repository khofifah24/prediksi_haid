"""KDD-2 Preprocessing (preprocessing.py).

Pembersihan data: missing value, duplikat, seleksi fitur, balancing.
Signature acuan: SPESIFIKASI §8.3.
"""

from __future__ import annotations

import pandas as pd

from .constants import RANDOM_STATE


def clean_missing_values(df: pd.DataFrame, strategy: str) -> pd.DataFrame:
    """Tangani nilai kosong.

    ``strategy``:
        - "drop"   : buang baris yang memuat nilai kosong.
        - "median" : isi kolom numerik dengan median (kolom non-numerik: modus).
        - "mode"   : isi seluruh kolom dengan modus (nilai paling sering).
    """
    df = df.copy()
    if strategy == "drop":
        return df.dropna().reset_index(drop=True)

    if strategy == "median":
        for col in df.columns:
            if df[col].isna().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].median())
                else:
                    df[col] = df[col].fillna(_mode_or_none(df[col]))
        return df

    if strategy == "mode":
        for col in df.columns:
            if df[col].isna().any():
                df[col] = df[col].fillna(_mode_or_none(df[col]))
        return df

    raise ValueError(f"Strategi missing tidak dikenal: {strategy!r}")


def _mode_or_none(series: pd.Series):
    """Modus pertama; None bila kosong seluruhnya."""
    modes = series.mode(dropna=True)
    return modes.iloc[0] if not modes.empty else None


def drop_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Buang baris duplikat (identik penuh)."""
    return df.drop_duplicates().reset_index(drop=True)


def select_features(df: pd.DataFrame, feature_columns: list[str]) -> pd.DataFrame:
    """Seleksi kolom fitur untuk pemodelan."""
    return df[list(feature_columns)].copy()


def balance_dataset(X: pd.DataFrame, y: pd.Series, method: str) -> tuple:
    """Seimbangkan kelas. ``method``: "none" | "smote" | "undersample". -> (X, y).

    SMOTE & undersample memerlukan ``imbalanced-learn`` (impor lokal agar tidak
    menjadi dependensi wajib).
    """
    if method in (None, "none"):
        return X, y

    if method == "smote":
        from imblearn.over_sampling import SMOTE

        return SMOTE(random_state=RANDOM_STATE).fit_resample(X, y)

    if method == "undersample":
        from imblearn.under_sampling import RandomUnderSampler

        return RandomUnderSampler(random_state=RANDOM_STATE).fit_resample(X, y)

    raise ValueError(f"Metode balancing tidak dikenal: {method!r}")
