"""Uji KDD-4 Model."""

import pandas as pd

from prediksi_haid import model as model_mod


def _toy_data():
    X = pd.DataFrame({"a": [1, 2, 3, 4, 5, 6], "b": [6, 5, 4, 3, 2, 1]})
    y = pd.Series([0, 0, 0, 1, 1, 1])
    return X, y


def test_build_model_criterion():
    m = model_mod.build_model({"criterion": "entropy", "max_depth": 3})
    assert m.criterion == "entropy"
    assert m.max_depth == 3
    assert m.random_state == 42  # default disisipkan


def test_train_and_importance():
    X, y = _toy_data()
    m = model_mod.train_model(model_mod.build_model({}), X, y)
    imp = model_mod.get_feature_importance(m, list(X.columns))
    assert set(imp["fitur"]) == {"a", "b"}
    assert abs(imp["importance"].sum() - 1.0) < 1e-6


def test_save_load_roundtrip(tmp_path):
    X, y = _toy_data()
    m = model_mod.train_model(model_mod.build_model({}), X, y)
    path = tmp_path / "m.joblib"
    model_mod.save_model(m, str(path))
    loaded = model_mod.load_model(str(path))
    assert list(loaded.predict(X)) == list(m.predict(X))
