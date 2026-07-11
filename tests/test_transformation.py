"""Uji KDD-3 Transformation."""

import pandas as pd

from prediksi_haid import transformation
from prediksi_haid.constants import (
    FEATURE_COLUMNS,
    LIKERT_MAP,
    TARGET_COLUMN,
    TARGET_MAP,
)


def test_encode_likert():
    df = pd.DataFrame({"q1": ["SS", "S", "N", "TS", "STS"]})
    out = transformation.encode_likert(df, LIKERT_MAP)
    assert list(out["q1"]) == [5, 4, 3, 2, 1]


def test_aggregate_indicators_mean():
    # jadwal_kegiatan_harian = mean(q1, q2)
    df = pd.DataFrame({"q1": [4], "q2": [2]})
    out = transformation.aggregate_indicators(df)
    assert out.loc[0, "jadwal_kegiatan_harian"] == 3.0
    assert "tingkat_stres" in out.columns  # dari q7 (walau q7 tak ada -> NaN)


def test_encode_target():
    df = pd.DataFrame({TARGET_COLUMN: ["teratur", "tidak teratur"]})
    out = transformation.encode_target(df, TARGET_MAP)
    assert list(out[TARGET_COLUMN]) == [1, 0]


def test_split_features_target():
    data = {c: [3.0, 4.0] for c in FEATURE_COLUMNS}
    data[TARGET_COLUMN] = [1, 0]
    df = pd.DataFrame(data)
    X, y = transformation.split_features_target(df)
    assert list(X.columns) == FEATURE_COLUMNS
    assert list(y) == [1, 0]
