from __future__ import annotations

import json
import os
import shutil
from typing import Dict, Any

def _load_json(path: str) -> Dict[str, Any] | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def _atomic_write_json(path: str, data: Dict[str, Any]) -> bool:
    tmp = f"{path}.tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
        return True
    except Exception:
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except Exception:
            pass
        return False

def write_meta_to_json(path: str, updates: Dict[str, Any]) -> bool:
    """
    Actualiza metadatos en un JSON existente y crea .bak si no existe.
    Espera claves con los nombres que usas en PendingDialog:
      - "Vocation", "Mode", "Vocation duo", "Zona", "Level",
        "Balance Real", "Ignore Duo Balance"
    """
    if not path or not os.path.isfile(path):
        return False

    data = _load_json(path)
    if data is None or not isinstance(data, dict):
        return False

    # Backup .bak (si no existe)
    try:
        bak = f"{path}.bak"
        if not os.path.exists(bak):
            shutil.copy2(path, bak)
    except Exception:
        pass  # si falla el backup, seguimos

    # Aplicar cambios si están en updates
    def set_if_present(json_key: str):
        if json_key in updates:
            data[json_key] = updates[json_key]

    for key in ["Vocation", "Mode", "Vocation duo", "Zona", "Level", "Balance Real", "Ignore Duo Balance"]:
        set_if_present(key)

    return _atomic_write_json(path, data)
