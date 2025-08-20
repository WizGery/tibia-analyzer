import json
import os
from typing import List, Dict, Optional

APP_DIR_NAME = "Tibia Analyzer"  # carpeta de datos de la app (persistencia)
PROFILES_FILE = "profiles.json"

def _appdata_dir() -> str:
    # %APPDATA%\Tibia Analyzer en Windows; fallback a home en otros SO
    base = os.getenv("APPDATA") or os.path.expanduser("~")
    path = os.path.join(base, APP_DIR_NAME)
    os.makedirs(path, exist_ok=True)
    return path

def _profiles_path() -> str:
    return os.path.join(_appdata_dir(), PROFILES_FILE)

def _load_raw() -> Dict:
    path = _profiles_path()
    if not os.path.exists(path):
        return {"profiles": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict) or "profiles" not in data:
            return {"profiles": []}
        return data
    except Exception:
        return {"profiles": []}

def _save_raw(data: Dict) -> None:
    path = _profiles_path()
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)

def list_profiles() -> List[Dict[str, str]]:
    return list(_load_raw().get("profiles", []))

def get_profile(name: str) -> Optional[Dict[str, str]]:
    for p in list_profiles():
        if p.get("name") == name:
            return p
    return None

def upsert_profile(name: str, vocation: str, level: str) -> None:
    data = _load_raw()
    profiles = data.get("profiles", [])
    # si existe, actualiza; si no, añade
    for p in profiles:
        if p.get("name") == name:
            p["vocation"] = vocation
            p["level"] = level
            _save_raw(data)
            return
    profiles.append({"name": name, "vocation": vocation, "level": level})
    data["profiles"] = profiles
    _save_raw(data)

def delete_profile(name: str) -> None:
    data = _load_raw()
    profiles = [p for p in data.get("profiles", []) if p.get("name") != name]
    data["profiles"] = profiles
    _save_raw(data)
