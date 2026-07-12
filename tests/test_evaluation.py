"""Uji KDD-5 Evaluation."""

import numpy as np
import pandas as pd

from prediksi_haid import evaluation
from prediksi_haid import model as model_mod


def _fitted():
    X = pd.DataFrame({"a": [1, 2, 3, 4, 5, 6], "b": [6, 5, 4, 3, 2, 1]})
    y = pd.Series([0, 0, 0, 1, 1, 1])
    m = model_mod.train_model(model_mod.build_model({}), X, y)
    return m, X, y


def test_build_confusion_matrix_shape():
    cm = evaluation.build_confusion_matrix([0, 1, 0, 1], [0, 1, 1, 1])
    assert cm.shape == (2, 2)
    assert cm.sum() == 4


def test_evaluate_model_keys_and_range():
    m, X, y = _fitted()
    metrics = evaluation.evaluate_model(m, X, y)
    for k in ("accuracy", "precision", "recall", "f1_score"):
        assert k in metrics
        assert 0.0 <= metrics[k] <= 1.0 or np.isnan(metrics[k])
    assert "roc_auc" not in metrics  # ROC-AUC sengaja tidak dipakai
    assert np.array(metrics["confusion_matrix"]).shape == (2, 2)


def test_export_metrics(tmp_path):
    path = tmp_path / "metrik.json"
    evaluation.export_metrics({"accuracy": 0.9}, str(path))
    assert path.exists()
    assert '"accuracy"' in path.read_text(encoding="utf-8")
