# Prediksi Keteraturan Haid Santriwati — *Decision Tree* (KDD)

Sistem *machine learning* klasifikasi biner untuk memprediksi **keteraturan haid**
(teratur / tidak teratur) santriwati berdasarkan jadwal & aktivitas harian, memakai
metode **Decision Tree** dengan alur **KDD**. Dilengkapi **UI web statis** (HTML/CSS/JS).

- 📄 Spesifikasi teknis: [`SPESIFIKASI-SISTEM-PREDIKSI-HAID.md`](SPESIFIKASI-SISTEM-PREDIKSI-HAID.md)
- 🎨 Rancangan UI: [`RANCANGAN-UI-WEB.md`](RANCANGAN-UI-WEB.md)

> ⚠️ **Disclaimer:** keluaran sistem adalah **prediksi berbasis data, BUKAN diagnosis medis.**

---

## 1. Prasyarat (yang perlu diinstal lebih dulu)

| Kebutuhan | Versi | Cara cek |
|---|---|---|
| **Python** | ≥ 3.11 | `python --version` |
| **pip** | terbaru | `pip --version` |
| **Git** (opsional) | — | `git --version` |

Tidak butuh database, Node.js, atau framework web — UI cukup file statis.

---

## 2. Instalasi & Setup

### Cara cepat (skrip otomatis)

```bat
REM Windows
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
pip install -r requirements.txt          # inti saja
# pip install -r requirements-dev.txt    # + alat dev (pytest, ruff, jupyter)

# 4. (opsional) pasang paket dalam mode editable agar "import prediksi_haid" jalan
pip install -e .

# 5. (opsional) salin konfigurasi lingkungan
copy .env.example .env        # Windows
# cp .env.example .env        # Linux/macOS
```

### Verifikasi instalasi

```bash
pytest -q          # harus lolos (smoke test struktur & konstanta)
```

---

## 3. Struktur Proyek

```
prediksi_haid/
├── config/config.yaml         # semua parameter & path (§6 spesifikasi)
├── data/
│   ├── raw/                   # kuesioner mentah (+ contoh_kuesioner_santriwati.csv)
│   ├── interim/               # data bersih
│   └── processed/             # dataset final (X/y train/test)
├── models/                    # model & encoder .joblib (hasil latih)
├── reports/
│   ├── figures/               # PNG: pohon, confusion matrix, ROC, importance
│   ├── metrik_evaluasi.json   # metrik evaluasi
│   └── *.json                 # ekspor untuk UI (ringkasan, importance, dst.)
├── notebooks/                 # EDA (01_eksplorasi_data.ipynb)
├── src/prediksi_haid/         # PAKET UTAMA (satu modul per tahap KDD)
│   ├── config.py  constants.py
│   ├── data_loader.py  preprocessing.py  transformation.py
│   ├── dataset_splitter.py  model.py  evaluation.py  visualization.py
│   ├── predictor.py  pipeline.py  web_export.py
├── scripts/                   # CLI: run_training/evaluation/prediction + setup
├── tests/                     # pytest
└── ui/                        # UI WEB STATIS (HTML/CSS/JS + Tailwind CDN)
    ├── index.html  santriwati.html  proses.html  pengujian.html  evaluasi.html
    ├── login.html
    └── assets/  (style.css, app.js)
```

> Modul di `src/prediksi_haid/` saat ini berisi **kerangka fungsi (signature) + `NotImplementedError`**.
> Isi logika tiap tahap KDD adalah pekerjaan implementasi berikutnya.

---

## 4. Cara Menjalankan

### A. Pipeline Python (latih → evaluasi → prediksi)

```bash
# Latih model dari data mentah (KDD-1..5), simpan model + metrik + gambar
python scripts/run_training.py --config config/config.yaml --verbose

# Evaluasi model pada data uji
python scripts/run_evaluation.py --config config/config.yaml

# Prediksi data baru
python scripts/run_prediction.py --input data/baru.csv --output reports/hasil.csv
```

Argumen CLI standar: `--config`, `--input`, `--output`, `--model-path`, `--verbose`.

### B. UI Web (statis)

UI membaca berkas JSON/PNG dari `reports/` via `fetch()`, jadi **harus** dilayani lewat
server statis (bukan dibuka `file://`):

```bash
# dari akar proyek
python -m http.server 8000
# lalu buka:  http://localhost:8000/ui/index.html
```

Alur pemakaian ideal (mis. saat demo): **Data → Proses → Pengujian → Evaluasi.**

> Berkas `reports/*.json` yang ada sekarang berisi **contoh/placeholder** agar UI bisa
> langsung tampil; nilainya ditimpa otomatis setelah pipeline Python dijalankan
> (`prediksi_haid.web_export`).

---

## 5. Menyiapkan Data

1. Siapkan CSV kuesioner sesuai skema (lihat `data/raw/contoh_kuesioner_santriwati.csv`):
   kolom identitas + `q1`–`q15` (Likert `SS/S/N/TS/STS`) + `keteraturan_haid`
   (`teratur` / `tidak teratur`).
2. Simpan sebagai `data/raw/kuesioner_santriwati.csv` (nama sesuai `config.yaml`).
3. Jalankan pelatihan (bagian 4A).

Detail skema: **SPESIFIKASI §4**.

---

## 6. Alur Kerja Pengembangan (Dev)

```bash
ruff check .        # linter
ruff format .       # formatter (atau: black .)
mypy                # cek tipe statis
pytest -q           # unit test
```

Konvensi kode: PEP 8 — `snake_case` (fungsi/variabel), `PascalCase` (kelas),
`UPPER_SNAKE_CASE` (konstanta). Lihat **SPESIFIKASI §9**.

---

## 7. Status & Langkah Berikutnya

- [x] Struktur proyek, dependensi, konfigurasi, konstanta
- [x] Kerangka modul KDD (signature) + CLI + tests scaffold
- [x] UI web statis (5 halaman + login) membaca `reports/`
- [x] **Implementasi logika tiap modul KDD (`data_loader` … `pipeline`)** — pipeline latih→evaluasi→prediksi berjalan end-to-end
- [x] **Visualisasi PNG** (pohon, confusion matrix, ROC, feature importance)
- [x] **Generator data sintetis** (`scripts/generate_dummy_data.py`) + 26 unit test hijau
- [ ] Ekspor artefak UI (`web_export`) + JS prediksi di browser — *fase berikutnya*
- [ ] Dataset asli ± 300 responden (ganti `data/raw/kuesioner_santriwati.csv`)

> **Menjalankan sekarang:** `python scripts/generate_dummy_data.py` lalu
> `python scripts/run_training.py` → model + metrik + 4 PNG langsung terbentuk.

---

*Lokasi studi: Pondok Pesantren Annuqayah, Guluk-Guluk, Sumenep. Batasan: hanya faktor
jadwal/aktivitas; tidak mencakup faktor medis/hormonal.*
