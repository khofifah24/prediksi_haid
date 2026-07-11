"""KDD-5 Evaluation (evaluation.py).

Hitung metrik, confusion matrix, ROC/AUC; ekspor ke JSON.
Signature acuan: SPESIFIKASI §8.7 & §11.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from .constants import TARGET_LABELS

POS_LABEL = 1


def evaluate_model(model, X_test, y_test) -> dict:
    """Hitung accuracy/precision/recall/f1/roc_auc + confusion_matrix -> dict.

    Kunci mengikuti SPESIFIKASI §11 sehingga langsung cocok untuk
    ``reports/metrik_evaluasi.json``.
    """
    y_pred = model.predict(X_test)
    cm = build_confusion_matrix(y_test, y_pred)

    metrics: dict = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, pos_label=POS_LABEL, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, pos_label=POS_LABEL, zero_division=0)),
        "f1_score": float(f1_score(y_test, y_pred, pos_label=POS_LABEL, zero_division=0)),
        "roc_auc": compute_roc_auc(model, X_test, y_test),
        "confusion_matrix": cm.tolist(),
        "support_test": int(len(y_test)),
        "labels": TARGET_LABELS,
    }
    return metrics


def build_confusion_matrix(y_true, y_pred) -> np.ndarray:
    """Bangun confusion matrix 2x2 (baris=aktual, kolom=prediksi; label [0,1])."""
    return confusion_matrix(y_true, y_pred, labels=[0, 1])


def compute_roc_auc(model, X_test, y_test) -> float:
    """Hitung ROC-AUC dari probabilitas kelas positif.

    Mengembalikan ``nan`` bila hanya satu kelas hadir di ``y_test`` (AUC takdefinisi).
    """
    if len(np.unique(y_test)) < 2:
        return float("nan")
    if hasattr(model, "predict_proba"):
        y_score = model.predict_proba(X_test)[:, 1]
    else:  # fallback
        y_score = model.predict(X_test)
    return float(roc_auc_score(y_test, y_score))


def export_metrics(metrics: dict, path: str) -> None:
    """Tulis dict metrik ke ``reports/metrik_evaluasi.json`` (UTF-8, indent 2)."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
