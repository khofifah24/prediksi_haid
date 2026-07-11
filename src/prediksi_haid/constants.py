"""Konstanta & nama kolom terpusat (constants.py).

Semua *magic string* (nama kolom, pemetaan encoding, seed) dikumpulkan di
sini agar konsisten lintas modul. Acuan: SPESIFIKASI §4 & §5.
"""

from __future__ import annotations

# --- Kolom target (label) ---------------------------------------------------
TARGET_COLUMN: str = "keteraturan_haid"

# --- Kolom fitur (7 variabel penelitian, §4.2) ------------------------------
FEATURE_COLUMNS: list[str] = [
    "jadwal_kegiatan_harian",
    "pola_tidur",
    "tingkat_kelelahan",
    "tingkat_stres",
    "pola_makan",
    "aktivitas_harian",
    "waktu_istirahat",
]

# --- Kolom identitas (di-drop sebelum latih; privasi) -----------------------
IDENTITY_COLUMNS: list[str] = [
    "responden_id",
    "nama",
    "usia",
    "lama_mondok",
    "tingkat_pendidikan",
]

# --- Item kuesioner Likert mentah q1..q15 -----------------------------------
LIKERT_ITEM_COLUMNS: list[str] = [f"q{i}" for i in range(1, 16)]

# Peta item -> variabel agregat (untuk transformation.aggregate_indicators)
FEATURE_ITEM_MAP: dict[str, list[str]] = {
    "jadwal_kegiatan_harian": ["q1", "q2"],
    "pola_tidur": ["q3", "q4"],
    "tingkat_kelelahan": ["q5", "q6"],
    "tingkat_stres": ["q7"],
    "pola_makan": ["q8", "q9"],
    "aktivitas_harian": ["q10"],
    "waktu_istirahat": ["q11"],
}
# Item penyusun target (§4.3)
TARGET_ITEM_COLUMNS: list[str] = ["q12", "q13", "q14", "q15"]

# --- Pemetaan encoding (§4.4) -----------------------------------------------
LIKERT_MAP: dict[str, int] = {"SS": 5, "S": 4, "N": 3, "TS": 2, "STS": 1}
TARGET_MAP: dict[str, int] = {"teratur": 1, "tidak teratur": 0}

# Label terurut menurut indeks kelas (0 -> "Tidak Teratur", 1 -> "Teratur")
TARGET_LABELS: list[str] = ["Tidak Teratur", "Teratur"]

# --- Reproduksibilitas & split ----------------------------------------------
RANDOM_STATE: int = 42
TEST_SIZE: float = 0.20
