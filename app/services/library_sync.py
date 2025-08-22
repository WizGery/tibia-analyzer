# app/services/library_sync.py
import os
import json
import shutil
import hashlib
from typing import Tuple
from .paths import library_dir, library_manifest_path

def _hash_file(path: str) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def _read_json(path: str) -> dict | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def _same_json(a: str, b: str) -> bool:
    ja = _read_json(a)
    jb = _read_json(b)
    if ja is None or jb is None:
        try:
            return os.path.getsize(a) == os.path.getsize(b)
        except Exception:
            return False
    return ja == jb

def _next_free_name(base_dir: str, filename: str) -> str:
    """
    Si filename existe y es distinto por contenido, genera nombre con sufijo:
    nombre.json -> nombre_2.json, nombre_3.json, ...
    """
    name, ext = os.path.splitext(filename)
    i = 2
    while True:
        cand = f"{name}_{i}{ext}"
        if not os.path.exists(os.path.join(base_dir, cand)):
            return cand
        i += 1

def _load_manifest() -> dict:
    path = library_manifest_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"files": {}}
    return {"files": {}}

def _save_manifest(manifest: dict):
    path = library_manifest_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

def import_from_source(source_dir: str) -> Tuple[int, int]:
    """
    Copia a la biblioteca interna los JSON nuevos según hash.
    Devuelve (copiados, ignorados).
    Reglas:
      - Calcula hash del archivo de origen.
      - Si hash ya está en el manifest -> ignorar.
      - Si no, copiar a biblioteca (si existe por nombre pero distinto contenido -> renombrar).
    """
    lib = library_dir()
    manifest = _load_manifest()
    copied = 0
    ignored = 0

    if not source_dir or not os.path.isdir(source_dir):
        return (0, 0)

    for entry in os.scandir(source_dir):
        if not entry.is_file() or not entry.name.lower().endswith(".json"):
            continue

        src = entry.path
        h = _hash_file(src)

        # Ya registrado en manifest -> ignorar
        if h in manifest["files"]:
            ignored += 1
            continue

        dst = os.path.join(lib, entry.name)

        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            copied += 1
            manifest["files"][h] = os.path.basename(dst)
        else:
            if _same_json(src, dst):
                ignored += 1
                manifest["files"][h] = os.path.basename(dst)
            else:
                new_name = _next_free_name(lib, entry.name)
                new_dst = os.path.join(lib, new_name)
                shutil.copy2(src, new_dst)
                copied += 1
                manifest["files"][h] = os.path.basename(new_dst)

    _save_manifest(manifest)
    return (copied, ignored)
