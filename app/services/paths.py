# app/services/paths.py
from __future__ import annotations
import os
import sys
from pathlib import Path

_APP_NAME = "TibiaAnalyzer"

# ---------- Recursos (assets) ----------
def _frozen_base() -> Path:
    """
    Base de lectura de recursos:
    - Si está congelado (PyInstaller): sys._MEIPASS
    - Si no, la raíz del repo (dos niveles arriba de este archivo)
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    # este archivo: .../app/services/paths.py  -> subimos dos niveles
    return Path(__file__).resolve().parents[2]

def asset_path(*parts: str) -> Path:
    """
    Devuelve la ruta absoluta a un asset incluido en el bundle.
    Uso: asset_path("assets", "style.qss")
    """
    return _frozen_base().joinpath(*parts)

# ---------- Biblioteca JSON (persistente fuera del .exe) ----------
_LIB_DIR_CACHE: Path | None = None

def _user_data_root() -> Path:
    """
    Carpeta de datos del usuario donde guardar la biblioteca y config.
    - Windows: %LOCALAPPDATA%/_APP_NAME
    - Linux/Mac: ~/.local/share/_APP_NAME
    """
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Local")
        return Path(base) / _APP_NAME
    # POSIX
    return Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local" / "share"))) / _APP_NAME

def library_dir() -> str:
    """
    Directorio donde la app guarda/lee los JSON de biblioteca (siempre externo al .exe).
    """
    global _LIB_DIR_CACHE
    if _LIB_DIR_CACHE is None:
        _LIB_DIR_CACHE = _user_data_root() / "json"
        _LIB_DIR_CACHE.mkdir(parents=True, exist_ok=True)
    return str(_LIB_DIR_CACHE)

def library_manifest_path() -> str:
    """
    Ruta absoluta al MANIFEST.json de la biblioteca (dedupe por hash) en AppData.
    """
    return str(_user_data_root() / "library_manifest.json")
