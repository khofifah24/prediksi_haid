"""Entry-point CLI: latih model dari data mentah.

Contoh:
    python scripts/run_training.py --config config/config.yaml --verbose

Argumen standar (§10): --config, --input, --output, --model-path, --verbose.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Pastikan paket src/ dapat diimpor saat dijalankan langsung.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from prediksi_haid.config import load_config  # noqa: E402
from prediksi_haid.pipeline import run_training_pipeline  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Latih model Decision Tree (KDD-1..5).")
    p.add_argument("--config", default="config/config.yaml", help="path config.yaml")
    p.add_argument("--input", default=None, help="override path CSV kuesioner mentah")
    p.add_argument("--model-path", default=None, help="override path output model .joblib")
    p.add_argument("--verbose", action="store_true", help="tampilkan log detail")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config(args.config)
    if args.input:
        config["paths"]["raw_data"] = args.input
    if args.model_path:
        config["paths"]["model_output"] = args.model_path

    result = run_training_pipeline(config)
    print("Pelatihan selesai:", result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
