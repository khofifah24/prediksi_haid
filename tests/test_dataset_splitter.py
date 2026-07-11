"""Uji split 80:20 + pipeline latih end-to-end pada data sintetis kecil."""

import pandas as pd

from prediksi_haid import dataset_splitter
from prediksi_haid.constants import FEATURE_COLUMNS


def test_split_proportion_and_stratify():
    n = 100
    X = pd.DataFrame({c: list(range(n)) for c in FEATURE_COLUMNS})
    y = pd.Series([0] * 60 + [1] * 40)
    X_tr, X_te, y_tr, y_te = dataset_splitter.split_train_test(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    assert len(X_te) == 20
    assert len(X_tr) == 80
    # stratifikasi menjaga rasio ~60:40 di data uji
    assert y_te.mean() == 0.40


def test_save_splits(tmp_path):
    X = pd.DataFrame({c: [1, 2, 3, 4] for c in FEATURE_COLUMNS})
    y = pd.Series([0, 1, 0, 1], name="keteraturan_haid")
    dataset_splitter.save_splits((X, X, y, y), str(tmp_path))
    for name in ("X_train.csv", "X_test.csv", "y_train.csv", "y_test.csv"):
        assert (tmp_path / name).exists()
