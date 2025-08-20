from typing import Dict

# ---------------- Catálogo ES ----------------
_STRINGS_ES: Dict[str, str] = {
    # App / MainWindow
    "app.title": "Tibia Analyzer",
    "language": "Idioma",
    "language.es": "Español",
    "language.en": "English",
    "source.choose": "Elegir carpeta origen (Tibia)…",
    "source.label.empty": "Origen: (no seleccionado)",
    "sync.now": "Sincronizar ahora",
    "library.label": "Biblioteca:",
    "pending.count": "Pendientes: {n}",
    "pending.manage": "Gestionar pendientes…",
    "profiles.open": "Perfiles…",
    "sync.msg.need_source": "Primero selecciona la carpeta de origen (Tibia).",
    "sync.msg.result": "Copiados: {copied}",
    "sync.msg.duplicates": " | Duplicados ignorados: {ignored}",
    "pending.none": "No hay archivos pendientes.",

    # FiltersPanel
    "filters.vocation": "Vocación",
    "filters.mode": "Modo",
    "filters.level": "Nivel",
    "filters.hilo": "High/Low",

    # ZonesTable (columnas)
    "zones.col.zone": "Zona",
    "zones.col.hunts": "Hunts",
    "zones.col.hours": "Horas",
    "zones.col.xp_h": "XP Gain/h",
    "zones.col.raw_h": "Raw XP/h",
    "zones.col.balance_h": "Balance/h",
    "zones.col.xp_h.min": "XP/h Mín",
    "zones.col.xp_h.max": "XP/h Máx",
    "zones.col.raw_h.min": "Raw/h Mín",
    "zones.col.raw_h.max": "Raw/h Máx",
    "zones.col.balance_h.min": "Bal/h Mín",
    "zones.col.balance_h.max": "Bal/h Máx",

    # PendingDialog (UI)
    "pending.title": "Pendientes de metadatos",
    "pending.info":
        "Edita los campos y pulsa 'Guardar cambios'. Se creará un .bak por archivo.\n"
        "Consejo: si la hunt es Duo, puedes calcular el Balance Real o marcar 'Ignorar Balance'.",
    "pending.profile": "Perfil:",
    "pending.load_profile_all": "Cargar perfil en todos",
    "pending.view_monsters": "Ver Monsters…",
    "pending.calc_balance": "Calcular balance…",
    "pending.save": "Guardar cambios",
    "pending.close": "Cerrar",

    # PendingDialog (columnas)
    "pending.col.file": "Archivo",
    "pending.col.vocation": "Vocación",
    "pending.col.mode": "Modo",
    "pending.col.vocation_duo": "Vocación duo",
    "pending.col.zone": "Zona",
    "pending.col.level": "Nivel",
    "pending.col.balance_real": "Balance Real",
    "pending.col.ignore_duo": "Ignorar Balance (Duo)",
    "pending.col.issues": "Problemas",

    # PendingDialog (mensajes)
    "pending.msg.select_row": "Selecciona primero una fila.",
    "pending.msg.not_duo": "Esta fila no es Duo.",
    "pending.msg.no_pending": "No hay archivos pendientes.",
    "pending.msg.saved_ok": "Se guardaron {n} archivos.",
    "pending.msg.saved_partial": "Se guardaron {ok} archivos, pero fallaron:\n\n{names}",
    "pending.msg.profile_select": "Selecciona un perfil primero.",
    "pending.msg.profile_not_found": "Perfil no encontrado.",
    "pending.msg.profile.apply.title": "Aplicar perfil",
    "pending.msg.profile.apply.body":
        "Se aplicará Vocación='{voc}' y Nivel='{lvl}' a TODOS los pendientes.\n\n¿Continuar?",
    "pending.msg.calc.paste": "Pega primero el texto de Party o Transfer.",
    "pending.msg.calc.not_detected": "No se reconoció Party ni Transfer en el texto.",
    "pending.msg.calc.result.title": "Balance Real",
    "pending.msg.calc.result.body": "Balance real calculado: {val}",

    # Issues (problemas) — ¡NUEVAS CLAVES!
    "pending.issue.missing_vocation": "Falta vocación",
    "pending.issue.missing_mode": "Falta modo",
    "pending.issue.missing_zone": "Falta zona",
    "pending.issue.missing_level": "Falta nivel",
    "pending.issue.invalid_vocation": "Vocación no válida",
    "pending.issue.invalid_mode": "Modo no válido",
    "pending.issue.invalid_level": "Nivel no válido",
    "pending.issue.duo_must_be_none": "En Solo, 'Vocación duo' debe ser 'none'",
    "pending.issue.duo_missing": "En Duo, selecciona 'Vocación duo'",
    "pending.issue.duo_cannot_equal_vocation": "En Duo, 'Vocación duo' no puede ser la misma que 'Vocación'",
    "pending.issue.balance_duo_required": "En Duo, indica Balance Real o marca 'Ignorar Balance'",

    # MonstersDialog
    "monsters.title": "Monstruos de la hunt",
    "monsters.col.name": "Monstruo",
    "monsters.col.count": "Cantidad",
    "monsters.btn.close": "Cerrar",
    "monsters.msg.read_error": "No se pudo leer el JSON:\n{err}",

    # ProfilesDialog
    "profiles.title": "Perfiles",
    "profiles.name": "Nombre del perfil (Personaje)",
    "profiles.vocation": "Vocación",
    "profiles.level": "Nivel",
    "profiles.new": "Nuevo",
    "profiles.save": "Guardar",
    "profiles.delete": "Eliminar",
    "profiles.msg.name_required": "El nombre del perfil no puede estar vacío.",
    "profiles.msg.select_first": "Selecciona primero un perfil.",
    "profiles.msg.delete.title": "Eliminar perfil",
    "profiles.msg.delete.body": "¿Eliminar el perfil '{name}'?",
}

# ---------------- Catálogo EN ----------------
_STRINGS_EN: Dict[str, str] = {
    # App / MainWindow
    "app.title": "Tibia Analyzer",
    "language": "Language",
    "language.es": "Spanish",
    "language.en": "English",
    "source.choose": "Choose source folder (Tibia)…",
    "source.label.empty": "Source: (not selected)",
    "sync.now": "Sync now",
    "library.label": "Library:",
    "pending.count": "Pending: {n}",
    "pending.manage": "Manage pending…",
    "profiles.open": "Profiles…",
    "sync.msg.need_source": "Please select the source folder (Tibia) first.",
    "sync.msg.result": "Copied: {copied}",
    "sync.msg.duplicates": " | Duplicates ignored: {ignored}",
    "pending.none": "No pending files.",

    # FiltersPanel
    "filters.vocation": "Vocation",
    "filters.mode": "Mode",
    "filters.level": "Level",
    "filters.hilo": "High/Low",

    # ZonesTable (columns)
    "zones.col.zone": "Zone",
    "zones.col.hunts": "Hunts",
    "zones.col.hours": "Hours",
    "zones.col.xp_h": "XP Gain/h",
    "zones.col.raw_h": "Raw XP/h",
    "zones.col.balance_h": "Balance/h",
    "zones.col.xp_h.min": "XP/h Min",
    "zones.col.xp_h.max": "XP/h Max",
    "zones.col.raw_h.min": "Raw/h Min",
    "zones.col.raw_h.max": "Raw/h Max",
    "zones.col.balance_h.min": "Bal/h Min",
    "zones.col.balance_h.max": "Bal/h Max",

    # PendingDialog (UI)
    "pending.title": "Pending metadata",
    "pending.info":
        "Edit the fields and click 'Save changes'. A .bak will be created per file.\n"
        "Tip: if the hunt is Duo, you can compute Real Balance or mark 'Ignore Balance'.",
    "pending.profile": "Profile:",
    "pending.load_profile_all": "Load profile to all",
    "pending.view_monsters": "View Monsters…",
    "pending.calc_balance": "Compute balance…",
    "pending.save": "Save changes",
    "pending.close": "Close",

    # PendingDialog (columns)
    "pending.col.file": "File",
    "pending.col.vocation": "Vocation",
    "pending.col.mode": "Mode",
    "pending.col.vocation_duo": "Vocation duo",
    "pending.col.zone": "Zone",
    "pending.col.level": "Level",
    "pending.col.balance_real": "Real Balance",
    "pending.col.ignore_duo": "Ignore Balance (Duo)",
    "pending.col.issues": "Issues",

    # PendingDialog (messages)
    "pending.msg.select_row": "Select a row first.",
    "pending.msg.not_duo": "This row is not Duo.",
    "pending.msg.no_pending": "No pending files.",
    "pending.msg.saved_ok": "{n} files saved.",
    "pending.msg.saved_partial": "{ok} files saved, but failed:\n\n{names}",
    "pending.msg.profile_select": "Select a profile first.",
    "pending.msg.profile_not_found": "Profile not found.",
    "pending.msg.profile.apply.title": "Apply profile",
    "pending.msg.profile.apply.body":
        "Vocation='{voc}' and Level='{lvl}' will be applied to ALL pending rows.\n\nContinue?",
    "pending.msg.calc.paste": "Paste Party or Transfer text first.",
    "pending.msg.calc.not_detected": "Party or Transfer not detected in the text.",
    "pending.msg.calc.result.title": "Real Balance",
    "pending.msg.calc.result.body": "Real balance computed: {val}",

    # Issues (problems) — NEW KEYS!
    "pending.issue.missing_vocation": "Missing vocation",
    "pending.issue.missing_mode": "Missing mode",
    "pending.issue.missing_zone": "Missing zone",
    "pending.issue.missing_level": "Missing level",
    "pending.issue.invalid_vocation": "Invalid vocation",
    "pending.issue.invalid_mode": "Invalid mode",
    "pending.issue.invalid_level": "Invalid level",
    "pending.issue.duo_must_be_none": "In Solo, 'Vocation duo' must be 'none'",
    "pending.issue.duo_missing": "In Duo, select 'Vocation duo'",
    "pending.issue.duo_cannot_equal_vocation": "In Duo, 'Vocation duo' cannot equal 'Vocation'",
    "pending.issue.balance_duo_required": "In Duo, provide Real Balance or mark 'Ignore Balance'",

    # MonstersDialog
    "monsters.title": "Hunt monsters",
    "monsters.col.name": "Monster",
    "monsters.col.count": "Count",
    "monsters.btn.close": "Close",
    "monsters.msg.read_error": "Could not read JSON:\n{err}",

    # ProfilesDialog
    "profiles.title": "Profiles",
    "profiles.name": "Profile name (Character)",
    "profiles.vocation": "Vocation",
    "profiles.level": "Level",
    "profiles.new": "New",
    "profiles.save": "Save",
    "profiles.delete": "Delete",
    "profiles.msg.name_required": "Profile name cannot be empty.",
    "profiles.msg.select_first": "Select a profile first.",
    "profiles.msg.delete.title": "Delete profile",
    "profiles.msg.delete.body": "Delete profile '{name}'?",
}

_current_lang = "es"
_catalogs = {"es": _STRINGS_ES, "en": _STRINGS_EN}

def set_language(lang: str) -> None:
    global _current_lang
    _current_lang = "en" if str(lang).lower().startswith("en") else "es"

def get_language() -> str:
    return _current_lang

def tr(key: str, **kwargs) -> str:
    cat = _catalogs.get(_current_lang, _STRINGS_ES)
    text = cat.get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
