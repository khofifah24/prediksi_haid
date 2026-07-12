# Rancangan UI Web — Sistem Prediksi Keteraturan Haid Santriwati (Decision Tree)

> Dokumen desain antarmuka (UI/UX) untuk sistem prediksi keteraturan haid santriwati berbasis Decision Tree.
> **Pola acuan:** aplikasi data-mining sederhana bergaya *admin dashboard* (referensi "C45 App").
> **Prinsip:** satu dashboard, **tanpa peran (role)**, **login/register opsional** — fokus pada alur data mining (KDD), bukan manajemen pengguna.
> **Teknologi UI:** cukup **HTML + CSS + JavaScript** (boleh **Tailwind CSS** via CDN) — **tanpa framework backend**. Frontend statis yang membaca hasil olahan Python (JSON/PNG) dari folder `reports/`.

---

## 1. Prinsip Desain

| Prinsip | Penerapan |
|---|---|
| **Sederhana & fokus** | Satu sidebar, 5 halaman inti. Tidak ada role, tidak ada hak akses berlapis. |
| **Login opsional** | Sistem berjalan penuh tanpa login. Login/Logout hanya pelengkap bila ingin membatasi akses. |
| **Alur mengikuti KDD** | Urutan menu = urutan proses: kelola data → proses → uji → evaluasi. |
| **Data sensitif** | Nama disamarkan (inisial/ID). Warna status kalem, bukan merah "alarm". Ada disclaimer non-medis. |
| **Bersih & mobile-friendly** | Kartu rounded, spasi lega, tabel responsif, Bahasa Indonesia sederhana. |
| **UI statis** | Cukup HTML/CSS/JS (atau Tailwind via CDN). Tanpa server/framework; data dibaca dari file JSON/PNG hasil skrip Python. |

**Nama aplikasi (placeholder):** `Prediksi Haid` — bisa diganti nama yang lebih diskret bila diinginkan (mis. `SIPRESA` — Sistem Prediksi Kesehatan Santri).

---

## 2. Struktur Navigasi

Sidebar kiri, mengikuti tata letak referensi (logo → grup MENU → grup GENERAL).

```
┌────────────────────┐
│  ⬢  Prediksi Haid  │   ← logo + nama app
├────────────────────┤
│  MENU              │
│  ▣  Dashboard      │   index.html       → Ringkasan
│  ▤  Data Santriwati│   santriwati.html  → Kelola dataset
│  ⚙  Proses D-Tree  │   proses.html      → Bangun model
│  🧪 Pengujian      │   pengujian.html   → Prediksi & uji
│  📊 Evaluasi Model │   evaluasi.html    → Metrik & pohon
├────────────────────┤
│  GENERAL           │
│  ↪  Logout         │   (opsional)
└────────────────────┘
```

**Peta halaman → file → sumber data** (semua diproses lebih dulu oleh skrip Python di `SPESIFIKASI-SISTEM-PREDIKSI-HAID.md`, lalu ditulis ke folder `reports/` sebagai JSON/PNG yang dibaca UI):

| Halaman | File HTML | Sumber data untuk UI |
|---|---|---|
| Dashboard | `index.html` | `reports/ringkasan.json`, `reports/feature_importance.json` |
| Data Santriwati | `santriwati.html` | `reports/data_santriwati.json` (atau CSV) |
| Proses Decision Tree | `proses.html` | `reports/status_model.json` (form parameter → disimpan lokal) |
| Pengujian | `pengujian.html` | `reports/aturan_pohon.json`, `reports/data_uji.json` |
| Evaluasi Model | `evaluasi.html` | `reports/metrik_evaluasi.json`, `reports/figures/pohon_keputusan.png`, `reports/figures/confusion_matrix.png`, `reports/figures/feature_importance.png` |
| Login/Register (opsional) | `login.html`, `register.html` | — |

> **Catatan alur:** perhitungan Decision Tree (latih model, metrik, gambar pohon) dilakukan **sekali** oleh skrip Python, hasilnya diekspor ke `reports/`. UI hanya **menampilkan** hasil tersebut — jadi cukup HTML/CSS/JS statis tanpa backend berjalan.

---

## 3. Kerangka Layout Global

Semua halaman memakai kerangka yang sama: **sidebar tetap (kiri) + topbar + area konten**.

```
┌──────────┬──────────────────────────────────────────────────────┐
│          │  [Judul Halaman]                      🔔   AC Admin ▾  │  ← topbar
│ SIDEBAR  ├──────────────────────────────────────────────────────┤
│  (menu)  │                                                        │
│          │                 AREA KONTEN                            │
│          │        (kartu, tabel, form, grafik)                    │
│          │                                                        │
└──────────┴──────────────────────────────────────────────────────┘
```

- **Topbar:** judul halaman (kiri) + notifikasi/aksi cepat + identitas (kanan; hanya tampil bila login aktif, jika tidak → disembunyikan).
- **Sidebar:** menu aktif ditandai highlight (seperti "Data Mahasiswa" pada referensi).

---

## 4. Halaman 1 — Dashboard (`/`)

Ringkasan cepat kondisi data & model. Isinya kartu statistik + grafik ringkas.

```
┌──────────────────────────────────────────────────────────────────┐
│  Dashboard                                                         │
│  Ringkasan data & performa model prediksi keteraturan haid.        │
│                                                                    │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐       │
│  │ Total Data │ │  Teratur   │ │Tdk Teratur │ │  Akurasi   │       │
│  │    300     │ │  190 (63%) │ │  110 (37%) │ │   87.5 %   │       │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘       │
│                                                                    │
│  ┌───────────────────────────┐  ┌──────────────────────────────┐  │
│  │ Distribusi Kelas (donat)  │  │ Faktor Paling Berpengaruh    │  │
│  │        ◑ 63% / 37%        │  │ (feature importance, bar)    │  │
│  │                           │  │ Tingkat Stres    ▇▇▇▇▇▇ 0.31  │  │
│  │                           │  │ Pola Tidur       ▇▇▇▇▇  0.24  │  │
│  │                           │  │ Kelelahan        ▇▇▇▇   0.18  │  │
│  └───────────────────────────┘  └──────────────────────────────┘  │
│                                                                    │
│  ⓘ Model terakhir dilatih: 12 Jul 2026 · 300 data · rasio 80:20    │
└──────────────────────────────────────────────────────────────────┘
```

**Komponen & fitur**
- **4 kartu statistik**: Total Data, jumlah Teratur, jumlah Tidak Teratur, Akurasi model terakhir.
- **Grafik donat** distribusi kelas target.
- **Bar chart** *feature importance* — variabel apa yang paling menentukan (nilai jual edukatif).
- **Info strip**: kapan model terakhir dilatih, jumlah data, rasio split.
- Bila belum ada model terlatih → tampilkan *empty state*: "Belum ada model. Jalankan Proses Decision Tree dulu."

---

## 5. Halaman 2 — Data Santriwati (`/santriwati`) — layar utama

Padanan langsung "Data Mahasiswa" pada referensi. Kelola dataset kuesioner.

```
┌──────────────────────────────────────────────────────────────────┐
│  Data Santriwati                  [⬇ Template CSV] [⚗ Lihat        │
│  Kelola dataset untuk proses       Preprocessing] [⬆ Import Data]  │
│  Decision Tree.                                   [＋ Tambah Data] │
│                                                                    │
│ ┌────────────────────────────────────────────────────────────────┐│
│ │ ID   Nama    Jdwl Tidur Lelah Stres Makan Aktv Istrht  Status  ⋮ ││
│ ├────────────────────────────────────────────────────────────────┤│
│ │ S001 Santri A 4.5  2.0   4.0   4.5   2.5   5.0   2.0  🟡 Tdk Ttr ││
│ │ S002 Santri B 3.0  4.5   2.0   2.0   4.0   3.0   4.5  🟢 Teratur ││
│ │ S003 Santri C 5.0  1.5   4.5   5.0   2.0   4.5   1.5  🟡 Tdk Ttr ││
│ │ …                                                               ││
│ └────────────────────────────────────────────────────────────────┘│
│  Showing 1 to 10 of 300 results          ‹ 1 2 3 4 5 … 30 ›        │
└──────────────────────────────────────────────────────────────────┘
```

**Kolom tabel** (7 variabel penelitian + status): `ID · Nama(anonim) · Jadwal · Tidur · Kelelahan · Stres · Pola Makan · Aktivitas · Istirahat · Status`.
Nilai kolom = skor agregat 1–5 tiap variabel. Kolom **⋮** = aksi baris (Lihat detail / Edit / Hapus).

**Tombol aksi (atas kanan)** — sama seperti referensi:
| Tombol | Fungsi |
|---|---|
| **Template CSV** | Unduh berkas CSV kosong berisi header kolom yang benar |
| **Lihat Preprocessing** | Buka panel/halaman perbandingan data mentah → data bersih → data ter-encode |
| **Import Data** | Unggah CSV kuesioner (validasi skema; tampilkan ringkasan baris valid/gagal) |
| **Tambah Data** | Modal berisi form kuesioner 15 pertanyaan (lihat §4.1) |

### 5.1 Modal "Tambah Data" — Form Kuesioner

Form 15 pertanyaan Likert, dikelompokkan per variabel; skala **SS–S–N–TS–STS**.

```
┌──────────── Tambah Data Santriwati ─────────────┐
│  Nama (inisial/anonim): [____________]           │
│  Usia: [__]   Lama mondok (th): [__]             │
│  ────────────────────────────────────────────   │
│  1. Jadwal Kegiatan Harian                        │
│     Q1  ○SS ○S ○N ○TS ○STS                        │
│     Q2  ○SS ○S ○N ○TS ○STS                        │
│  2. Pola Tidur                                    │
│     Q3 …  Q4 …                                    │
│  … (sampai Q15) …                                 │
│  ────────────────────────────────────────────   │
│  Status haid (label): ( ) Teratur ( ) Tidak      │
│                      [Batal]        [Simpan]      │
└──────────────────────────────────────────────────┘
```
- Field label "Status haid" hanya untuk **data latih** (data yang sudah diketahui hasilnya). Untuk prediksi kasus baru gunakan halaman **Pengujian**.

### 5.2 Panel "Lihat Preprocessing"

Tampilkan 3 tab langkah KDD agar proses transparan (bagus untuk dokumentasi skripsi):
- **Tab 1 – Data Cleaning:** baris dengan *missing value*/duplikat yang dibuang.
- **Tab 2 – Transformation:** contoh konversi Likert (SS→5 … STS→1) & target (Teratur→1, Tidak→0).
- **Tab 3 – Balancing (opsional):** distribusi sebelum vs sesudah *balancing*.

---

## 6. Halaman 3 — Proses Decision Tree (`/proses`)

Padanan "Proses C4.5". Menjalankan pelatihan model dari data yang ada.

```
┌──────────────────────────────────────────────────────────────────┐
│  Proses Decision Tree                                              │
│  Bangun model dari 300 data santriwati.                           │
│                                                                    │
│  Parameter:                                                        │
│   Kriteria split : (•) Gini   ( ) Entropy (Information Gain)       │
│   Kedalaman maks : [  auto ▾ ]     Rasio latih:uji : [ 80:20 ▾ ]   │
│   Pruning (ccp)  : [ 0.0 ]         Random state    : [ 42 ]        │
│                                                                    │
│                         [ ▶ Jalankan Proses ]                      │
│                                                                    │
│  ── Progres ─────────────────────────────────────────────────     │
│  ✔ Data Selection      ✔ Preprocessing     ✔ Transformation       │
│  ✔ Split 80:20         ✔ Build Tree        ✔ Model tersimpan       │
│                                                                    │
│  ✅ Model berhasil dibuat. Lihat hasilnya di Evaluasi Model.       │
└──────────────────────────────────────────────────────────────────┘
```

**Fitur**
- **Form parameter** = hyperparameter dari spesifikasi (`criterion`, `max_depth`, `test_size`, `ccp_alpha`, `random_state`).
- **Tombol "Jalankan Proses"**: karena UI bersifat statis, tombol ini **menampilkan panduan/perintah** untuk menjalankan skrip Python (`python pipeline.py`) dengan parameter terpilih, lalu memantau `reports/status_model.json`. (Bila kelak ingin otomatis, cukup ganti dengan satu endpoint kecil — struktur UI tidak berubah.)
- **Stepper progres** menampilkan tahap KDD satu per satu berdasarkan status di `reports/status_model.json` (edukatif & meyakinkan saat demo sidang).
- **Notifikasi hasil** + tautan ke Evaluasi Model.

> Alternatif paling sederhana: halaman ini murni **informasi/dokumentasi** parameter, sedangkan pelatihan model dijalankan manual via terminal. Ini menjaga UI tetap 100% statis (HTML/CSS/JS).

---

## 7. Halaman 4 — Pengujian (`/pengujian`)

Padanan "Pengujian C4.5". Dua mode dalam satu halaman (tab).

**Tab A — Prediksi Kasus Baru**
```
┌──────────────── Prediksi Kasus Baru ─────────────────┐
│  Isi 15 pertanyaan / 7 skor variabel:                 │
│   Jadwal [4] Tidur [2] Kelelahan [4] Stres [5]        │
│   Pola Makan [2] Aktivitas [5] Istirahat [2]          │
│                    [ 🔍 Prediksi ]                    │
│  ─────────────────────────────────────────────────   │
│  Hasil:  🟡  CENDERUNG TIDAK TERATUR   (keyakinan 82%)│
│  Faktor dominan: Tingkat Stres, Pola Tidur            │
│  ⓘ Ini prediksi berbasis data, BUKAN diagnosis medis. │
└───────────────────────────────────────────────────────┘
```

**Tab B — Uji Data Testing**
- Jalankan model pada 20% data uji → tampilkan tabel: data uji, label aktual, label prediksi, benar/salah.
- Ringkasan jumlah benar/salah di atas tabel.

**Fitur**
- Input manual 7 skor **atau** isi ulang 15 Likert.
- Output: **label + tingkat keyakinan** + **faktor dominan** (jalur keputusan / feature importance).
- **Prediksi di sisi browser:** aturan pohon diekspor Python ke `reports/aturan_pohon.json` (daftar if-else sederhana). JavaScript cukup menelusuri aturan itu untuk memberi hasil — tanpa perlu server.
- **Disclaimer non-medis** wajib tampil di area hasil.

---

## 8. Halaman 5 — Evaluasi Model (`/evaluasi`)

Metrik performa + visualisasi pohon. Sumber lampiran bab hasil skripsi.

```
┌──────────────────────────────────────────────────────────────────┐
│  Evaluasi Model                                                    │
│                                                                    │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐                   │
│  │Accuracy │ │Precision│ │ Recall  │ │   F1    │                   │
│  │ 87.5 %  │ │ 0.86    │ │ 0.84    │ │ 0.85    │                   │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘                   │
│                                                                    │
│  ┌──────────────────────────┐   ┌────────────────────────────┐    │
│  │ Confusion Matrix          │   │ Feature Importance (bar)   │    │
│  │        Pred:0  Pred:1     │   │ Stres    ▇▇▇▇▇▇ 0.31        │    │
│  │  Act0 [ TN ][ FP ]        │   │ Tidur    ▇▇▇▇▇  0.24        │    │
│  │  Act1 [ FN ][ TP ]        │   │ Lelah    ▇▇▇▇   0.18        │    │
│  └──────────────────────────┘   └────────────────────────────┘    │
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │ Visualisasi Pohon Keputusan            [⬇ Unduh PNG]        │   │
│  │   Stres ≤ 3.5 ─┬─ ya → Tidur ≤ 2.5 → …                      │   │
│  │                └─ tidak → Teratur                           │   │
│  └────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

**Komponen & fitur**
- **4 kartu metrik**: Accuracy, Precision, Recall, F1 (dari `reports/metrik_evaluasi.json`).
- **Confusion matrix** (heatmap 2×2) + **feature importance** (bar).
- **Visualisasi pohon keputusan** + tombol **Unduh PNG** (dari `visualization.plot_decision_tree`).
- Semua gambar dapat diunduh untuk dilampirkan ke laporan.

---

## 9. Komponen UI yang Dipakai Ulang

| Komponen | Kegunaan | Catatan |
|---|---|---|
| **Badge status** | Label Teratur/Tidak Teratur | 🟢 hijau kalem / 🟡 amber (bukan merah alarm) |
| **Kartu statistik** | Angka ringkas di Dashboard & Evaluasi | Judul + angka besar + ikon |
| **Tabel data** | Data Santriwati, Uji Data | Sortir kolom, pagination, aksi baris |
| **Modal form** | Tambah/Edit data, kuesioner | Validasi field wajib |
| **Stepper progres** | Proses Decision Tree | Menandai tahap KDD selesai |
| **Toast/alert** | Notifikasi sukses/gagal | Import, latih model, simpan |
| **Empty state** | Saat data/model kosong | Ajakan aksi ("Import Data", "Jalankan Proses") |
| **Disclaimer banner** | Halaman hasil prediksi | "Bukan diagnosis medis" |

---

## 10. Palet Warna & Tipografi

**Warna** (nuansa tenang, sesuai konteks pesantren & data sensitif)

| Peran warna | Saran hex | Pemakaian |
|---|---|---|
| Primary | `#0D9488` (teal kalem) | Tombol utama, menu aktif, aksen |
| Teratur | `#10B981` (hijau lembut) | Badge & grafik kelas "Teratur" |
| Tidak Teratur | `#F59E0B` (amber) | Badge & grafik "Tidak Teratur" (hindari merah) |
| Netral teks | `#1F2937` / `#6B7280` | Judul / teks sekunder |
| Latar | `#F9FAFB` + kartu `#FFFFFF` | Background bersih |

**Tipografi:** sans-serif modern (Inter / Plus Jakarta Sans). Judul halaman `~24px` bold, teks tabel `~14px`, angka kartu statistik `~28px` bold.

---

## 11. Alur Navigasi Pengguna (User Flow)

```
        (opsional) Login ──► 
                              ▼
   ┌─────────► Dashboard ◄───────────┐
   │              │                   │
   │              ▼                   │
   │        Data Santriwati           │  (kelola dataset:
   │         │   import / tambah      │   isi hingga cukup)
   │         ▼                        │
   │     Proses Decision Tree ────────┘  (latih model)
   │         │
   │         ▼
   │      Pengujian  ──► prediksi kasus baru / uji data testing
   │         │
   │         ▼
   └────  Evaluasi Model  ──► metrik, confusion matrix, pohon
```

Urutan ideal saat demo sidang: **Data → Proses → Pengujian → Evaluasi**.

---

## 12. Opsi Login (Opsional)

Bila ingin membatasi akses (mis. hanya operator pesantren):
- Halaman **Login** sederhana (`login.html`) dan **Register** satu tingkat (`register.html`), tanpa peran.
- Tanpa login, seluruh halaman tetap dapat diakses (mode terbuka).
- Karena UI statis, ini hanya **gerbang tampilan** (mis. cek kata sandi sederhana via JavaScript + `localStorage`), **bukan** keamanan sungguhan. Untuk pembatasan akses nyata, sajikan folder di balik autentikasi server (mis. Basic Auth pada web server) — di luar cakupan UI.

---

## 13. Catatan Privasi (Ringkas)

- Simpan **inisial/ID**, bukan nama lengkap, pada tampilan tabel.
- Sediakan kalimat persetujuan singkat saat pengisian kuesioner.
- Tegakkan disclaimer **"prediksi, bukan diagnosis medis"** di setiap keluaran.
- Data hasil ekspor (CSV/PDF) sebaiknya tidak memuat identitas yang bisa menelusuri individu.

---

## 14. Rekomendasi Teknis (selaras spesifikasi)

- **Frontend (UI):** cukup **HTML + CSS + JavaScript**. Untuk tampilan bersih seperti referensi, pakai **Tailwind CSS via CDN** (`<script src="https://cdn.tailwindcss.com"></script>`) — tanpa build step. Alternatif: satu berkas `style.css` biasa.
- **Struktur berkas UI:** kumpulan halaman statis + aset ringan.

```text
ui/
├── index.html          # Dashboard
├── santriwati.html     # Data Santriwati
├── proses.html         # Proses Decision Tree
├── pengujian.html      # Pengujian
├── evaluasi.html       # Evaluasi Model
├── login.html          # (opsional)
└── assets/
    ├── theme.js        # konfigurasi tema Tailwind (palet & token warna)
    ├── style.css       # token CSS + komponen (kartu, badge, tabel, dark mode)
    └── app.js          # layout bersama (sidebar/topbar), helper JSON, chart, dark-mode toggle
# reports/ (di akar proyek, bukan di ui/) — JSON & PNG hasil skrip Python, dibaca UI via ../reports/
```

- **Grafik:** **Chart.js via CDN** untuk donat (distribusi kelas) & bar (feature importance) yang interaktif + adaptif dark mode; visualisasi pohon dan heatmap confusion matrix ditampilkan sebagai **PNG** hasil Matplotlib/Seaborn dari `reports/figures/`.
- **Tema:** Tailwind CSS via CDN + `assets/theme.js` (palet **teal** primary, semantik **hijau/amber** untuk kelas — divalidasi CVD-safe). Mendukung **mode gelap** (toggle di topbar, tersimpan di `localStorage`). Font **Inter** via Google Fonts.
- **Data:** UI membaca berkas **JSON/CSV/PNG** di `reports/` menggunakan `fetch()`. Jalankan lewat server statis lokal agar `fetch` bekerja (mis. `python -m http.server` lalu buka `http://localhost:8000/ui/index.html`).
- **Pemisahan tanggung jawab:** semua komputasi Decision Tree tetap di Python (spesifikasi terpisah); UI hanya lapisan presentasi. Ini menjaga UI ringan dan mudah dipresentasikan saat sidang.

---

*Rancangan ini melengkapi `SPESIFIKASI-SISTEM-PREDIKSI-HAID.md`. Wireframe berupa sketsa ASCII sebagai acuan tata letak; implementasi visual final memakai HTML/CSS/JS (atau Tailwind) statis.*
