"""Smoke test: pastikan paket & konstanta ter-impor dengan benar.

Jalankan: pytest -q
Test skema ini lolos bahkan sebelum modul KDD diimplementasikan, sehingga
memastikan lingkungan & struktur proyek sudah benar sejak awal.
"""

from prediksi_haid import constants


def test_feature_columns_ada_tujuh():
    assert len(constants.FEATURE_COLUMNS) == 7


def test_likert_item_columns_ada_lima_belas():
    assert constants.LIKERT_ITEM_COLUMNS == [f"q{i}" for i in range(1, 16)]


def test_likert_map_lengkap():
    assert constants.LIKERT_MAP == {"SS": 5, "S": 4, "N": 3, "TS": 2, "STS": 1}


def test_target_labels_urut_indeks():
    # indeks 0 -> Tidak Teratur, indeks 1 -> Teratur
    assert constants.TARGET_LABELS[0] == "Tidak Teratur"
    assert constants.TARGET_LABELS[1] == "Teratur"
