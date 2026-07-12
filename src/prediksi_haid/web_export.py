"""Ekspor artefak untuk UI statis (web_export.py).

UI web (HTML/CSS/JS) tidak memakai backend; ia membaca berkas JSON/PNG dari
folder ``reports/``. Modul ini hanya menulis JSON (``json.dump``) — tidak
menambah dependensi web apa pun. Acuan: SPESIFIKASI §11.1 & RANCANGAN-UI-WEB.md.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .constants import TARGET_LABELS


def _dump(obj: Any, path: str) -> None:
    """Tulis ``obj`` ke JSON (UTF-8, indent 2), buat folder bila perlu."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def export_ringkasan(summary: dict[str, Any], path: str) -> None:
    """Tulis ringkasan Dashboard -> reports/ringkasan.json.

    Isi: total data, jumlah per kelas, akurasi, tanggal & rasio latih terakhir.
    """
    _dump(summary, path)


def export_feature_importance(importance_df, path: str) -> None:
    """Tulis daftar {fitur, skor} terurut -> reports/feature_importance.json.

    ``importance_df`` DataFrame berkolom ``fitur`` & ``importance`` (dari
    ``model.get_feature_importance``).
    """
    records = [
        {"fitur": str(row["fitur"]), "skor": round(float(row["importance"]), 4)}
        for _, row in importance_df.iterrows()
    ]
    _dump(records, path)


def export_data_santriwati(df, path: str) -> None:
    """Tulis baris dataset (ID anonim + 7 skor + status) -> reports/data_santriwati.json.

    ``df`` mengandung ``responden_id``, 7 kolom fitur agregat, dan ``keteraturan_haid``
    (0/1). Nama/identitas lain sengaja TIDAK diekspor (privasi).
    """
    from .constants import FEATURE_COLUMNS, TARGET_COLUMN

    records = []
    for _, row in df.iterrows():
        rec: dict[str, Any] = {"responden_id": str(row.get("responden_id", ""))}
        for col in FEATURE_COLUMNS:
            rec[col] = round(float(row[col]), 2)
        rec["status"] = int(row[TARGET_COLUMN])
        records.append(rec)
    _dump(records, path)


def _node_to_dict(tree, node_id: int, feature_names: list[str]) -> dict[str, Any]:
    """Ubah satu simpul sklearn ``tree_`` menjadi dict if-else rekursif.

    Aturan sklearn: ``X[feature] <= threshold`` menuju anak kiri.
    """
    left = int(tree.children_left[node_id])
    right = int(tree.children_right[node_id])

    if left == right:  # daun (keduanya -1)
        counts = tree.value[node_id][0]
        total = float(counts.sum())
        label = int(counts.argmax())
        conf = float(counts.max() / total) if total else 0.0
        return {
            "leaf": True,
            "label": label,
            "label_teks": TARGET_LABELS[label],
            "confidence": round(conf, 4),
            "samples": int(total),
        }

    return {
        "feature": feature_names[int(tree.feature[node_id])],
        "threshold": round(float(tree.threshold[node_id]), 4),
        "left": _node_to_dict(tree, left, feature_names),
        "right": _node_to_dict(tree, right, feature_names),
    }


def export_aturan_pohon(model, feature_names: list[str], path: str) -> None:
    """Ekspor aturan if-else pohon -> reports/aturan_pohon.json.

    Dipakai halaman Pengujian agar prediksi kasus baru bisa berjalan di browser
    (JavaScript menelusuri aturan; tanpa server).
    """
    root = _node_to_dict(model.tree_, 0, list(feature_names))
    _dump(root, path)


def export_data_uji(ids, y_true, y_pred, path: str) -> None:
    """Tulis data uji + label aktual & prediksi -> reports/data_uji.json.

    Setiap baris: ``{index, aktual, prediksi, benar}``. ``ids`` boleh None
    (pakai indeks urut). Berguna untuk Tab "Uji Data Testing".
    """
    y_true = list(y_true)
    y_pred = list(y_pred)
    ids = list(ids) if ids is not None else list(range(len(y_true)))
    records = []
    for i, (a, p) in enumerate(zip(y_true, y_pred, strict=False)):
        records.append({
            "id": str(ids[i]),
            "aktual": int(a),
            "aktual_teks": TARGET_LABELS[int(a)],
            "prediksi": int(p),
            "prediksi_teks": TARGET_LABELS[int(p)],
            "benar": bool(int(a) == int(p)),
        })
    summary = {
        "total": len(records),
        "benar": sum(1 for r in records if r["benar"]),
        "salah": sum(1 for r in records if not r["benar"]),
        "rows": records,
    }
    _dump(summary, path)
