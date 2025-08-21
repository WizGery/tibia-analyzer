from __future__ import annotations

import json
import os
from typing import List, Dict, Any, Tuple, Optional

from app.services import i18n

# Vocaciones, modos y niveles permitidos
ALLOWED_VOCS: List[str] = ["Knight", "Paladin", "Sorcerer", "Druid", "Monk"]
ALLOWED_MODES: List[str] = ["Solo", "Duo"]
ALLOWED_LEVELS: List[str] = [
    "8-25","26-50","51-75","76-100","101-150","151-200","201-250",
    "251-300","301-350","351-400","401-450","451-500"
]

# ---------------- Utilidades de lectura directa del JSON ----------------

def _read_json(path: str) -> Optional[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def _read_balance_real_and_ignore(path: str) -> Tuple[Optional[int], bool]:
    """
    Lee 'Balance Real' (si existe) y 'Ignore Duo Balance' del JSON.
    """
    data = _read_json(path)
    if not data:
        return (None, False)

    # Balance Real
    bal_real_raw = data.get("Balance Real", "")
    bal_val: Optional[int] = None
    if str(bal_real_raw).strip() != "":
        # limpiar separadores
        digits = "".join(ch for ch in str(bal_real_raw) if ch.isdigit() or ch == "-")
        try:
            bal_val = int(digits)
        except Exception:
            bal_val = None

    # Ignore flag
    raw_flag = str(data.get("Ignore Duo Balance", "")).strip().lower()
    ignore = raw_flag in ("1", "true", "yes", "y", "on")

    return (bal_val, ignore)

# ---------------- Reglas de consistencia ----------------

def coerce_consistency(meta: Dict[str, str]) -> Dict[str, str]:
    """
    Aplica reglas de consistencia sin tocar disco:
     - Si Mode == Solo => Vocation duo = 'none'
     - Si Mode == Duo  => Vocation duo no puede ser la misma que Vocation y no puede ser 'none'
    """
    m = dict(meta) if meta else {}
    mode = (m.get("Mode") or "").strip()
    voc  = (m.get("Vocation") or "").strip()
    duo  = (m.get("Vocation duo") or "").strip()

    if mode == "Solo":
        m["Vocation duo"] = "none"
    elif mode == "Duo":
        # Si el duo es inválido, lo vaciamos para que el usuario elija
        if not duo or duo == "none" or duo == voc:
            m["Vocation duo"] = ""
    return m

# ---------------- Detección de problemas (localizados) ----------------

def _issues_for_record(record) -> List[str]:
    """
    Recibe un HuntRecord (o estructura equivalente con atributos):
      - path, vocation, mode, vocation_duo, zona, level_bucket
    Devuelve lista de 'issues' ya traducidos según i18n.get_language().
    """
    issues: List[str] = []

    # Campos base
    vocation = (getattr(record, "vocation", None) or "").strip()
    mode = (getattr(record, "mode", None) or "").strip()
    zona = (getattr(record, "zona", None) or "").strip()
    level_bucket = (getattr(record, "level_bucket", None) or "").strip()
    duo = (getattr(record, "vocation_duo", None) or "").strip()

    # Faltantes / inválidos
    if not vocation:
        issues.append(i18n.tr("pending.issue.missing_vocation"))
    elif vocation not in ALLOWED_VOCS:
        issues.append(i18n.tr("pending.issue.invalid_vocation"))

    if not mode:
        issues.append(i18n.tr("pending.issue.missing_mode"))
    elif mode not in ALLOWED_MODES:
        issues.append(i18n.tr("pending.issue.invalid_mode"))

    if not zona:
        issues.append(i18n.tr("pending.issue.missing_zone"))

    if not level_bucket:
        issues.append(i18n.tr("pending.issue.missing_level"))
    elif level_bucket not in ALLOWED_LEVELS:
        issues.append(i18n.tr("pending.issue.invalid_level"))

    # Reglas Duo/Solo
    if mode == "Solo":
        if duo != "none":
            issues.append(i18n.tr("pending.issue.duo_must_be_none"))
    elif mode == "Duo":
        if not duo:
            issues.append(i18n.tr("pending.issue.duo_missing"))
        elif duo == "none" or (vocation and duo == vocation):
            # none o igual a la principal
            if duo == "none":
                issues.append(i18n.tr("pending.issue.duo_missing"))
            else:
                issues.append(i18n.tr("pending.issue.duo_cannot_equal_vocation"))

        # Balance Real o ignorado
        bal_real, ignore_flag = _read_balance_real_and_ignore(getattr(record, "path", ""))
        if bal_real is None and not ignore_flag:
            issues.append(i18n.tr("pending.issue.balance_duo_required"))

    return issues

# ---------------- API pública usada por la UI ----------------

def find_pending(hunts: List) -> List[Dict[str, Any]]:
    """
    Dada la lista de hunts (normalizadas), devuelve filas para el panel de pendientes:
    [
      {
        "path": str,
        "vocation": str,
        "mode": str,
        "vocation_duo": str,
        "zona": str,
        "level": str,
        "issues": [str, ...]  # ya traducidos según idioma actual
      },
      ...
    ]
    """
    rows: List[Dict[str, Any]] = []
    for h in hunts:
        issues = _issues_for_record(h)
        if not issues:
            continue
        rows.append({
            "path": getattr(h, "path", ""),
            "vocation": getattr(h, "vocation", "") or "",
            "mode": getattr(h, "mode", "") or "",
            "vocation_duo": getattr(h, "vocation_duo", "") or "",
            "zona": getattr(h, "zona", "") or "",
            "level": getattr(h, "level_bucket", "") or "",
            "issues": issues,
        })
    return rows
