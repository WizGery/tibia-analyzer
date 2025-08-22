from typing import Dict

# =======================
# Catálogo ES (canónicas)
# =======================
_STRINGS_ES: Dict[str, str] = {
    # App / MainWindow
    "app.title": "Tibia Analyzer",
    "language.es": "Español",
    "language.en": "English",
    "source.choose": "Elegir carpeta origen (Tibia)",
    "sync.now": "Sincronizar ahora",
    "library.label": "Biblioteca:",
    "pending.manage": "Gestionar pendientes",
    "pending.manage_with_count": "Gestionar pendientes: {n}",
    "pending.none": "No hay archivos pendientes.",
    "profiles.open": "Perfiles",
    "sync.msg.need_source": "Primero selecciona la carpeta de origen (Tibia).",
    "sync.msg.result": "Copiados: {copied}",
    "sync.msg.duplicates": " | Duplicados ignorados: {ignored}",

    # Estado / contadores
    "settings.status": "Estado",
    "settings.source.count": "Archivos en origen: {n}",

    # Filtros
    "filters.vocation": "Vocación",
    "filters.mode": "Modo",
    "filters.level": "Nivel",
    "filters.hilo": "High/Low",

    # Settings
    "settings.title": "Ajustes",
    "settings.section.language": "Idioma",
    "settings.section.source": "Origen de JSON de Tibia",
    "settings.section.library": "Biblioteca local",
    "settings.source.choose": "Elegir carpeta de origen",
    "settings.library.choose": "Elegir carpeta de biblioteca",
    "settings.save": "Guardar",
    "settings.saved": "Ajustes guardados.",

    # Tools
    "tools.title": "Herramientas",
    "tools.dataset.download": "Descargar dataset (GitHub)",
    "tools.dataset.err": "Error al descargar:",
    "tools.dataset.result": "Descarga completada.\nCopiados: {copied}\nIdénticos ya existentes: {identical}\nErrores: {errors}",
    "tools.stats.open": "Estadísticas",
    "tools.stats.title": "Estadísticas",

    # ZonesTable (columnas específicas con min/max)
    "zones.col.xp_h.min": "XP/h Mín",
    "zones.col.xp_h.max": "XP/h Máx",
    "zones.col.raw_h.min": "Raw/h Mín",
    "zones.col.raw_h.max": "Raw/h Máx",
    "zones.col.balance_h.min": "Bal/h Mín",
    "zones.col.balance_h.max": "Bal/h Máx",

    # PendingDialog (cabecera y acciones)
    "pending.title": "Pendientes",
    "pending.info": "Información",
    "pending.profile": "Perfil",
    "pending.save": "Guardar",
    "pending.close": "Cerrar",
    "pending.load_profile_all": "Cargar perfil a todos",
    "pending.view_monsters": "Ver monstruos",
    "pending.calc_balance": "Calcular Balance",

    # PendingDialog (tabla)
    "pending.col.name": "Archivo",
    "pending.col.vocation": "Vocación",
    "pending.col.vocation_duo": "Vocación (Duo)",
    "pending.col.mode": "Modo",
    "pending.col.zone": "Zona",
    "pending.col.level": "Nivel",
    "pending.col.balance_real": "Balance Real",
    "pending.col.ignore_duo": "Ignorar Balance (Duo)",
    "pending.col.issues": "Problemas",

    # PendingDialog (mensajes)
    "pending.msg.select_row": "Selecciona primero una fila.",
    "pending.msg.not_duo": "Esta fila no es Duo.",
    "pending.msg.saved_ok": "Se guardaron {n} archivos.",
    "pending.msg.saved_partial": "Se guardaron {ok} archivos, pero fallaron:\n\n{names}",
    "pending.msg.profile.select": "Selecciona un perfil primero.",
    "pending.msg.profile.not_found": "Perfil no encontrado.",
    "pending.msg.profile.apply.title": "Aplicar perfil",
    "pending.msg.profile.apply.body":
        "Se aplicará Vocación='{voc}' y Nivel='{lvl}' a TODOS los pendientes.\n\n¿Continuar?",
    "pending.msg.calc.paste": "Pega primero el texto de Party o Transfer.",
    "pending.msg.calc.not_detected": "No se reconoció Party ni Transfer en el texto.",
    "pending.msg.calc.result.title": "Balance Real",
    "pending.msg.calc.result.body": "Balance real calculado: {val}",

    # Issues (problemas)
    "pending.issue.missing_vocation": "Falta vocación",
    "pending.issue.missing_mode": "Falta modo",
    "pending.issue.missing_zone": "Falta zona",
    "pending.issue.missing_level": "Falta nivel",
    "pending.issue.invalid_vocation": "Vocación no válida",
    "pending.issue.invalid_mode": "Modo no válido",
    "pending.issue.invalid_level": "Nivel no válido",
    "pending.issue.duo_must_be_none": "En Solo, 'Vocación duo' debe ser 'none'",
    "pending.issue.duo_missing": "En Duo, selecciona 'Vocación duo'",
    "pending.issue.duo_cannot_equal_vocation": "En Duo, 'Vocación duo' no puede ser igual a 'Vocación'",
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
    "profiles.msg.delete.body": "¿Eliminar el perfil '{name}'?",

    # ============
    # Etiquetas genéricas (canónicas)
    # ============
    "label.zone": "Zona",
    "label.hunts": "Hunts",
    "label.hours": "Horas",
    "label.xp_h": "XP Gain/h",
    "label.raw_h": "Raw XP/h",
    "label.balance_h": "Balance/h",
    "label.vocation": "Vocación",
    "label.mode": "Modo",
    "label.level": "Nivel",
    "label.profile": "Perfil",
    "label.info": "Información",
    "label.total": "Total",
    "label.solo": "Solo",
    "label.duo": "Duo",

    # Vocaciones (canónicas)
    "label.voc.knight": "Knight",
    "label.voc.paladin": "Paladin",
    "label.voc.druid": "Druid",
    "label.voc.sorcerer": "Sorcerer",
    "label.voc.monk": "Monk",

    # Acciones genéricas (canónicas)
    "action.save": "Guardar",
    "action.close": "Cerrar",
    "action.open": "Abrir",
    "action.new": "Nuevo",
    "action.delete": "Eliminar",
    "action.yes": "Sí",
    "action.no": "No",
}

# =======================
# Catálogo EN (canónicas)
# =======================
_STRINGS_EN: Dict[str, str] = {
    # App / MainWindow
    "app.title": "Tibia Analyzer",
    "language.es": "Spanish",
    "language.en": "English",
    "source.choose": "Choose source folder (Tibia)",
    "sync.now": "Sync now",
    "library.label": "Library:",
    "pending.manage": "Manage pending",
    "pending.manage_with_count": "Manage pending: {n}",
    "pending.none": "No pending files.",
    "profiles.open": "Profiles",
    "sync.msg.need_source": "Please select the source folder (Tibia) first.",
    "sync.msg.result": "Copied: {copied}",
    "sync.msg.duplicates": " | Duplicates ignored: {ignored}",

    # Status / counters
    "settings.status": "Status",
    "settings.source.count": "Files in source: {n}",

    # Filters
    "filters.vocation": "Vocation",
    "filters.mode": "Mode",
    "filters.level": "Level",
    "filters.hilo": "High/Low",

    # Settings
    "settings.title": "Settings",
    "settings.section.language": "Language",
    "settings.section.source": "Tibia JSON source",
    "settings.section.library": "Local library",
    "settings.source.choose": "Choose source folder",
    "settings.library.choose": "Choose library folder",
    "settings.save": "Save",
    "settings.saved": "Settings saved.",

    # Tools
    "tools.title": "Tools",
    "tools.dataset.download": "Download dataset (GitHub)",
    "tools.dataset.err": "Download error:",
    "tools.dataset.result": "Download completed.\nCopied: {copied}\nIdentical existing: {identical}\nErrors: {errors}",
    "tools.stats.open": "Statistics",
    "tools.stats.title": "Statistics",

    # ZonesTable (specific min/max columns)
    "zones.col.xp_h.min": "XP/h Min",
    "zones.col.xp_h.max": "XP/h Max",
    "zones.col.raw_h.min": "Raw/h Min",
    "zones.col.raw_h.max": "Raw/h Max",
    "zones.col.balance_h.min": "Bal/h Min",
    "zones.col.balance_h.max": "Bal/h Max",

    # PendingDialog (header & actions)
    "pending.title": "Pending",
    "pending.info": "Info",
    "pending.profile": "Profile",
    "pending.save": "Save",
    "pending.close": "Close",
    "pending.load_profile_all": "Load profile to all",
    "pending.view_monsters": "View monsters",
    "pending.calc_balance": "Calc Balance",

    # PendingDialog (table)
    "pending.col.name": "File",
    "pending.col.vocation": "Vocation",
    "pending.col.vocation_duo": "Vocation (Duo)",
    "pending.col.mode": "Mode",
    "pending.col.zone": "Zone",
    "pending.col.level": "Level",
    "pending.col.balance_real": "Real Balance",
    "pending.col.ignore_duo": "Ignore Balance (Duo)",
    "pending.col.issues": "Issues",

    # PendingDialog (messages)
    "pending.msg.select_row": "Select a row first.",
    "pending.msg.not_duo": "This row is not Duo.",
    "pending.msg.saved_ok": "{n} files saved.",
    "pending.msg.saved_partial": "{ok} files saved, but failed:\n\n{names}",
    "pending.msg.profile.select": "Select a profile first.",
    "pending.msg.profile.not_found": "Profile not found.",
    "pending.msg.profile.apply.title": "Apply profile",
    "pending.msg.profile.apply.body":
        "Vocation='{voc}' and Level='{lvl}' will be applied to ALL pending.\n\nContinue?",
    "pending.msg.calc.paste": "Paste Party or Transfer text first.",
    "pending.msg.calc.not_detected": "Party or Transfer not detected.",
    "pending.msg.calc.result.title": "Real Balance",
    "pending.msg.calc.result.body": "Calculated real balance: {val}",

    # Issues
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
    "profiles.msg.delete.body": "Delete profile '{name}'?",

    # ============
    # Generic labels (canonical)
    # ============
    "label.zone": "Zone",
    "label.hunts": "Hunts",
    "label.hours": "Hours",
    "label.xp_h": "XP Gain/h",
    "label.raw_h": "Raw XP/h",
    "label.balance_h": "Balance/h",
    "label.vocation": "Vocation",
    "label.mode": "Mode",
    "label.level": "Level",
    "label.profile": "Profile",
    "label.info": "Info",
    "label.total": "Total",
    "label.solo": "Solo",
    "label.duo": "Duo",

    # Vocations (canonical)
    "label.voc.knight": "Knight",
    "label.voc.paladin": "Paladin",
    "label.voc.druid": "Druid",
    "label.voc.sorcerer": "Sorcerer",
    "label.voc.monk": "Monk",

    # Generic actions (canonical)
    "action.save": "Save",
    "action.close": "Close",
    "action.open": "Open",
    "action.new": "New",
    "action.delete": "Delete",
    "action.yes": "Yes",
    "action.no": "No",
}

# ==========================================
# Aliases: claves contextuales -> canónicas
# ==========================================
_ALIASES: Dict[str, str] = {
    # Duplicados claros
    "tools.header": "tools.title",
    "pending.col.file": "pending.col.name",

    # Columnas / labels repetidos (zona, horas, hunts, etc.)
    "tools.stats.zone": "label.zone",
    "zones.col.zone": "label.zone",
    "pending.col.zone": "label.zone",

    "tools.stats.hunts": "label.hunts",
    "zones.col.hunts": "label.hunts",

    "tools.stats.hours": "label.hours",
    "zones.col.hours": "label.hours",

    "tools.stats.xp_h": "label.xp_h",
    "zones.col.xp_h": "label.xp_h",

    "tools.stats.raw_h": "label.raw_h",
    "zones.col.raw_h": "label.raw_h",

    "tools.stats.balance_h": "label.balance_h",
    "zones.col.balance_h": "label.balance_h",

    # Totales, modos (estadística)
    "tools.stats.total": "label.total",
    "tools.stats.solo": "label.solo",
    "tools.stats.duo": "label.duo",

    # Vocaciones (estadística)
    "tools.stats.voc.knight": "label.voc.knight",
    "tools.stats.voc.paladin": "label.voc.paladin",
    "tools.stats.voc.druid": "label.voc.druid",
    "tools.stats.voc.sorcerer": "label.voc.sorcerer",
    "tools.stats.voc.monk": "label.voc.monk",

    # Acciones comunes (botones)
    "pending.save": "action.save",
    "profiles.save": "action.save",
    "settings.save": "action.save",
    "pending.close": "action.close",
    "monsters.btn.close": "action.close",

    # Apertura de diálogos
    "tools.stats.open": "tools.stats.title",

    # Corrección de variante con guion bajo
    "pending.msg.profile_select": "pending.msg.profile.select",
}

_current_lang = "es"
_catalogs = {"es": _STRINGS_ES, "en": _STRINGS_EN}

def set_language(lang: str) -> None:
    """Establece el idioma activo ('es' o 'en')."""
    global _current_lang
    _current_lang = "en" if str(lang).lower().startswith("en") else "es"

def get_language() -> str:
    """Devuelve el idioma actual."""
    return _current_lang

def tr(key: str, **kwargs) -> str:
    """Traduce una clave; si falta, devuelve la clave literal. Soporta alias."""
    real_key = _ALIASES.get(key, key)
    cat = _catalogs.get(_current_lang, _STRINGS_ES)
    text = cat.get(real_key, real_key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
