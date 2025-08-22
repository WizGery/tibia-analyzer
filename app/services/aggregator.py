# app/services/aggregator.py
from collections import defaultdict
from typing import Iterable, List, Optional
from app.data.schema import HuntRecord, AggregatedZone

def _hours(sec: int) -> float:
    return sec / 3600.0 if sec else 0.0

def _has_real_balance(h: HuntRecord) -> bool:
    """
    True si el registro tiene un 'Balance Real' presente.
    Intentamos varias variantes por compatibilidad con el loader.
    """
    for attr in ("balance_real", "balance_real_value", "has_real_balance"):
        v = getattr(h, attr, None)
        if v is None:
            continue
        s = str(v).strip()
        if s != "":
            return True
    return False

def aggregate_by_zone(
    hunts: Iterable[HuntRecord],
    vocation: Optional[str],
    mode: Optional[str],
    level_filter: Optional[str] = None,  # "All" o un bucket
) -> List[AggregatedZone]:
    filtered: List[HuntRecord] = []
    for h in hunts:
        if not h.has_all_meta or not h.zona:
            continue
        if vocation and h.vocation != vocation:
            continue
        if mode and h.mode != mode:
            continue
        if level_filter and level_filter != "All":
            if h.level_bucket != level_filter:
                continue
        filtered.append(h)

    bucket = defaultdict(lambda: {
        "hunts": 0,
        "sec_sum": 0,
        "raw_sec_sum": 0,
        "bal_sec_sum": 0,     # ← denominador (horas) SOLO de hunts que cuentan para balance
        "xp_sum": 0,
        "raw_sum": 0,
        "sup_sum": 0,
        "loot_sum": 0,
        "bal_sum": 0,         # ← numerador SOLO de hunts que cuentan para balance
        "xp_list": [],
        "raw_list": [],
        "sup_list": [],
        "loot_list": [],
        "bal_list": [],       # ← lista para min/máx SOLO de hunts que cuentan para balance
    })

    for h in filtered:
        hrs = _hours(h.duration_sec)
        b = bucket[h.zona]

        b["hunts"] += 1
        b["sec_sum"] += h.duration_sec
        b["xp_sum"]  += h.xp_gain
        b["sup_sum"] += h.supplies
        b["loot_sum"]+= h.loot

        # ----- REGLA DE BALANCE -----
        # Si el filtro Mode == "Duo": SOLO computan hunts con Balance Real y SIN "Ignorar Balance".
        # En otros modos: mantenemos tu comportamiento previo (excluir Duo ignoradas).
        ignore_flag = bool(getattr(h, "ignore_duo_balance", False))
        if mode == "Duo":
            include_balance = _has_real_balance(h) and not ignore_flag
        else:
            include_balance = not (h.mode == "Duo" and ignore_flag)

        if include_balance:
            b["bal_sum"] += h.balance

        # Listas por hora (para medias simples y min/máx)
        if hrs > 0:
            b["xp_list"].append(h.xp_gain / hrs)
            b["sup_list"].append(h.supplies / hrs)
            b["loot_list"].append(h.loot / hrs)
            if include_balance:
                b["bal_list"].append(h.balance / hrs)

        # RAW (si está presente, acumulamos y calculamos por horas de los que lo tienen)
        if h.raw_xp_gain is not None:
            b["raw_sum"] += h.raw_xp_gain
            b["raw_sec_sum"] += h.duration_sec
            if hrs > 0:
                b["raw_list"].append(h.raw_xp_gain / hrs)

        # Denominador específico de Balance (solo hunts que cuentan para balance)
        if include_balance:
            b["bal_sec_sum"] += h.duration_sec

    rows = []
    for zona, b in bucket.items():
        hrs_total = _hours(b["sec_sum"])
        hrs_raw   = _hours(b["raw_sec_sum"])
        hrs_bal   = _hours(b["bal_sec_sum"])

        xp_h  = (b["xp_sum"]  / hrs_total) if hrs_total > 0 else 0.0
        sup_h = (b["sup_sum"] / hrs_total) if hrs_total > 0 else 0.0
        loot_h= (b["loot_sum"]/ hrs_total) if hrs_total > 0 else 0.0
        bal_h = (b["bal_sum"] / hrs_bal)   if hrs_bal   > 0 else 0.0  # ← usa denominador de balance
        raw_h = (b["raw_sum"] / hrs_raw)   if hrs_raw   > 0 else 0.0

        # min/max
        def _minmax(lst): return (min(lst), max(lst)) if lst else (0.0, 0.0)
        xp_min, xp_max = _minmax(b["xp_list"])
        raw_min, raw_max = _minmax(b["raw_list"])
        sup_min, sup_max = _minmax(b["sup_list"])
        loot_min, loot_max = _minmax(b["loot_list"])
        bal_min, bal_max = _minmax(b["bal_list"])

        rows.append(AggregatedZone(
            zona=zona,
            hunts=b["hunts"],
            hours_total=hrs_total,
            xp_gain_per_h=xp_h,
            raw_xp_gain_per_h=raw_h,
            supplies_per_h=sup_h,
            loot_per_h=loot_h,
            balance_per_h=bal_h,
            xp_gain_per_h_min=xp_min,  xp_gain_per_h_max=xp_max,
            raw_xp_gain_per_h_min=raw_min, raw_xp_gain_per_h_max=raw_max,
            supplies_per_h_min=sup_min, supplies_per_h_max=sup_max,
            loot_per_h_min=loot_min,   loot_per_h_max=loot_max,
            balance_per_h_min=bal_min, balance_per_h_max=bal_max,
        ))

    rows.sort(key=lambda r: r.balance_per_h, reverse=True)
    return rows
