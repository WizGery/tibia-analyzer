import re
from datetime import datetime
from typing import Optional
from .schema import HuntRecord
from .schema import Vocation, Mode

_COMMA_RE = re.compile(r",")

LEVEL_BUCKETS = [
    "8-25","26-50","51-75","76-100","101-150","151-200",
    "201-250","251-300","301-350","351-400","401-450","451-500"
]

def parse_int(value: Optional[str]) -> int:
    if value is None:
        return 0
    if isinstance(value, int):
        return value
    try:
        return int(_COMMA_RE.sub("", str(value)))
    except ValueError:
        return 0

def parse_optional_int(value) -> Optional[int]:
    if value is None:
        return None
    try:
        s = _COMMA_RE.sub("", str(value))
        return int(s)
    except Exception:
        return None

def parse_duration_to_sec(duration_str: Optional[str]) -> int:
    if not duration_str or not isinstance(duration_str, str):
        return 0
    try:
        h, m = duration_str.replace("h", "").split(":")
        return int(h) * 3600 + int(m) * 60
    except Exception:
        return 0

def parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if not value or not isinstance(value, str):
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d, %H:%M:%S")
    except Exception:
        return None


def normalize_json(path: str, data: dict) -> HuntRecord:
    xp_gain = parse_int(data.get("XP Gain"))
    raw_xp_gain = parse_optional_int(data.get("Raw XP Gain"))  # puede faltar
    supplies = parse_int(data.get("Supplies"))
    loot = parse_int(data.get("Loot"))

    # Nuevo: Balance Real opcional
    balance_real = parse_optional_int(data.get("Balance Real"))
    # Si no hay Balance Real, usa Balance (o loot - supplies como fallback)
    balance_std = parse_int(data.get("Balance")) if "Balance" in data else (loot - supplies)
    balance = balance_real if balance_real is not None else balance_std

    start = parse_datetime(data.get("Session start"))
    end = parse_datetime(data.get("Session end"))
    duration_sec = parse_duration_to_sec(data.get("Session length"))

    vocation = (data.get("Vocation", "") or "").strip() or None
    mode = (data.get("Mode", "") or "").strip() or None
    vocation_duo = (data.get("Vocation duo", "") or "").strip() or None
    zona = (data.get("Zona", "") or "").strip() or None
    level_bucket = (data.get("Level", "") or "").strip() or None

    has_all_meta = True
    allowed_vocations = {v.value for v in Vocation}
    allowed_modes = {m.value for m in Mode}
    allowed_levels = set(LEVEL_BUCKETS)

    if not vocation or vocation not in allowed_vocations:
        has_all_meta = False
    if not mode or mode not in allowed_modes:
        has_all_meta = False
    if mode == "Solo" and vocation_duo != "none":
        has_all_meta = False
    if mode != "Solo" and (not vocation_duo or (vocation_duo not in allowed_vocations)):
        has_all_meta = False
    if not zona:
        has_all_meta = False
    if not level_bucket or level_bucket not in allowed_levels:
        has_all_meta = False
        
    # flag para ignorar balance en DUO (si lo marcaste manualmente)
    ignore_duo_balance = False
    try:
        raw = str(data.get("Ignore Duo Balance", "")).strip().lower()
        ignore_duo_balance = raw in ("1", "true", "yes", "y", "on")
    except Exception:
        ignore_duo_balance = False

    return HuntRecord(
        path=path,
        session_start=start,
        session_end=end,
        duration_sec=duration_sec,
        xp_gain=xp_gain,
        raw_xp_gain=raw_xp_gain,
        supplies=supplies,
        loot=loot,
        balance=balance,
        vocation=vocation,
        mode=mode,
        vocation_duo=vocation_duo,
        zona=zona,
        level_bucket=level_bucket,
        has_all_meta=has_all_meta,
        source_raw=data,
        ignore_duo_balance=ignore_duo_balance,   # ← NUEVO
    )