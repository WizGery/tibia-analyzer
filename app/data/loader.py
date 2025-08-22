# app/data/loader.py
import os
import json
from typing import List
from app.data.normalizer import normalize_json
from app.services.paths import library_dir

# nombre del fichero auxiliar que NO es un hunt válido
_IGNORE_FILENAME = "_dataset_seen_hashes.json"

def load_hunts_from_library() -> List:
    hunts = []
    lib = library_dir()
    if not os.path.isdir(lib):
        return hunts

    for entry in os.scandir(lib):
        if not entry.is_file() or not entry.name.lower().endswith(".json"):
            continue
        # ignorar el registro local de hashes del dataset
        if entry.name == _IGNORE_FILENAME:
            continue

        path = entry.path
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            hunts.append(normalize_json(path, data))
        except Exception as e:
            print(f"Error leyendo {path}: {e}")
    return hunts
