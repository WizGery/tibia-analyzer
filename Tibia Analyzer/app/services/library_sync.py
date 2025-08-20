import os
import json
import shutil
from typing import Tuple
from .paths import library_dir

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
        # si no se pueden leer, comparamos tamaño como fallback
        try:
            return os.path.getsize(a) == os.path.getsize(b)
        except Exception:
            return False
    return ja == jb  # comparación estructural

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

def import_from_source(source_dir: str) -> Tuple[int, int]:
    """
    Copia a la biblioteca interna los JSON que no estén.
    Devuelve (copiados, duplicados_ignorados).
    Regla:
      - Si no existe el nombre -> copiar.
      - Si existe el nombre:
          * Si contenido idéntico -> ignorar (duplicado).
          * Si distinto -> copiar con sufijo _2, _3, ...
    """
    lib = library_dir()
    copied = 0
    ignored = 0

    if not source_dir or not os.path.isdir(source_dir):
        return (0, 0)

    for entry in os.scandir(source_dir):
        if not entry.is_file():
            continue
        if not entry.name.lower().endswith(".json"):
            continue

        src = entry.path
        dst = os.path.join(lib, entry.name)

        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            copied += 1
            continue

        # Existe por nombre: comparar contenido
        if _same_json(src, dst):
            ignored += 1
        else:
            new_name = _next_free_name(lib, entry.name)
            shutil.copy2(src, os.path.join(lib, new_name))
            copied += 1

    return (copied, ignored)
