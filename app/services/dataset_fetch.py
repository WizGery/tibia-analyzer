# app/services/dataset_fetch.py
from __future__ import annotations
import json
import os
import re
import tempfile
import hashlib
from typing import Dict, Tuple, List, Any, Set
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

from app.services.paths import library_dir
from app.services.library_sync import _same_json, _next_free_name

# --- Config del repo remoto ---
_GH_OWNER  = "WizGery"
_GH_REPO   = "tibia-analyzer"
_GH_BRANCH = "main"

_BASE_RAW     = f"https://raw.githubusercontent.com/{_GH_OWNER}/{_GH_REPO}/{_GH_BRANCH}/datasets/json"
_URL_MANIFEST = f"{_BASE_RAW}/MANIFEST.json"

# --- Archivo local de registro (se sincroniza con lo que haya físicamente) ---
def _seen_hashes_path() -> str:
    # Lo guardamos dentro de la propia biblioteca JSON del usuario
    return os.path.join(library_dir(), "_dataset_seen_hashes.json")


# =========================
# Utilidades locales
# =========================
def _http_get_text(url: str, timeout: int = 20) -> str:
    req = Request(url, headers={"User-Agent": "TibiaAnalyzer/1.0"})
    with urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def _http_get_bytes(url: str, timeout: int = 30) -> bytes:
    req = Request(url, headers={"User-Agent": "TibiaAnalyzer/1.0"})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _compute_sha256(path: str) -> str:
    """Devuelve el sha256 (hex) de un archivo local."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _scan_library_hashes() -> Set[str]:
    """
    Calcula los sha256 de todos los .json presentes en la biblioteca.
    Esto refleja exactamente lo que HAY en disco ahora mismo.
    """
    lib = library_dir()
    os.makedirs(lib, exist_ok=True)
    hashes: Set[str] = set()
    try:
        for entry in os.scandir(lib):
            if not entry.is_file():
                continue
            if not entry.name.lower().endswith(".json"):
                continue
            try:
                sha = _compute_sha256(entry.path)
                hashes.add(sha.lower())
            except Exception:
                # si no podemos leer uno, lo ignoramos sin romper el flujo
                pass
    except Exception:
        pass
    return hashes


def _load_seen_hashes() -> Set[str]:
    """Lee el archivo local si existe (lista de sha en JSON)."""
    p = _seen_hashes_path()
    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return set(str(x).lower() for x in data)
    except Exception:
        pass
    return set()


def _save_seen_hashes(seen: Set[str]) -> None:
    """Guarda el set de sha en disco (ordenado para diffs limpios)."""
    p = _seen_hashes_path()
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(sorted(seen), f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# =========================
# MANIFEST
# =========================
def fetch_manifest() -> Any:
    text = _http_get_text(_URL_MANIFEST)
    return json.loads(text)


def _normalize_entries(manifest: Any) -> List[Dict[str, str]]:
    """
    Acepta varios formatos de MANIFEST:
      - {"entries":[{"path":"by-hash/<sha>.json","original_name":"..."}]}
      - {"files":[...]}
      - ["by-hash/<sha>.json", ...]
      - [{"sha256":"...", "original_name":"..."}, ...]
      - [["by-hash/<sha>.json","Original.json"], ...]
      - etc.
    Produce una lista de dicts: {"path": "by-hash/<sha>.json", "original_name": "<name>.json"}
    """
    if isinstance(manifest, dict):
        entries = manifest.get("entries") or manifest.get("files") or []
    else:
        entries = manifest

    if not isinstance(entries, list):
        return []

    norm: List[Dict[str, str]] = []
    for it in entries:
        if isinstance(it, dict):
            path = str(it.get("path") or "").strip()
            sha  = str(it.get("sha256") or "").strip()
            orig = str(it.get("original_name") or it.get("name") or "").strip()

            if not path and sha:
                path = f"by-hash/{sha}.json"
            if not orig:
                orig = os.path.basename(path) if path else (sha + ".json" if sha else "hunt.json")

            if path and not path.startswith("by-hash/"):
                if path.endswith(".json") and "/" not in path:
                    path = f"by-hash/{path}"

            if path:
                norm.append({"path": path, "original_name": orig})
            continue

        if isinstance(it, str):
            s = it.strip()
            if not s:
                continue
            if s.startswith("by-hash/"):
                path = s
                orig = os.path.basename(s)
            else:
                if s.endswith(".json") and "/" not in s:
                    path = f"by-hash/{s}"
                    orig = s
                else:
                    path = f"by-hash/{s}.json"
                    orig = f"{s}.json"
            norm.append({"path": path, "original_name": orig})
            continue

        if isinstance(it, (list, tuple)) and len(it) == 2:
            p = str(it[0]).strip()
            o = str(it[1]).strip()
            if p and not p.startswith("by-hash/"):
                if p.endswith(".json") and "/" not in p:
                    p = f"by-hash/{p}"
            if not o:
                o = os.path.basename(p) if p else "hunt.json"
            if p:
                norm.append({"path": p, "original_name": o})
            continue

    return norm


_SHA_RE = re.compile(r"by-hash/([A-Fa-f0-9]{16,})\.json$")


def _extract_sha_from_path(path: str) -> str:
    m = _SHA_RE.search(path or "")
    return m.group(1).lower() if m else ""


# =========================
# Descarga principal
# =========================
def download_dataset_to_library() -> Tuple[int, int, int]:
    """
    Devuelve (copiados, ya_identicos, errores).

    Comportamiento clave:
    - No duplica por nombre ciegamente; deduplica por HASH (sha256) comparando
      contra lo que EXISTE en la biblioteca local ahora (escaneo real).
    - Si borras un archivo local, su hash ya no está en el set → se descarga de nuevo.
    - _dataset_seen_hashes.json se sincroniza con el estado físico de la carpeta.
    """
    lib = library_dir()
    os.makedirs(lib, exist_ok=True)

    # 1) Hashes que HAY ahora mismo en disco
    current_hashes = _scan_library_hashes()

    # 2) Sincronizamos el archivo local con lo que hay realmente
    _save_seen_hashes(current_hashes)

    # 3) Manifest remoto
    try:
        manifest = fetch_manifest()
    except Exception:
        # fallo de red o parsing
        return (0, 0, 1)

    entries = _normalize_entries(manifest)

    copied = 0
    identical = 0
    errors = 0

    for e in entries:
        by_hash_path = e.get("path", "").strip()
        original_name = e.get("original_name", "").strip()
        if not by_hash_path:
            continue
        if not original_name.lower().endswith(".json"):
            original_name = (original_name or "hunt") + ".json"

        sha_from_path = _extract_sha_from_path(by_hash_path)

        # 4) Si YA tenemos este hash en nuestra biblioteca, no descargamos.
        if sha_from_path and (sha_from_path in current_hashes):
            identical += 1
            continue

        file_url = f"{_BASE_RAW}/{by_hash_path}"
        try:
            blob = _http_get_bytes(file_url)
        except (URLError, HTTPError, Exception):
            errors += 1
            continue

        # Guardar temporal para comparaciones por contenido y calcular sha real
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tf:
                tmp_path = tf.name
                tf.write(blob)
        except Exception:
            errors += 1
            continue

        try:
            # Calculamos el hash REAL del blob descargado
            sha_real = ""
            try:
                sha_real = _compute_sha256(tmp_path)
            except Exception:
                pass

            # Si por lo que sea el sha del manifest no estaba, usamos el real para deduplicar
            key_sha = (sha_from_path or sha_real).lower()

            # Si (por otro motivo) ya está en la biblio tras calcular el real, evitamos duplicar
            if key_sha and (key_sha in current_hashes):
                identical += 1
            else:
                dst = os.path.join(lib, original_name)
                if not os.path.exists(dst):
                    # No existe el nombre: guardamos
                    with open(dst, "wb") as f:
                        f.write(blob)
                    copied += 1
                else:
                    # Ya existe ese nombre. ¿Contenido idéntico?
                    if _same_json(tmp_path, dst):
                        identical += 1
                    else:
                        # Contenido diferente → nuevo nombre incremental
                        new_name = _next_free_name(lib, original_name)
                        with open(os.path.join(lib, new_name), "wb") as f:
                            f.write(blob)
                        copied += 1

                # Añadimos el hash del que acabamos de dejar en disco
                if key_sha:
                    current_hashes.add(key_sha)

        except Exception:
            errors += 1
        finally:
            try:
                os.remove(tmp_path)
            except Exception:
                pass

    # 5) Guardamos el estado final (sincronizado con lo que HAY)
    _save_seen_hashes(current_hashes)
    return copied, identical, errors
