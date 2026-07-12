"""Visualisasi (visualization.py) — pohon, confusion matrix, feature importance.

Menyimpan gambar PNG ke ``reports/figures/``. Memakai backend non-interaktif
(``Agg``) agar aman dijalankan headless / dari CLI. Signature acuan: §8.8.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # backend headless — harus sebelum import pyplot

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import seaborn as sns  # noqa: E402
from sklearn.tree import plot_tree  # noqa: E402


def _ensure_parent(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def plot_decision_tree(model, feature_names, class_names, output_path: str) -> None:
    """Render & simpan visualisasi pohon keputusan (PNG)."""
    _ensure_parent(output_path)
    fig, ax = plt.subplots(figsize=(20, 12))
    plot_tree(
        model,
        feature_names=list(feature_names),
        class_names=list(class_names),
        filled=True,
        rounded=True,
        fontsize=8,
        ax=ax,
    )
    fig.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def plot_confusion_matrix(cm, labels, output_path: str) -> None:
    """Render heatmap confusion matrix (PNG)."""
    _ensure_parent(output_path)
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(
        np.asarray(cm),
        annot=True,
        fmt="d",
        cmap="Greens",
        xticklabels=list(labels),
        yticklabels=list(labels),
        ax=ax,
    )
    ax.set_xlabel("Prediksi")
    ax.set_ylabel("Aktual")
    ax.set_title("Confusion Matrix")
    fig.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def plot_feature_importance(importance_df, output_path: str) -> None:
    """Render bar chart feature importance (PNG). Kolom: fitur, importance."""
    _ensure_parent(output_path)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(
        data=importance_df,
        x="importance",
        y="fitur",
        hue="fitur",
        legend=False,
        palette="viridis",
        ax=ax,
    )
    ax.set_title("Feature Importance")
    fig.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
