#!/usr/bin/env bash
# ============================================================
#  Setup lingkungan pengembangan (Linux/macOS) — Prediksi Haid
#  Jalankan dari akar proyek:  bash scripts/setup.sh
# ============================================================
set -e

echo "[1/4] Membuat virtual environment (.venv)..."
python3 -m venv .venv

echo "[2/4] Mengaktifkan venv..."
# shellcheck disable=SC1091
source .venv/bin/activate

echo "[3/4] Memperbarui pip..."
python -m pip install --upgrade pip

echo "[4/4] Memasang dependensi (dev)..."
pip install -r requirements-dev.txt
pip install -e .

echo
echo "Selesai. Aktifkan venv dengan:  source .venv/bin/activate"
echo "Uji cepat:  pytest -q"
