@echo off
REM ============================================================
REM  Setup lingkungan pengembangan (Windows) — Prediksi Haid
REM  Jalankan dari akar proyek:  scripts\setup.bat
REM ============================================================
setlocal

echo [1/4] Membuat virtual environment (.venv)...
py -m venv .venv || python -m venv .venv

echo [2/4] Mengaktifkan venv...
call .venv\Scripts\activate.bat

echo [3/4] Memperbarui pip...
python -m pip install --upgrade pip

echo [4/4] Memasang dependensi (dev)...
pip install -r requirements-dev.txt
pip install -e .

echo.
echo Selesai. Aktifkan venv dengan:  .venv\Scripts\activate
echo Uji cepat:  pytest -q
endlocal
