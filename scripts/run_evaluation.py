"""Entry-point CLI: evaluasi model terlatih pada data uji tersimpan.

Contoh:
    python scripts/run_evaluation.py --config config/config.yaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pandas as pd  # noqa: E402

from prediksi_haid import evaluation  # noqa: E402
from prediksi_haid import model as model_mod
from prediksi_haid.config import load_config  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Evaluasi model Decision Tree.")
    p.add_argument("--config", default="config/config.yaml", help="path config.yaml")
    p.add_argument("--model-path", default=None, help="override path model .joblib")
    p.add_argument("--verbose", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config(args.config)
    if args.model_path:
        config["paths"]["model_output"] = args.model_path

    paths = config["paths"]
    processed = Path(paths["processed_dir"])

    model = model_mod.load_model(paths["model_output"])
    X_test = pd.read_csv(processed / "X_test.csv")
    y_test = pd.read_csv(processed / "y_test.csv").iloc[:, 0]

    metrics = evaluation.evaluate_model(model, X_test, y_test)
    out = Path(paths["reports_dir"]) / "metrik_evaluasi.json"
    evaluation.export_metrics(metrics, str(out))

    print(f"Metrik disimpan ke {out}")
    for k in ("accuracy", "precision", "recall", "f1_score"):
        print(f"  {k:10s}: {metrics[k]:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
