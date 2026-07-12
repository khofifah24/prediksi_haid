"""Orkestrasi end-to-end KDD (pipeline.py).

Menyatukan seluruh tahap: Data Selection -> Preprocessing -> Transformation
-> Split -> Training -> Evaluation -> Visualization.
Signature acuan: SPESIFIKASI §8.10 & §12.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd

from . import (
    data_loader,
    dataset_splitter,
    evaluation,
    preprocessing,
    transformation,
    visualization,
    web_export,
)
from . import (
    model as model_mod,
)
from .constants import (
    FEATURE_COLUMNS,
    IDENTITY_COLUMNS,
    LIKERT_ITEM_COLUMNS,
    LIKERT_MAP,
    TARGET_COLUMN,
    TARGET_LABELS,
    TARGET_MAP,
)


def _prepare_encoded(df_raw: pd.DataFrame, config: dict[str, Any]) -> pd.DataFrame:
    """KDD-1..3: seleksi -> cleaning -> Likert encode -> agregasi -> target encode.

    Kembalikan DataFrame berisi 7 kolom fitur numerik + target 0/1.
    """
    pre = config.get("preprocessing", {})

    data_loader.validate_schema(df_raw)
    keep = [*IDENTITY_COLUMNS, *LIKERT_ITEM_COLUMNS, TARGET_COLUMN]
    df = data_loader.select_relevant_columns(df_raw, keep)

    # KDD-2 Preprocessing
    if pre.get("drop_duplicates", True):
        df = preprocessing.drop_duplicate_rows(df)
    df = preprocessing.clean_missing_values(df, pre.get("missing_strategy", "drop"))

    # KDD-3 Transformation
    df = transformation.encode_likert(df, LIKERT_MAP)
    df = transformation.aggregate_indicators(df)   # -> 7 fitur (mean) + target
    df = transformation.encode_target(df, TARGET_MAP)
    df = df.dropna(subset=[TARGET_COLUMN]).reset_index(drop=True)
    return df


def run_training_pipeline(config: dict[str, Any]) -> dict[str, Any]:
    """Jalankan KDD-1..5, latih & simpan model, ekspor metrik + gambar.

    Kembalikan ringkasan hasil (path model & nilai metrik utama).
    """
    paths = config["paths"]
    split_cfg = config.get("split", {})
    pre = config.get("preprocessing", {})

    # --- KDD-1..3
    df_raw = data_loader.load_dataset(paths["raw_data"])
    df_encoded = _prepare_encoded(df_raw, config)

    # Simpan dataset ter-encode (jejak audit KDD)
    Path(paths["processed_dir"]).mkdir(parents=True, exist_ok=True)
    df_encoded.to_csv(Path(paths["processed_dir"]) / "dataset_encoded.csv", index=False)

    X, y = transformation.split_features_target(df_encoded)

    # Balancing opsional (sebelum split agar tidak membocorkan data uji? -> di train saja)
    # Di sini balancing diterapkan setelah split untuk mencegah kebocoran.

    # --- KDD Split 80:20
    stratify = y if split_cfg.get("stratify", True) else None
    X_train, X_test, y_train, y_test = dataset_splitter.split_train_test(
        X, y,
        test_size=split_cfg.get("test_size", 0.20),
        random_state=split_cfg.get("random_state", 42),
        stratify=stratify,
    )

    balance = pre.get("balance_method", "none")
    if balance not in (None, "none"):
        X_train, y_train = preprocessing.balance_dataset(X_train, y_train, balance)

    dataset_splitter.save_splits((X_train, X_test, y_train, y_test), paths["processed_dir"])

    # --- KDD-4 Training
    model = model_mod.build_model(config.get("decision_tree", {}))
    model = model_mod.train_model(model, X_train, y_train)
    model_mod.save_model(model, paths["model_output"])
    importance = model_mod.get_feature_importance(model, FEATURE_COLUMNS)

    # --- KDD-5 Evaluation
    metrics = evaluation.evaluate_model(model, X_test, y_test)
    metrics["support_train"] = int(len(y_train))
    evaluation.export_metrics(metrics, str(Path(paths["reports_dir"]) / "metrik_evaluasi.json"))

    # --- Visualization
    fig = Path(paths["figures_dir"])
    visualization.plot_decision_tree(
        model, FEATURE_COLUMNS, TARGET_LABELS, str(fig / "pohon_keputusan.png")
    )
    visualization.plot_confusion_matrix(
        metrics["confusion_matrix"], TARGET_LABELS, str(fig / "confusion_matrix.png")
    )
    visualization.plot_roc_curve(model, X_test, y_test, str(fig / "kurva_roc.png"))
    visualization.plot_feature_importance(importance, str(fig / "feature_importance.png"))

    # --- Ekspor artefak untuk UI statis (§11.1)
    reports = Path(paths["reports_dir"])
    test_size = split_cfg.get("test_size", 0.20)
    web_export.export_ringkasan(
        {
            "total_data": int(len(df_encoded)),
            "jumlah_teratur": int((y == 1).sum()),
            "jumlah_tidak_teratur": int((y == 0).sum()),
            "akurasi": metrics["accuracy"],
            "tanggal_latih": date.today().isoformat(),
            "rasio_split": f"{int((1 - test_size) * 100)}:{int(test_size * 100)}",
        },
        str(reports / "ringkasan.json"),
    )
    web_export.export_feature_importance(importance, str(reports / "feature_importance.json"))
    web_export.export_data_santriwati(df_encoded, str(reports / "data_santriwati.json"))
    web_export.export_aturan_pohon(model, FEATURE_COLUMNS, str(reports / "aturan_pohon.json"))

    y_pred_test = model.predict(X_test)
    test_ids = None
    if "responden_id" in df_encoded:
        test_ids = df_encoded.loc[X_test.index, "responden_id"]
    web_export.export_data_uji(test_ids, y_test, y_pred_test, str(reports / "data_uji.json"))

    return {
        "model_path": paths["model_output"],
        "n_train": int(len(y_train)),
        "n_test": int(len(y_test)),
        "accuracy": metrics["accuracy"],
        "f1_score": metrics["f1_score"],
        "roc_auc": metrics["roc_auc"],
    }


def run_prediction_pipeline(config: dict[str, Any], input_data) -> pd.Series:
    """Muat model tersimpan lalu klasifikasi ``input_data`` -> Series label 0/1.

    ``input_data`` boleh path CSV mentah atau DataFrame. Data diproses melalui
    tahap KDD-1..3 yang sama seperti saat latih (tanpa perlu kolom target).
    """
    from . import predictor

    paths = config["paths"]
    model = model_mod.load_model(paths["model_output"])

    if isinstance(input_data, str):
        df_raw = data_loader.load_dataset(input_data)
    else:
        df_raw = input_data.copy()

    # Transform tanpa mensyaratkan target
    df = transformation.encode_likert(df_raw, LIKERT_MAP)
    df = transformation.aggregate_indicators(df)
    pre = config.get("preprocessing", {})
    df = preprocessing.clean_missing_values(df, pre.get("missing_strategy", "drop"))

    return predictor.predict_batch(model, df)
