# Prediksi Keteraturan Haid Santriwati — *Decision Tree* (KDD)

Sistem *machine learning* klasifikasi biner untuk memprediksi **keteraturan haid**
(teratur / tidak teratur) santriwati berdasarkan jadwal & aktivitas harian, memakai
metode **Decision Tree** dengan alur **KDD** (*Knowledge Discovery in Database*).
Dilengkapi **UI web statis** (HTML/CSS/JS + Tailwind) yang menampilkan hasil pipeline.

- 📄 Spesifikasi teknis: [`SPESIFIKASI-SISTEM-PREDIKSI-HAID.md`](SPESIFIKASI-SISTEM-PREDIKSI-HAID.md)
- 🎨 Rancangan UI: [`RANCANGAN-UI-WEB.md`](RANCANGAN-UI-WEB.md)
- 🗺️ Rencana implementasi: [`RENCANA-IMPLEMENTASI.md`](RENCANA-IMPLEMENTASI.md)

> ⚠️ **Disclaimer:** keluaran sistem adalah **prediksi berbasis data, BUKAN diagnosis medis.**

---

## 🚀 TL;DR — Jalankan dari nol dalam 6 langkah

Dari akar proyek (`c:\code\prediksi_haid`):

```bash
# 1. Buat & aktifkan virtual environment
python -m venv .venv
.venv\Scripts\activate                 # Windows (Linux/macOS: source .venv/bin/activate)

# 2. Pasang dependensi + paket
pip install -r requirements.txt
pip install -e .

# 3. Siapkan data (pakai data sintetis dulu; ganti data asli kapan saja)
python scripts/generate_dummy_data.py  # -> data/raw/kuesioner_santriwati.csv

# 4. Latih model (cleaning + transform + split + train + evaluasi + ekspor UI)
python scripts/run_training.py

# 5. (opsional) Uji kualitas kode & unit test
pytest -q

# 6. Jalankan UI, lalu buka http://localhost:8000/ui/index.html
python -m http.server 8000
```

Selengkapnya di bawah.

---

## 1. Prasyarat

| Kebutuhan | Versi | Cara cek |
|---|---|---|
| **Python** | ≥ 3.11 | `python --version` |
| **pip** | terbaru | `pip --version` |
| **Git** (untuk clone/commit) | — | `git --version` |
| **Peramban modern** | — | Chrome/Edge/Firefox (untuk UI) |

Tidak butuh database, Node.js, atau framework web — UI cukup file statis + CDN.

---

## 2. Instalasi & Setup

### Cara cepat (skrip otomatis)

```bat
REM Windows — buat venv, pasang dependensi dev, editable install
scripts\setup.bat
```
```bash
# Linux / macOS
bash scripts/setup.sh
```

### Cara manual (langkah demi langkah)

```bash
# 1. Buat & aktifkan virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# 2. Perbarui pip
python -m pip install --upgrade pip

# 3. Pasang dependensi
pip install -r requirements.txt          # inti (pandas, scikit-learn, dst.)
# pip install -r requirements-dev.txt    # + alat dev (pytest, ruff, mypy, jupyter)

# 4. Pasang paket dalam mode editable agar "import prediksi_haid" berfungsi
pip install -e .

# 5. (opsional) salin konfigurasi lingkungan
copy .env.example .env        # Windows
# cp .env.example .env        # Linux/macOS
```

### Verifikasi instalasi

```bash
pytest -q          # seluruh unit test harus hijau
```

---

## 3. Menyiapkan Data Kuesioner

### 3.1 Skema data

Satu baris = satu responden. Kolom yang dibutuhkan (lihat contoh di
[`data/raw/contoh_kuesioner_santriwati.csv`](data/raw/contoh_kuesioner_santriwati.csv)):

| Kelompok | Kolom | Isi |
|---|---|---|
| Identitas | `responden_id`, `nama`, `usia`, `lama_mondok`, `tingkat_pendidikan` | ID anonim + metadata. `nama` **di-drop** sebelum latih (privasi). |
| Kuesioner | `q1` … `q15` | Jawaban Likert: `SS` / `S` / `N` / `TS` / `STS` (boleh juga angka 1–5). |
| Label | `keteraturan_haid` | `teratur` atau `tidak teratur` (boleh juga 1 / 0). |

Pemetaan variabel: `q1,q2`→jadwal · `q3,q4`→pola tidur · `q5,q6`→kelelahan · `q7`→stres ·
`q8,q9`→pola makan · `q10`→aktivitas · `q11`→istirahat · `q12–q15`→target. Detail: **SPESIFIKASI §4**.

### 3.2 Contoh isi CSV

```csv
responden_id,nama,usia,lama_mondok,tingkat_pendidikan,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,keteraturan_haid
S001,Santri A,16,3,MTs,S,SS,TS,N,S,S,SS,TS,N,S,TS,SS,S,N,S,tidak teratur
S002,Santri B,17,4,MA,N,S,S,S,TS,N,TS,S,S,N,S,S,SS,S,S,teratur
```

### 3.3 Dua cara menyiapkan dataset

**Opsi A — Data sintetis (untuk uji coba / demo, tanpa data asli):**

```bash
python scripts/generate_dummy_data.py            # 300 baris -> data/raw/kuesioner_santriwati.csv
python scripts/generate_dummy_data.py -n 500     # jumlah lain
```
Generator sengaja menyisipkan sedikit *missing value* & duplikat agar tahap **cleaning**
benar-benar teruji.

**Opsi B — Data asli:**
Simpan CSV kuesioner asli sebagai **`data/raw/kuesioner_santriwati.csv`**
(nama & path sesuai `config/config.yaml`). Tidak perlu ubah kode — cukup timpa file ini.

> Unduh **template kosong** berisi header yang benar dari tombol *Template CSV* di
> halaman **Data Santriwati** pada UI.

---

## 4. Menjalankan Pipeline (Cleaning → Training → Evaluasi)

Satu perintah menjalankan seluruh alur KDD:

```bash
python scripts/run_training.py --config config/config.yaml
```

Tahapan yang dijalankan otomatis (**SPESIFIKASI §12**):

| Tahap KDD | Yang terjadi | Keluaran |
|---|---|---|
| 1. Data Selection | muat `data/raw/kuesioner_santriwati.csv` | — |
| 2. **Cleaning** | buang *missing value* & duplikat | jumlah baris menyusut |
| 3. Transformation | Likert→angka, agregasi rata-rata, target→0/1 | `data/processed/dataset_encoded.csv` |
| 4. Split 80:20 | *stratified*, `random_state=42` | `X_train/X_test/y_train/y_test.csv` |
| 5. **Training** | latih Decision Tree | `models/decision_tree_model.joblib` |
| 6. Evaluation | akurasi, precision, recall, F1, ROC-AUC, confusion matrix | `reports/metrik_evaluasi.json` |
| 7. Visualization | render 4 grafik | `reports/figures/*.png` |
| 8. Ekspor UI | ringkasan, importance, data, aturan pohon, data uji | `reports/*.json` |

Contoh keluaran ringkas di terminal:

```
Pelatihan selesai: {'model_path': 'models/decision_tree_model.joblib',
 'n_train': 225, 'n_test': 57, 'accuracy': 0.60, 'f1_score': 0.49, 'roc_auc': 0.61}
```

> ℹ️ Dengan **data sintetis**, akurasi wajar berkisar ~0.6 (sinyalnya lemah karena acak).
> Angka akan bermakna setelah dataset asli dipakai.

### Mengubah parameter model

Semua parameter ada di [`config/config.yaml`](config/config.yaml) — **tidak** perlu ubah kode.
Contoh yang sering disetel: `decision_tree.criterion` (`gini`/`entropy`),
`decision_tree.max_depth` (default `3`, membatasi agar tak *overfitting*),
`split.test_size` (default `0.20`), `preprocessing.missing_strategy` (`drop`/`median`/`mode`),
`preprocessing.balance_method` (`none`/`smote`/`undersample`).

### Evaluasi ulang & prediksi data baru

```bash
# Evaluasi model tersimpan pada data uji (mencetak metrik)
python scripts/run_evaluation.py --config config/config.yaml

# Prediksi CSV baru (format kolom q1..q15 seperti data latih, tanpa perlu label)
python scripts/run_prediction.py --input data/raw/kuesioner_santriwati.csv --output reports/hasil.csv
```

Argumen CLI standar: `--config`, `--input`, `--output`, `--model-path`, `--verbose`.

---

## 5. Menjalankan UI Web

UI membaca berkas JSON/PNG dari `reports/` via `fetch()`, sehingga **harus** dilayani
lewat server statis (bukan dibuka langsung sebagai `file://`):

```bash
# dari akar proyek, setelah pipeline dijalankan (langkah 4)
python -m http.server 8000
# lalu buka:  http://localhost:8000/ui/index.html
```

Halaman yang tersedia:

| Halaman | Isi | Sumber data |
|---|---|---|
| **Dashboard** | kartu statistik + donat distribusi + bar feature importance | `ringkasan.json`, `feature_importance.json` |
| **Data Santriwati** | tabel dataset (ID anonim + 7 skor + status) | `data_santriwati.json` |
| **Proses D-Tree** | form parameter + generator perintah latih | — |
| **Pengujian** | prediksi kasus baru (geser 7 skor) — ditelusuri di browser | `aturan_pohon.json` |
| **Evaluasi Model** | metrik + confusion matrix + pohon/ROC | `metrik_evaluasi.json`, `figures/*.png` |

Alur ideal saat demo/sidang: **Data → Proses → Pengujian → Evaluasi**.
Fitur lain: mode gelap (ikon di kanan atas), responsif, disclaimer non-medis.

> **Demo cepat prediksi:** buka `http://localhost:8000/ui/pengujian.html#demo` — sliders
> terisi profil contoh dan prediksi langsung berjalan.

---

## 6. Pengujian (Testing) & Kualitas Kode

```bash
pytest -q              # jalankan seluruh unit test (data_loader s.d. web_export)
pytest -q -k model     # jalankan sebagian (mis. hanya test model)

ruff check .           # linter
ruff format .          # formatter (alternatif: black .)
mypy                   # pemeriksaan tipe statis
```

Tes mencakup tiap tahap KDD + ekspor UI. Konvensi kode PEP 8: `snake_case`
(fungsi/variabel), `PascalCase` (kelas), `UPPER_SNAKE_CASE` (konstanta). Lihat **SPESIFIKASI §9**.

---

## 7. Struktur Proyek

```text
prediksi_haid/
├── config/config.yaml         # semua parameter & path (SPESIFIKASI §6)
├── data/
│   ├── raw/                   # kuesioner mentah (+ contoh_kuesioner_santriwati.csv)
│   ├── interim/               # data bersih
│   └── processed/             # dataset final (X/y train/test + dataset_encoded)
├── models/                    # model .joblib (hasil latih)
├── reports/
│   ├── figures/               # PNG: pohon, confusion matrix, ROC, importance
│   ├── metrik_evaluasi.json   # metrik evaluasi
│   └── *.json                 # ekspor UI (ringkasan, importance, data, aturan_pohon, data_uji)
├── notebooks/                 # EDA (01_eksplorasi_data.ipynb)
├── src/prediksi_haid/         # PAKET UTAMA (satu modul per tahap KDD)
│   ├── config.py  constants.py
│   ├── data_loader.py  preprocessing.py  transformation.py
│   ├── dataset_splitter.py  model.py  evaluation.py  visualization.py
│   ├── predictor.py  pipeline.py  web_export.py
├── scripts/                   # CLI: generate_dummy_data, run_training/evaluation/prediction, setup
├── tests/                     # pytest
└── ui/                        # UI WEB STATIS (HTML/CSS/JS + Tailwind & Chart.js via CDN)
    ├── index.html  santriwati.html  proses.html  pengujian.html  evaluasi.html  login.html
    └── assets/  (theme.js, style.css, app.js)
```

> Data mentah, model, dan berkas di `reports/` **tidak** di-commit (lihat `.gitignore`) —
> semuanya dihasilkan ulang oleh pipeline. Yang di-commit: kode, tes, UI, konfigurasi,
> template contoh, dan dokumentasi.

---

## 8. Status Implementasi

- [x] Struktur proyek, dependensi, konfigurasi, konstanta
- [x] Modul KDD lengkap (`data_loader` … `pipeline`) — pipeline berjalan end-to-end
- [x] CLI: generate data, training, evaluation, prediction
- [x] Visualisasi PNG (pohon, confusion matrix, ROC, feature importance)
- [x] Generator data sintetis + unit test (31 tes hijau) + lolos `ruff`
- [x] Ekspor artefak UI (`web_export`) + prediksi pohon di browser
- [x] UI web modern (6 halaman, mode gelap) menampilkan hasil pipeline nyata
- [ ] Dataset asli ± 300 responden (cukup timpa `data/raw/kuesioner_santriwati.csv`)

---

*Lokasi studi: Pondok Pesantren Annuqayah, Guluk-Guluk, Sumenep. Batasan: hanya faktor
jadwal/aktivitas; tidak mencakup faktor medis/hormonal.*
