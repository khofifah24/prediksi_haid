"""Entry-point CLI: prediksi data baru dengan model terlatih.

Contoh:
    python scripts/run_prediction.py --input data/baru.csv --output reports/hasil.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from prediksi_haid.config import load_config  # noqa: E402
from prediksi_haid.pipeline import run_prediction_pipeline  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Prediksi keteraturan haid data baru.")
    p.add_argument("--config", default="config/config.yaml", help="path config.yaml")
    p.add_argument("--input", required=True, help="path CSV data baru")
    p.add_argument("--output", default=None, help="path CSV hasil prediksi")
    p.add_argument("--verbose", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config(args.config)

    predictions = run_prediction_pipeline(config, args.input)
    if args.output:
        predictions.to_csv(args.output, index=False)
        print(f"Hasil disimpan ke {args.output}")
    else:
        print(predictions)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
