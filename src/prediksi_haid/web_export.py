"""Ekspor artefak untuk UI statis (web_export.py) — OPSIONAL.

UI web (HTML/CSS/JS) tidak memakai backend; ia membaca berkas JSON/PNG dari
folder ``reports/``. Modul ini hanya menulis JSON (``json.dump``) — tidak
menambah dependensi web apa pun. Acuan: SPESIFIKASI §11.1 & RANCANGAN-UI-WEB.md.
"""

from __future__ import annotations

from typing import Any


def export_ringkasan(summary: dict[str, Any], path: str) -> None:
    """Tulis ringkasan Dashboard -> reports/ringkasan.json.

    Isi: total data, jumlah per kelas, tanggal & rasio latih terakhir.
    """
    raise NotImplementedError("TODO: json.dump(summary, ...)")


def export_feature_importance(importance_df, path: str) -> None:
    """Tulis daftar {fitur, skor} terurut -> reports/feature_importance.json."""
    raise NotImplementedError("TODO: export feature importance ke JSON")


def export_data_santriwati(df, path: str) -> None:
    """Tulis baris dataset (ID anonim + 7 skor + status) -> reports/data_santriwati.json."""
    raise NotImplementedError("TODO: export data santriwati ke JSON")


def export_aturan_pohon(model, feature_names: list[str], path: str) -> None:
    """Ekspor aturan if-else pohon -> reports/aturan_pohon.json.

    Dipakai halaman Pengujian agar prediksi kasus baru bisa berjalan di browser
    (JavaScript menelusuri aturan; tanpa server).
    """
    raise NotImplementedError("TODO: serialisasi struktur pohon ke JSON")


def export_data_uji(y_true, y_pred, path: str) -> None:
    """Tulis 20% data uji + label aktual & prediksi -> reports/data_uji.json."""
    raise NotImplementedError("TODO: export data uji ke JSON")
