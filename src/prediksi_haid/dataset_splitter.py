"""Pembagian data latih/uji 80:20 (dataset_splitter.py).

Signature acuan: SPESIFIKASI §8.5.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


def split_train_test(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float,
    random_state: int,
    stratify,
) -> tuple:
    """Bagi (X, y) menjadi (X_train, X_test, y_train, y_test).

    ``stratify`` berupa vektor label (mis. ``y``) agar proporsi kelas terjaga,
    atau ``None`` untuk split acak biasa.
    """
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify,
    )


def save_splits(splits: tuple, output_dir: str) -> None:
    """Simpan X_train/X_test/y_train/y_test ke ``output_dir`` sebagai CSV."""
    X_train, X_test, y_train, y_test = splits
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    X_train.to_csv(out / "X_train.csv", index=False)
    X_test.to_csv(out / "X_test.csv", index=False)
    y_train.to_frame(name=y_train.name or "target").to_csv(out / "y_train.csv", index=False)
    y_test.to_frame(name=y_test.name or "target").to_csv(out / "y_test.csv", index=False)
