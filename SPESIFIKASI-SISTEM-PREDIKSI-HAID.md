# Spesifikasi Sistem — Prediksi Keteraturan Haid Santriwati Berdasarkan Jadwal Kegiatan (Metode *Decision Tree*)

> Dokumen ini mengekstrak kebutuhan sistem dari proposal skripsi (sempro) dan menerjemahkannya menjadi **spesifikasi teknis** siap-bangun: pustaka, arsitektur, struktur proyek, skema data, variabel/parameter, dan konvensi penamaan (file, modul, fungsi, kelas, variabel, konfigurasi).
> **Catatan:** dokumen ini berisi *penamaan* dan *tanda tangan (signature)* — **bukan** contoh implementasi kode.

---

## 1. Ringkasan Sistem

| Aspek | Nilai |
|---|---|
| **Judul** | Prediksi Keteraturan Haid Santriwati Berdasarkan Jadwal Kegiatan Menggunakan Metode *Decision Tree* |
| **Jenis sistem** | Pipeline *machine learning* klasifikasi biner (batch, offline) |
| **Bahasa** | Python |
| **Metodologi olah data** | KDD — *Knowledge Discovery in Database* |
| **Algoritma** | *Decision Tree* (CART, kriteria *Gini*/*entropy–information gain*) |
| **Tugas** | Klasifikasi biner: **teratur (1)** vs **tidak teratur (0)** |
| **Sumber data** | Kuesioner (skala Likert 1–5) + observasi; ± 300 responden santriwati |
| **Rasio split** | 80% *training* : 20% *testing* |
| **Metrik evaluasi** | *Accuracy*, *Precision*, *Recall*, *ROC/AUC*, *Confusion Matrix* |
| **Lokasi studi** | Pondok Pesantren Annuqayah, Guluk-Guluk, Sumenep |
| **Batasan** | Hanya faktor jadwal/aktivitas; tidak mencakup faktor medis/hormonal; bukan alat diagnosis medis |

**Alur inti (KDD):** `Data Selection → Data Preprocessing → Data Transformation → Data Mining (Decision Tree) → Evaluation → Hasil Prediksi`

---

## 2. Tech Stack & Pustaka (Library)

### 2.1 Pustaka inti (wajib)

| Pustaka | Versi minimum | Peran dalam sistem |
|---|---|---|
| `python` | `>=3.11` | Runtime |
| `pandas` | `>=2.2` | Muat & manipulasi dataset kuesioner (DataFrame) |
| `numpy` | `>=1.26` | Operasi numerik, array fitur |
| `scikit-learn` | `>=1.5` | `DecisionTreeClassifier`, split, metrik, `LabelEncoder` |
| `matplotlib` | `>=3.8` | Visualisasi pohon, kurva ROC, grafik |
| `seaborn` | `>=0.13` | Heatmap *confusion matrix*, distribusi fitur |
| `joblib` | `>=1.4` | Serialisasi model (`.joblib`) |
| `pyyaml` | `>=6.0` | Baca berkas konfigurasi `config.yaml` |

### 2.2 Pustaka pendukung (opsional / disarankan)

| Pustaka | Peran |
|---|---|
| `imbalanced-learn` | *Balancing* data tidak seimbang (SMOTE) — disebut di proposal ("balance pada data yang unbalance") |
| `openpyxl` | Baca kuesioner format `.xlsx` |
| `pydantic` | Validasi skema baris data & konfigurasi |
| `python-dotenv` | Muat variabel lingkungan dari `.env` |

### 2.3 Pustaka pengembangan (dev)

| Pustaka | Peran |
|---|---|
| `pytest` | Pengujian unit |
| `ruff` | *Linter* + *formatter* |
| `black` | Format kode (opsional bila tak pakai ruff-format) |
| `mypy` | Pemeriksaan tipe statis |
| `jupyter` | Eksplorasi *notebook* (EDA) |

> Pustaka seperti `TensorFlow`, `Keras`, `PyTorch`, `SciPy`, `Dask` disebut di landasan teori proposal, **tetapi tidak diperlukan** untuk *Decision Tree*. Jangan dimasukkan ke `requirements.txt` agar dependensi tetap ramping.

---

## 3. Struktur Proyek (Penamaan File & Folder)

Mengikuti tata letak standar proyek *data science* Python (mirip *cookiecutter-data-science*, `src/`-layout).

```
prediksi-keteraturan-haid/
├── README.md
├── pyproject.toml               # metadata proyek + dependensi (PEP 621)
├── requirements.txt             # dependensi terkunci (alternatif/ekspor)
├── .gitignore
├── .env.example                 # contoh variabel lingkungan
├── config/
│   └── config.yaml              # semua parameter & path (lihat §6)
│
├── data/
│   ├── raw/                     # data mentah kuesioner (JANGAN diedit manual)
│   │   └── kuesioner_santriwati.csv
│   ├── interim/                 # hasil antara (setelah cleaning)
│   │   └── data_bersih.csv
│   └── processed/               # dataset final siap latih
│       ├── dataset_encoded.csv
│       ├── X_train.csv
│       ├── X_test.csv
│       ├── y_train.csv
│       └── y_test.csv
│
├── models/
│   ├── decision_tree_model.joblib   # model terlatih
│   └── label_encoders.joblib        # encoder kategori tersimpan
│
├── reports/
│   ├── figures/
│   │   ├── pohon_keputusan.png
│   │   ├── confusion_matrix.png
│   │   ├── kurva_roc.png
│   │   └── feature_importance.png
│   └── metrik_evaluasi.json         # accuracy/precision/recall/AUC
│
├── notebooks/
│   └── 01_eksplorasi_data.ipynb     # EDA (penamaan: NN_deskripsi)
│
├── src/
│   └── prediksi_haid/               # package utama (importable)
│       ├── __init__.py
│       ├── config.py                # loader konfigurasi
│       ├── constants.py             # konstanta & nama kolom (lihat §5)
│       ├── data_loader.py           # KDD-1: Data Selection
│       ├── preprocessing.py         # KDD-2: Data Preprocessing
│       ├── transformation.py        # KDD-3: Data Transformation (encoding)
│       ├── dataset_splitter.py      # pembagian train/test 80:20
│       ├── model.py                 # KDD-4: Data Mining (Decision Tree)
│       ├── evaluation.py            # KDD-5: Evaluation (metrik + confmat)
│       ├── visualization.py         # plot pohon, ROC, importance
│       ├── predictor.py             # inferensi data baru
│       └── pipeline.py              # orkestrasi end-to-end KDD
│
├── scripts/                         # entry-point CLI (dijalankan langsung)
│   ├── run_training.py
│   ├── run_evaluation.py
│   └── run_prediction.py
│
└── tests/
    ├── test_preprocessing.py
    ├── test_transformation.py
    ├── test_model.py
    └── test_evaluation.py
```

**Konvensi penamaan berkas**
- Modul Python: `snake_case.py`, satu tanggung jawab per modul (sesuai satu tahap KDD).
- *Notebook*: prefiks nomor urut `NN_deskripsi.ipynb` (mis. `01_eksplorasi_data.ipynb`).
- Berkas data: `snake_case.csv`; jangan pakai spasi/huruf kapital.
- Model & encoder: `snake_case.joblib`.
- Gambar laporan: `snake_case.png`.

---

## 4. Skema Data (Dataset Kuesioner)

### 4.1 Kolom identitas responden

| Nama kolom (DataFrame) | Tipe | Keterangan | Dipakai untuk latih? |
|---|---|---|---|
| `responden_id` | `int` / `str` | ID anonim (pengganti Nama) | ❌ (identitas) |
| `nama` | `str` | Nama responden — **di-drop** sebelum latih (privasi) | ❌ |
| `usia` | `int` | Usia santriwati (tahun) | opsional |
| `lama_mondok` | `int` | Lama menetap di pesantren (tahun) | opsional |
| `tingkat_pendidikan` | `category` | Jenjang pendidikan | opsional |

### 4.2 Variabel penelitian (fitur / *features*)

Delapan variabel dari kuesioner. Kolom `q1`–`q15` = jawaban Likert mentah (1–5); kolom agregat = rata-rata/penjumlahan indikator per variabel.

| # | Variabel | Nama kolom fitur | Item kuesioner | Jumlah item | Rentang |
|---|---|---|---|---|---|
| 1 | Jadwal Kegiatan Harian | `jadwal_kegiatan_harian` | `q1`, `q2` | 2 | 1–5 |
| 2 | Pola Tidur | `pola_tidur` | `q3`, `q4` | 2 | 1–5 |
| 3 | Tingkat Kelelahan | `tingkat_kelelahan` | `q5`, `q6` | 2 | 1–5 |
| 4 | Tingkat Stres | `tingkat_stres` | `q7` | 1 | 1–5 |
| 5 | Pola Makan | `pola_makan` | `q8`, `q9` | 2 | 1–5 |
| 6 | Aktivitas Harian | `aktivitas_harian` | `q10` | 1 | 1–5 |
| 7 | Waktu Istirahat | `waktu_istirahat` | `q11` | 1 | 1–5 |

### 4.3 Variabel target (label)

| Nama kolom | Tipe | Nilai | Asal |
|---|---|---|---|
| `keteraturan_haid` | `int` (biner) | `1` = teratur, `0` = tidak teratur | Item `q12`, `q13`, `q14`, `q15` (4 item) |

- Total item kuesioner: **15 butir** (skala Likert lima tingkat).
- Total responden target: **± 300 santriwati**.

### 4.4 Pemetaan encoding

| Skala Likert | Kode numerik |
|---|---|
| Sangat Setuju (SS) | `5` |
| Setuju (S) | `4` |
| Netral (N) | `3` |
| Tidak Setuju (TS) | `2` |
| Sangat Tidak Setuju (STS) | `1` |

| Kelas target | Kode numerik |
|---|---|
| Teratur | `1` |
| Tidak Teratur | `0` |

---

## 5. Konstanta & Penamaan Kolom (`constants.py`)

Kumpulan nama kolom & konstanta dipusatkan agar tidak ada *string* ajaib (*magic string*) tersebar.

**Nama konstanta (identifier) yang disediakan:**

| Konstanta | Isi (tipe) | Kegunaan |
|---|---|---|
| `TARGET_COLUMN` | `str = "keteraturan_haid"` | Nama kolom label |
| `FEATURE_COLUMNS` | `list[str]` | 7 nama kolom fitur (§4.2) |
| `IDENTITY_COLUMNS` | `list[str]` | Kolom identitas yang di-drop saat latih |
| `LIKERT_ITEM_COLUMNS` | `list[str]` | `["q1", … , "q15"]` |
| `LIKERT_MAP` | `dict[str, int]` | Pemetaan `"SS"→5 … "STS"→1` |
| `TARGET_MAP` | `dict[str, int]` | `{"teratur": 1, "tidak teratur": 0}` |
| `TARGET_LABELS` | `list[str]` | `["Tidak Teratur", "Teratur"]` (urut indeks 0,1) |
| `RANDOM_STATE` | `int = 42` | Seed reproduksibilitas |
| `TEST_SIZE` | `float = 0.20` | Proporsi data uji |

---

## 6. Konfigurasi & Parameter (`config/config.yaml`)

Seluruh parameter yang dapat diubah dikumpulkan di satu berkas YAML (bukan *hard-code*).

**Kunci konfigurasi (config keys) yang didefinisikan:**

```
paths:
  raw_data            # path CSV kuesioner mentah
  interim_data        # path data bersih
  processed_dir       # folder dataset final
  model_output        # path decision_tree_model.joblib
  encoder_output      # path label_encoders.joblib
  reports_dir         # folder laporan
  figures_dir         # folder gambar

split:
  test_size           # 0.20
  random_state        # 42
  stratify            # true  (menjaga proporsi kelas)

preprocessing:
  drop_duplicates     # true
  missing_strategy    # "drop" | "median" | "mode"
  balance_method      # "none" | "smote" | "undersample"

decision_tree:        # hyperparameter DecisionTreeClassifier
  criterion           # "gini" | "entropy"
  max_depth           # int | null
  min_samples_split   # int (default 2)
  min_samples_leaf    # int (default 1)
  max_features        # "sqrt" | "log2" | null
  ccp_alpha           # float  (cost-complexity pruning)
  class_weight        # "balanced" | null

evaluation:
  metrics             # ["accuracy","precision","recall","f1","roc_auc"]
  average             # "binary"
  pos_label           # 1
```

### 6.1 Hyperparameter *Decision Tree* (`decision_tree.*`)

| Parameter (arg `DecisionTreeClassifier`) | Nilai awal disarankan | Catatan dari proposal |
|---|---|---|
| `criterion` | `"gini"` | *Gini index* (CART) — juga dukung `"entropy"` (*information gain*) |
| `max_depth` | `None` → tuning | Batasi untuk cegah *overfitting* |
| `min_samples_split` | `2` | Minimum sampel untuk pemisahan simpul |
| `min_samples_leaf` | `1` | Minimum sampel pada daun |
| `ccp_alpha` | `0.0` → tuning | *Pruning* (pemangkasan) yang disebut di teori |
| `class_weight` | `"balanced"` | Antisipasi kelas tidak seimbang |
| `random_state` | `42` | Reproduksibilitas |

---

## 7. Arsitektur & Pipeline (Pemetaan KDD → Modul)

Arsitektur berlapis: setiap tahap KDD = satu modul dengan fungsi berparameter jelas. Orkestrasi terpusat di `pipeline.py`.

```
                       ┌─────────────────────────┐
 data/raw/CSV  ───────►│ data_loader.py          │  KDD-1 Data Selection
                       │  load_dataset()         │
                       │  select_relevant_cols() │
                       └───────────┬─────────────┘
                                   ▼
                       ┌─────────────────────────┐
                       │ preprocessing.py        │  KDD-2 Preprocessing
                       │  clean_missing_values() │  (cleaning, dedup,
                       │  drop_duplicates()      │   feature selection,
                       │  balance_dataset()      │   balancing)
                       └───────────┬─────────────┘
                                   ▼
                       ┌─────────────────────────┐
                       │ transformation.py       │  KDD-3 Transformation
                       │  encode_likert()        │  (Likert→numerik,
                       │  encode_target()        │   target→0/1)
                       │  aggregate_indicators() │
                       └───────────┬─────────────┘
                                   ▼
                       ┌─────────────────────────┐
                       │ dataset_splitter.py     │  Split 80:20
                       │  split_train_test()     │
                       └───────────┬─────────────┘
                                   ▼
                       ┌─────────────────────────┐
                       │ model.py                │  KDD-4 Data Mining
                       │  build_model()          │  (Decision Tree:
                       │  train_model()          │   entropy/gain/gini,
                       │  save_model()           │   root→branch→leaf)
                       └───────────┬─────────────┘
                                   ▼
                       ┌─────────────────────────┐
                       │ evaluation.py           │  KDD-5 Evaluation
                       │  evaluate_model()       │  (confusion matrix,
                       │  build_confusion_matrix │   accuracy/precision/
                       │  compute_roc_auc()      │   recall/ROC)
                       └───────────┬─────────────┘
                                   ▼
                       ┌─────────────────────────┐
                       │ predictor.py            │  Hasil Prediksi
                       │  predict_single()       │  (teratur / tidak)
                       │  predict_batch()        │
                       └─────────────────────────┘
```

---

## 8. Penamaan Fungsi & Kelas (Signature, tanpa isi)

Daftar *identifier* + tanda tangan sebagai acuan penulisan kode (bukan implementasi).

### 8.1 `config.py`
```
def load_config(config_path: str = "config/config.yaml") -> dict
class AppConfig            # (opsional, jika pakai pydantic) merepresentasikan config.yaml
```

### 8.2 `data_loader.py` — *KDD-1 Data Selection*
```
def load_dataset(path: str) -> pandas.DataFrame
def select_relevant_columns(df: pandas.DataFrame, columns: list[str]) -> pandas.DataFrame
def validate_schema(df: pandas.DataFrame) -> bool
```

### 8.3 `preprocessing.py` — *KDD-2 Preprocessing*
```
def clean_missing_values(df: pandas.DataFrame, strategy: str) -> pandas.DataFrame
def drop_duplicate_rows(df: pandas.DataFrame) -> pandas.DataFrame
def select_features(df: pandas.DataFrame, feature_columns: list[str]) -> pandas.DataFrame
def balance_dataset(X: pandas.DataFrame, y: pandas.Series, method: str) -> tuple
```

### 8.4 `transformation.py` — *KDD-3 Transformation*
```
def encode_likert(df: pandas.DataFrame, mapping: dict) -> pandas.DataFrame
def aggregate_indicators(df: pandas.DataFrame) -> pandas.DataFrame
def encode_target(df: pandas.DataFrame, target_map: dict) -> pandas.DataFrame
def split_features_target(df: pandas.DataFrame) -> tuple   # -> (X, y)
```

### 8.5 `dataset_splitter.py`
```
def split_train_test(X, y, test_size: float, random_state: int, stratify) -> tuple
                                                          # -> (X_train, X_test, y_train, y_test)
def save_splits(splits: tuple, output_dir: str) -> None
```

### 8.6 `model.py` — *KDD-4 Data Mining (Decision Tree)*
```
def build_model(params: dict) -> sklearn.tree.DecisionTreeClassifier
def train_model(model, X_train, y_train) -> sklearn.tree.DecisionTreeClassifier
def get_feature_importance(model, feature_names: list[str]) -> pandas.DataFrame
def save_model(model, path: str) -> None
def load_model(path: str) -> sklearn.tree.DecisionTreeClassifier
```

### 8.7 `evaluation.py` — *KDD-5 Evaluation*
```
def evaluate_model(model, X_test, y_test) -> dict            # accuracy/precision/recall/f1/auc
def build_confusion_matrix(y_true, y_pred) -> numpy.ndarray
def compute_roc_auc(model, X_test, y_test) -> float
def export_metrics(metrics: dict, path: str) -> None         # -> reports/metrik_evaluasi.json
```

### 8.8 `visualization.py`
```
def plot_decision_tree(model, feature_names, class_names, output_path: str) -> None
def plot_confusion_matrix(cm, labels, output_path: str) -> None
def plot_roc_curve(model, X_test, y_test, output_path: str) -> None
def plot_feature_importance(importance_df, output_path: str) -> None
```

### 8.9 `predictor.py`
```
def predict_single(model, features: dict) -> int            # -> 0 | 1
def predict_batch(model, df: pandas.DataFrame) -> pandas.Series
def label_prediction(pred: int) -> str                      # -> "Teratur" | "Tidak Teratur"
```

### 8.10 `pipeline.py` — orkestrasi *end-to-end*
```
def run_training_pipeline(config: dict) -> dict             # jalankan KDD-1..5, simpan model+metrik
def run_prediction_pipeline(config: dict, input_data) -> pandas.Series
```

---

## 9. Konvensi Penamaan Variabel (Reference)

Nama variabel standar yang dipakai lintas modul agar konsisten.

| Variabel | Tipe | Makna |
|---|---|---|
| `df` | `pandas.DataFrame` | DataFrame kerja umum |
| `df_raw` | `pandas.DataFrame` | Data mentah hasil muat |
| `df_clean` | `pandas.DataFrame` | Data setelah *preprocessing* |
| `df_encoded` | `pandas.DataFrame` | Data setelah transformasi numerik |
| `X` | `pandas.DataFrame` | Matriks fitur |
| `y` | `pandas.Series` | Vektor target `keteraturan_haid` |
| `X_train`, `X_test` | `pandas.DataFrame` | Fitur latih / uji |
| `y_train`, `y_test` | `pandas.Series` | Target latih / uji |
| `model` | `DecisionTreeClassifier` | Objek model |
| `y_pred` | `numpy.ndarray` | Hasil prediksi kelas |
| `y_proba` | `numpy.ndarray` | Probabilitas kelas positif |
| `cm` | `numpy.ndarray` | *Confusion matrix* |
| `metrics` | `dict` | Kumpulan skor evaluasi |
| `feature_importance` | `pandas.DataFrame` | Skor pentingnya tiap fitur |
| `config` | `dict` | Konfigurasi terbaca |

**Aturan gaya (PEP 8):**
- Fungsi & variabel: `snake_case`.
- Kelas: `PascalCase` (mis. `AppConfig`, `PredictionResult`).
- Konstanta: `UPPER_SNAKE_CASE` (mis. `TARGET_COLUMN`, `RANDOM_STATE`).
- Modul & berkas: `snake_case.py`.
- *Private helper*: prefiks garis bawah (`_hitung_entropy`).

---

## 10. Entry-Point / CLI (`scripts/`)

| Berkas | Perintah | Fungsi dipanggil |
|---|---|---|
| `run_training.py` | `python scripts/run_training.py --config config/config.yaml` | `pipeline.run_training_pipeline()` |
| `run_evaluation.py` | `python scripts/run_evaluation.py` | `evaluation.evaluate_model()` |
| `run_prediction.py` | `python scripts/run_prediction.py --input data/baru.csv` | `pipeline.run_prediction_pipeline()` |

**Argumen CLI standar:** `--config`, `--input`, `--output`, `--model-path`, `--verbose`.

---

## 11. Metrik Evaluasi (Output `reports/metrik_evaluasi.json`)

| Kunci (JSON key) | Tipe | Sumber |
|---|---|---|
| `accuracy` | `float` | `accuracy_score` |
| `precision` | `float` | `precision_score(pos_label=1)` |
| `recall` | `float` | `recall_score(pos_label=1)` |
| `f1_score` | `float` | `f1_score(pos_label=1)` |
| `roc_auc` | `float` | `roc_auc_score` |
| `confusion_matrix` | `list[list[int]]` | `confusion_matrix` (2×2) |
| `support_train` | `int` | Jumlah baris data latih (± 240) |
| `support_test` | `int` | Jumlah baris data uji (± 60) |

Struktur *confusion matrix* (biner):

| | Prediksi: Tidak Teratur (0) | Prediksi: Teratur (1) |
|---|---|---|
| **Aktual: Tidak Teratur (0)** | TN | FP |
| **Aktual: Teratur (1)** | FN | TP |

### 11.1 Ekspor untuk UI Statis (Frontend)

Antarmuka web dibangun **tanpa framework backend** — hanya HTML/CSS/JS (opsional Tailwind), lihat `RANCANGAN-UI-WEB.md`. Karena itu, pipeline Python cukup **mengekspor berkas statis** ke folder `reports/`, lalu UI membacanya via `fetch()`. Tidak ada server aplikasi yang perlu berjalan.

| Berkas ekspor | Tipe | Dibaca halaman UI | Isi ringkas |
|---|---|---|---|
| `reports/metrik_evaluasi.json` | JSON | Dashboard, Evaluasi | metrik + confusion matrix (§11) |
| `reports/ringkasan.json` | JSON | Dashboard | total data, jumlah per kelas, tanggal & rasio latih terakhir |
| `reports/feature_importance.json` | JSON | Dashboard | daftar `{fitur, skor}` terurut |
| `reports/data_santriwati.json` | JSON | Data Santriwati | baris dataset (ID anonim + 7 skor + status) |
| `reports/aturan_pohon.json` | JSON | Pengujian | aturan if-else pohon (agar prediksi kasus baru bisa jalan di browser) |
| `reports/data_uji.json` | JSON | Pengujian | 20% data uji + label aktual & prediksi |
| `reports/figures/pohon_keputusan.png` | PNG | Evaluasi | visualisasi pohon |
| `reports/figures/confusion_matrix.png` | PNG | Evaluasi | heatmap |
| `reports/figures/kurva_roc.png` | PNG | Evaluasi | kurva ROC |
| `reports/figures/feature_importance.png` | PNG | Dashboard/Evaluasi | bar (alternatif dari JSON) |

Ekspor JSON tambahan ditangani fungsi ringan (mis. pada `evaluation.py`/`visualization.py` atau modul `web_export.py` opsional), semuanya sekadar `json.dump()` — **tidak menambah dependensi web** apa pun ke `requirements.txt`.

---

## 12. Ringkasan Alur Kerja (Runtime)

1. **Konfigurasi** — `load_config()` membaca `config/config.yaml`.
2. **Data Selection** — muat `data/raw/kuesioner_santriwati.csv`, ambil kolom relevan.
3. **Preprocessing** — buang *missing/duplicate*, seleksi fitur, *balancing* bila perlu → `data/interim/data_bersih.csv`.
4. **Transformation** — Likert→numerik, agregasi indikator, target→0/1 → `data/processed/dataset_encoded.csv`.
5. **Split** — bagi 80:20 (*stratified*, `random_state=42`) → simpan `X_train/X_test/y_train/y_test`.
6. **Training** — `build_model()` + `train_model()` → simpan `models/decision_tree_model.joblib`.
7. **Evaluation** — hitung metrik + *confusion matrix* → `reports/metrik_evaluasi.json`.
8. **Visualization** — simpan pohon, ROC, *feature importance* ke `reports/figures/`.
9. **Prediction** — `predict_batch()` mengklasifikasi data baru → **Teratur / Tidak Teratur**.

---

*Sumber ekstraksi: proposal skripsi "Prediksi Keteraturan Haid Santriwati Berdasarkan Jadwal Kegiatan Menggunakan Metode Decision Tree" (BAB I–III). Nilai yang tidak eksplisit di proposal (mis. hyperparameter awal, versi pustaka) diberikan sebagai rekomendasi praktik standar dan dapat disesuaikan.*
