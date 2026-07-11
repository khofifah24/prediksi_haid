"""KDD-1 Data Selection (data_loader.py).

Memuat dataset kuesioner mentah dan menyeleksi kolom relevan.
Signature acuan: SPESIFIKASI §8.2.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .constants import LIKERT_ITEM_COLUMNS, TARGET_COLUMN


def load_dataset(path: str) -> pd.DataFrame:
    """Muat CSV/XLSX kuesioner mentah menjadi DataFrame (``df_raw``).

    Raises:
        FileNotFoundError: bila berkas tidak ada.
        ValueError: bila ekstensi tidak didukung.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Berkas data tidak ditemukan: {p}")

    suffix = p.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(p)
    if suffix in (".xlsx", ".xls"):
        return pd.read_excel(p)
    raise ValueError(f"Ekstensi tidak didukung: {suffix} (pakai .csv atau .xlsx)")


def validate_schema(df: pd.DataFrame) -> bool:
    """Validasi keberadaan kolom wajib (q1..q15 + target).

    Raises:
        ValueError: bila ada kolom wajib yang hilang (pesan menyebut kolomnya).
    """
    required = [*LIKERT_ITEM_COLUMNS, TARGET_COLUMN]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Kolom wajib hilang: {missing}")
    return True


def select_relevant_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Ambil hanya kolom relevan (abaikan yang tidak ada di ``df``)."""
    available = [c for c in columns if c in df.columns]
    return df[available].copy()
