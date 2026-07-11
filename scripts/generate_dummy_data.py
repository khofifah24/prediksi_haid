"""FASE 0 — Generator data sintetis kuesioner santriwati.

Menghasilkan ~300 baris sesuai skema (q1..q15 Likert + target) untuk menguji
pipeline end-to-end SEBELUM data asli tersedia. Diberi korelasi lemah yang masuk
akal (stres/kelelahan tinggi -> cenderung "tidak teratur") plus sedikit
missing value & duplikat untuk menguji preprocessing.

Jalankan dari akar proyek:
    python scripts/generate_dummy_data.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from prediksi_haid.constants import LIKERT_ITEM_COLUMNS, TARGET_COLUMN  # noqa: E402

# Label Likert (indeks 0..4 -> STS..SS) untuk konversi kode numerik -> teks.
LIKERT_LABELS = ["STS", "TS", "N", "S", "SS"]
PENDIDIKAN = ["MTs", "MA", "SMP", "SMA"]


def _num_to_likert(value: int) -> str:
    """Kode numerik 1..5 -> label Likert STS..SS."""
    return LIKERT_LABELS[int(np.clip(value, 1, 5)) - 1]


def generate(n: int = 300, random_state: int = 42) -> pd.DataFrame:
    """Bangun DataFrame kuesioner sintetis berukuran ``n``."""
    rng = np.random.default_rng(random_state)

    # --- Faktor laten "risiko ketidakteraturan" (0..1) menyetir jawaban & target.
    risiko = rng.beta(2.0, 2.0, size=n)

    rows: list[dict] = []
    for i in range(n):
        r = risiko[i]

        def item(base_high_when_risky: bool, r: float = r) -> int:
            """Jawaban 1..5; berkorelasi dengan risiko bila diminta."""
            center = 1.0 + 4.0 * (r if base_high_when_risky else (1.0 - r))
            val = rng.normal(center, 0.9)
            return int(np.clip(round(val), 1, 5))

        row: dict[str, object] = {
            "responden_id": f"S{i + 1:03d}",
            "nama": f"Santri {i + 1:03d}",
            "usia": int(rng.integers(13, 20)),
            "lama_mondok": int(rng.integers(1, 7)),
            "tingkat_pendidikan": str(rng.choice(PENDIDIKAN)),
        }

        # q1,q2 jadwal padat; q3,q4 pola tidur buruk; q5,q6 kelelahan; q7 stres;
        # q8,q9 pola makan tak teratur; q10 aktivitas berat; q11 istirahat kurang.
        # Item yang "memburuk seiring risiko" -> base_high_when_risky=True.
        risky_items = {"q1", "q2", "q3", "q4", "q5", "q6", "q7", "q9", "q10", "q11"}
        for q in LIKERT_ITEM_COLUMNS:
            row[q] = _num_to_likert(item(q in risky_items))

        # Target: makin tinggi risiko -> makin mungkin "tidak teratur" (0).
        p_teratur = float(np.clip(1.0 - r + rng.normal(0, 0.08), 0.05, 0.95))
        teratur = rng.random() < p_teratur
        row[TARGET_COLUMN] = "teratur" if teratur else "tidak teratur"
        rows.append(row)

    df = pd.DataFrame(rows)

    # --- Sisipkan sedikit missing value (~2% pada beberapa item Likert).
    for q in ["q3", "q8", "q11"]:
        idx = rng.choice(n, size=max(1, int(0.02 * n)), replace=False)
        df.loc[idx, q] = np.nan

    # --- Sisipkan beberapa baris duplikat (~1%).
    dup = df.sample(max(1, int(0.01 * n)), random_state=random_state)
    df = pd.concat([df, dup], ignore_index=True)

    return df


def main() -> int:
    p = argparse.ArgumentParser(description="Generate data kuesioner sintetis.")
    p.add_argument("-n", "--rows", type=int, default=300, help="jumlah responden")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument(
        "-o", "--output",
        default="data/raw/kuesioner_santriwati.csv",
        help="path CSV keluaran",
    )
    args = p.parse_args()

    df = generate(args.rows, args.seed)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"OK: {len(df)} baris x {df.shape[1]} kolom -> {out}")
    print(df[TARGET_COLUMN].value_counts().to_dict())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
