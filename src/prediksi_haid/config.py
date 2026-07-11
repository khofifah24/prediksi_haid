"""Loader konfigurasi (config.py) — membaca ``config/config.yaml``.

Satu-satunya modul yang tahu cara membaca berkas konfigurasi; modul lain
menerima ``dict`` config sebagai argumen agar mudah diuji.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG_PATH = "config/config.yaml"


def load_config(config_path: str = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    """Muat konfigurasi YAML menjadi ``dict``.

    Urutan pencarian path: argumen ``config_path`` -> variabel lingkungan
    ``PREDIKSI_HAID_CONFIG`` -> default ``config/config.yaml``.

    Raises:
        FileNotFoundError: bila berkas konfigurasi tidak ditemukan.
    """
    path = Path(os.getenv("PREDIKSI_HAID_CONFIG", config_path))
    if not path.exists():
        raise FileNotFoundError(f"Berkas konfigurasi tidak ditemukan: {path}")
    with path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}
    return config


# NOTE: kelas AppConfig (validasi via pydantic) bersifat OPSIONAL — lihat §8.1.
# Aktifkan bila ingin validasi skema konfigurasi yang ketat.
# class AppConfig(BaseModel): ...
