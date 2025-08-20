from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime

class Vocation(str, Enum):
    KNIGHT = "Knight"
    PALADIN = "Paladin"
    SORCERER = "Sorcerer"
    DRUID = "Druid"
    MONK = "Monk"

class Mode(str, Enum):
    SOLO = "Solo"
    DUO = "Duo"

@dataclass
class HuntRecord:
    path: str
    session_start: datetime
    session_end: Optional[datetime]
    duration_sec: int
    xp_gain: int
    raw_xp_gain: Optional[int]   # puede faltar
    supplies: int
    loot: int
    balance: int
    vocation: Optional[str]
    mode: Optional[str]
    vocation_duo: Optional[str]
    zona: Optional[str]
    level_bucket: Optional[str]  # nuevo: "301-350", etc.
    has_all_meta: bool
    source_raw: dict
    ignore_duo_balance: bool = False 

@dataclass
class AggregatedZone:
    zona: str
    hunts: int
    hours_total: float
    xp_gain_per_h: float
    raw_xp_gain_per_h: float
    supplies_per_h: float
    loot_per_h: float
    balance_per_h: float
    xp_gain_per_h_min: float = 0.0
    xp_gain_per_h_max: float = 0.0
    raw_xp_gain_per_h_min: float = 0.0
    raw_xp_gain_per_h_max: float = 0.0
    supplies_per_h_min: float = 0.0
    supplies_per_h_max: float = 0.0
    loot_per_h_min: float = 0.0
    loot_per_h_max: float = 0.0
    balance_per_h_min: float = 0.0
    balance_per_h_max: float = 0.0
