"""Uji KDD-2 Preprocessing."""

import numpy as np
import pandas as pd

from prediksi_haid import preprocessing


def test_drop_duplicate_rows():
    df = pd.DataFrame({"a": [1, 1, 2], "b": [2, 2, 3]})
    out = preprocessing.drop_duplicate_rows(df)
    assert len(out) == 2


def test_clean_missing_drop():
    df = pd.DataFrame({"a": [1.0, np.nan, 3.0]})
    out = preprocessing.clean_missing_values(df, "drop")
    assert len(out) == 2


def test_clean_missing_median():
    df = pd.DataFrame({"a": [1.0, np.nan, 3.0]})
    out = preprocessing.clean_missing_values(df, "median")
    assert out["a"].isna().sum() == 0
    assert out.loc[1, "a"] == 2.0  # median dari [1, 3]


def test_select_features():
    df = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
    out = preprocessing.select_features(df, ["a", "c"])
    assert list(out.columns) == ["a", "c"]


def test_balance_none_no_change():
    X = pd.DataFrame({"f": [1, 2, 3, 4]})
    y = pd.Series([0, 0, 0, 1])
    Xo, yo = preprocessing.balance_dataset(X, y, "none")
    assert len(Xo) == len(X)
