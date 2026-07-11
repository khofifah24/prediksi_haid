# Rencana Implementasi — Sistem Prediksi Keteraturan Haid (Decision Tree / KDD)

> Dokumen perencanaan langkah demi langkah untuk mengisi logika modul yang saat ini
> masih berupa kerangka (`NotImplementedError`). Melengkapi
> [`SPESIFIKASI-SISTEM-PREDIKSI-HAID.md`](SPESIFIKASI-SISTEM-PREDIKSI-HAID.md) dan
> [`RANCANGAN-UI-WEB.md`](RANCANGAN-UI-WEB.md).

## Keputusan Desain (disepakati)

| Aspek | Keputusan | Alasan |
|---|---|---|
| **Data pengembangan** | Generator **data sintetis ± 300 baris** (sesuai skema q1–q15 + target) | Pipeline bisa diuji end-to-end sekarang; cukup ganti CSV saat data asli tiba |
| **Cakupan tahap ini** | **Pipeline Python dulu** (data_loader → pipeline + CLI + tests) | UI wiring (`web_export` + JS prediksi) dijadwalkan sebagai fase terpisah |
| **Agregasi indikator** | **Rata-rata (mean)** item per variabel | Semua fitur tetap di rentang 1–5 walau jumlah item beda (2 vs 1) |

> Data asli menyusul → semua kode ditulis agar **tidak tergantung** pada isi data, hanya pada
> **skema** (nama kolom di `constants.py`). Mengganti dataset = mengganti satu file CSV.

---

## Prinsip Kerja

1. **Test-driven per modul** — tiap modul KDD punya test unit; hapus `@pytest.mark.skip`
   begitu fungsi diisi, jalankan `pytest` untuk memvalidasi.
2. **Satu tahap KDD = satu modul** — jangan campur tanggung jawab (sesuai §7 spesifikasi).
3. **Config-driven** — tidak ada angka/path *hard-code*; semua dari `config/config.yaml`.
4. **Reproducible** — `random_state=42` di setiap titik acak (split, model, generator).
5. **Verifikasi bertahap** — jalankan pipeline setelah tiap modul selesai, bukan di akhir.

---

## Tahapan Implementasi

### FASE 0 — Alat Bantu Data Sintetis  *(prasyarat pengujian)*

**Tujuan:** menghasilkan dataset uji agar pipeline dapat dijalankan sebelum data asli ada.

- [ ] **0.1** Buat `scripts/generate_dummy_data.py`
  - Hasilkan ± 300 baris: identitas anonim + `q1`–`q15` (label Likert `SS/S/N/TS/STS`) + `keteraturan_haid` (`teratur`/`tidak teratur`).
  - Beri **korelasi lemah** yang masuk akal (mis. stres/kelelahan tinggi → cenderung "tidak teratur") supaya model belajar pola, bukan noise murni.
  - Sisipkan sedikit *missing value* & duplikat untuk menguji preprocessing.
  - `random_state=42`; tulis ke `data/raw/kuesioner_santriwati.csv`.
- [ ] **0.2** Verifikasi: `python scripts/generate_dummy_data.py` → file terbentuk, jumlah baris & kolom benar.

**Selesai bila:** CSV valid sesuai skema `constants.py` tersedia di `data/raw/`.

---

### FASE 1 — KDD-1 · Data Selection (`data_loader.py`)

- [ ] **1.1** `load_dataset(path)` — muat CSV (dan `.xlsx` via openpyxl bila ekstensi cocok) → `df_raw`.
- [ ] **1.2** `validate_schema(df)` — pastikan kolom wajib ada (`q1`–`q15` + `TARGET_COLUMN`); pesan error jelas bila kurang.
- [ ] **1.3** `select_relevant_columns(df, columns)` — ambil kolom relevan saja.
- [ ] **1.4** Test `tests/test_data_loader.py`: skema valid/invalid, kolom terseleksi.

**Selesai bila:** dapat memuat & memvalidasi CSV sintetis tanpa error.

---

### FASE 2 — KDD-2 · Preprocessing (`preprocessing.py`)

- [ ] **2.1** `clean_missing_values(df, strategy)` — dukung `"drop" | "median" | "mode"`.
- [ ] **2.2** `drop_duplicate_rows(df)`.
- [ ] **2.3** `select_features(df, feature_columns)`.
- [ ] **2.4** `balance_dataset(X, y, method)` — `"none"` (default), `"smote"` (imbalanced-learn), `"undersample"`.
- [ ] **2.5** Aktifkan & lengkapi `tests/test_preprocessing.py` (hapus skip): duplikat terbuang, missing tertangani, balancing mengubah distribusi.

**Selesai bila:** `df_clean` bebas duplikat/missing sesuai strategi config.

---

### FASE 3 — KDD-3 · Transformation (`transformation.py`)

- [ ] **3.1** `encode_likert(df, mapping)` — ubah `SS..STS` → `5..1` (`LIKERT_MAP`). Toleran bila sudah numerik.
- [ ] **3.2** `aggregate_indicators(df)` — **rata-rata** item per variabel via `FEATURE_ITEM_MAP` → 7 kolom fitur.
- [ ] **3.3** `encode_target(df, target_map)` — teks target → `0/1` (`TARGET_MAP`).
- [ ] **3.4** `split_features_target(df)` → `(X, y)`.
- [ ] **3.5** Aktifkan & lengkapi `tests/test_transformation.py`: encoding benar, agregasi = mean, target biner.

**Selesai bila:** `df_encoded` berisi 7 fitur numerik 1–5 + target 0/1; simpan ke `data/processed/dataset_encoded.csv`.

---

### FASE 4 — Split Data (`dataset_splitter.py`)

- [ ] **4.1** `split_train_test(X, y, test_size, random_state, stratify)` — `train_test_split` stratified 80:20.
- [ ] **4.2** `save_splits(splits, output_dir)` — tulis `X_train/X_test/y_train/y_test.csv` ke `data/processed/`.
- [ ] **4.3** Test `tests/test_dataset_splitter.py`: proporsi 80:20, stratifikasi menjaga rasio kelas.

**Selesai bila:** empat berkas split tersimpan dengan proporsi benar.

---

### FASE 5 — KDD-4 · Data Mining / Decision Tree (`model.py`)

- [ ] **5.1** `build_model(params)` — `DecisionTreeClassifier(**config['decision_tree'])`.
- [ ] **5.2** `train_model(model, X_train, y_train)` — `model.fit`.
- [ ] **5.3** `get_feature_importance(model, feature_names)` → DataFrame `{fitur, importance}` terurut.
- [ ] **5.4** `save_model(model, path)` / `load_model(path)` — joblib.
- [ ] **5.5** Aktifkan & lengkapi `tests/test_model.py`: model ter-fit, importance berjumlah ≈1, round-trip save/load.

**Selesai bila:** `models/decision_tree_model.joblib` terbentuk & bisa dimuat ulang.

---

### FASE 6 — KDD-5 · Evaluation (`evaluation.py`)

- [ ] **6.1** `evaluate_model(model, X_test, y_test)` → dict: accuracy, precision, recall, f1, roc_auc, confusion_matrix, support_train/test (kunci sesuai §11).
- [ ] **6.2** `build_confusion_matrix(y_true, y_pred)` → array 2×2.
- [ ] **6.3** `compute_roc_auc(model, X_test, y_test)` — dari `predict_proba`.
- [ ] **6.4** `export_metrics(metrics, path)` → `reports/metrik_evaluasi.json`.
- [ ] **6.5** Aktifkan & lengkapi `tests/test_evaluation.py`: bentuk confusion matrix, rentang metrik 0–1, JSON tertulis.

**Selesai bila:** `reports/metrik_evaluasi.json` berisi metrik nyata (bukan placeholder).

---

### FASE 7 — Visualisasi (`visualization.py`)

- [ ] **7.1** `plot_decision_tree(...)` → `reports/figures/pohon_keputusan.png` (`sklearn.tree.plot_tree`).
- [ ] **7.2** `plot_confusion_matrix(...)` → heatmap (seaborn) `confusion_matrix.png`.
- [ ] **7.3** `plot_roc_curve(...)` → `kurva_roc.png`.
- [ ] **7.4** `plot_feature_importance(...)` → `feature_importance.png`.
- [ ] **7.5** Gunakan backend non-interaktif (`matplotlib` `Agg`) agar aman dijalankan headless/CLI.

**Selesai bila:** empat PNG tersimpan di `reports/figures/`.

---

### FASE 8 — Inferensi (`predictor.py`)

- [ ] **8.1** `predict_single(model, features)` — dict 7 fitur → `0|1`.
- [ ] **8.2** `predict_batch(model, df)` — banyak baris → Series.
- [ ] **8.3** `label_prediction(pred)` — **sudah jadi** (`TARGET_LABELS`); tambahkan test.
- [ ] **8.4** Test `tests/test_predictor.py`: bentuk output & konsistensi label.

**Selesai bila:** prediksi kasus baru menghasilkan label yang benar.

---

### FASE 9 — Orkestrasi (`pipeline.py`) + CLI

- [ ] **9.1** `run_training_pipeline(config)` — rangkai FASE 1→7 berurutan (sesuai §12), kembalikan ringkasan (path model + metrik).
- [ ] **9.2** `run_prediction_pipeline(config, input_data)` — muat model → preprocessing/transform input → `predict_batch`.
- [ ] **9.3** Lengkapi `scripts/run_evaluation.py` (saat ini masih `NotImplementedError`).
- [ ] **9.4** Uji CLI: `run_training.py`, `run_evaluation.py`, `run_prediction.py` berjalan tuntas tanpa error.

**Selesai bila:** `python scripts/run_training.py` menjalankan seluruh KDD dari CSV → model + metrik + gambar dalam satu perintah.

---

### FASE 10 — Validasi Menyeluruh & Rapikan

- [ ] **10.1** `pytest -q` — seluruh test hijau (tidak ada lagi `skip`).
- [ ] **10.2** `ruff check .` & `ruff format .` (atau `black .`); `mypy` bersih pada `src/`.
- [ ] **10.3** Jalankan pipeline penuh pada data sintetis; periksa metrik masuk akal & gambar terbentuk.
- [ ] **10.4** Perbarui checklist "Status & Langkah Berikutnya" di `README.md`.

**Selesai bila:** pipeline end-to-end lolos test + lint, siap menerima data asli.

---

## Fase Lanjutan (di luar cakupan tahap ini)

- **FASE 11 — UI Wiring:** implementasi `web_export.py` (ekspor `ringkasan.json`,
  `feature_importance.json`, `data_santriwati.json`, `aturan_pohon.json`, `data_uji.json`)
  + logika `evaluateTree()` di `ui/pengujian.html` untuk prediksi di browser.
- **FASE 12 — Data Asli:** ganti `data/raw/kuesioner_santriwati.csv` dengan ± 300 responden nyata,
  latih ulang, dokumentasikan hasil untuk bab hasil skripsi.
- **Tuning (opsional):** eksplorasi `max_depth` / `ccp_alpha` untuk cegah overfitting.

---

## Peta Ketergantungan Antar-Fase

```
FASE 0 (data sintetis)
   │
   ▼
FASE 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8
   (data_loader → preprocessing → transformation → split → model → evaluation → viz → predictor)
                                     │
                                     ▼
                            FASE 9 (pipeline + CLI, merangkai semua)
                                     │
                                     ▼
                            FASE 10 (validasi + lint)
                                     │
                                     ▼
                     FASE 11 (UI) · FASE 12 (data asli)   ← fase lanjutan
```

Urutan wajib berurutan 1→9 (tiap fase memakai keluaran fase sebelumnya). FASE 0 harus
lebih dulu agar semua fase bisa diverifikasi dengan data nyata.

---

## Definition of Done (tahap ini)

- ✅ Semua modul di `src/prediksi_haid/` (kecuali `web_export.py`) terimplementasi, tanpa `NotImplementedError`.
- ✅ `pytest -q` hijau, tanpa test yang di-skip.
- ✅ Satu perintah `python scripts/run_training.py` menghasilkan model, `metrik_evaluasi.json`, dan 4 PNG.
- ✅ Kode lolos `ruff` & `mypy`; konsisten dengan konvensi §9 spesifikasi.
- ✅ Mengganti dataset cukup dengan menimpa satu file CSV — tanpa ubah kode.
