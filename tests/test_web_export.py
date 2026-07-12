"""Uji ekspor artefak UI (web_export.py)."""

import json

import pandas as pd

from prediksi_haid import model as model_mod
from prediksi_haid import web_export
from prediksi_haid.constants import FEATURE_COLUMNS, TARGET_COLUMN


def test_export_ringkasan(tmp_path):
    p = tmp_path / "ringkasan.json"
    web_export.export_ringkasan({"total_data": 300, "akurasi": 0.9}, str(p))
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["total_data"] == 300


def test_export_feature_importance(tmp_path):
    df = pd.DataFrame({"fitur": ["a", "b"], "importance": [0.7, 0.3]})
    p = tmp_path / "fi.json"
    web_export.export_feature_importance(df, str(p))
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data[0] == {"fitur": "a", "skor": 0.7}


def test_export_data_santriwati(tmp_path):
    row = {c: 3.0 for c in FEATURE_COLUMNS}
    row["responden_id"] = "S001"
    row[TARGET_COLUMN] = 1
    df = pd.DataFrame([row])
    p = tmp_path / "ds.json"
    web_export.export_data_santriwati(df, str(p))
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data[0]["responden_id"] == "S001"
    assert data[0]["status"] == 1
    assert "nama" not in data[0]  # identitas tidak diekspor


def test_export_aturan_pohon_traversable(tmp_path):
    X = pd.DataFrame({c: [1, 2, 3, 4, 5, 6] for c in FEATURE_COLUMNS})
    y = pd.Series([0, 0, 0, 1, 1, 1])
    m = model_mod.train_model(model_mod.build_model({"max_depth": 2}), X, y)
    p = tmp_path / "tree.json"
    web_export.export_aturan_pohon(m, FEATURE_COLUMNS, str(p))
    tree = json.loads(p.read_text(encoding="utf-8"))
    # Root harus punya feature/threshold, dan traversal berujung di daun berlabel 0/1.
    node = tree
    while not node.get("leaf"):
        assert node["feature"] in FEATURE_COLUMNS
        node = node["left"]
    assert node["label"] in (0, 1)


def test_export_data_uji(tmp_path):
    p = tmp_path / "uji.json"
    web_export.export_data_uji(["S1", "S2", "S3"], [1, 0, 1], [1, 1, 1], str(p))
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["total"] == 3
    assert data["benar"] == 2
    assert data["salah"] == 1
