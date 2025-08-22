# app/services/ui_prefs.py
from __future__ import annotations
from typing import Tuple, Dict, Any
from PySide6.QtWidgets import QWidget
from app.services import config as _config

# ---------------------------
# Funciones utilitarias
# ---------------------------

def _valid_size(val: Any) -> bool:
    try:
        return isinstance(val, (list, tuple)) and len(val) == 2 and int(val[0]) > 0 and int(val[1]) > 0
    except Exception:
        return False

def get_size(cfg: Dict[str, Any], key: str, default: Tuple[int, int]) -> Tuple[int, int]:
    """
    Lee de cfg["dialog_sizes"][key] un tamaño [w,h]. Si no existe o no es válido, devuelve 'default'.
    """
    if not isinstance(cfg, dict):
        return default
    node = cfg.get("dialog_sizes")
    if not isinstance(node, dict):
        return default
    val = node.get(key)
    if _valid_size(val):
        try:
            return int(val[0]), int(val[1])  # type: ignore[index]
        except Exception:
            return default
    return default

def save_size_cfg(cfg: Dict[str, Any], key: str, size: Tuple[int, int]) -> None:
    """
    Guarda cfg["dialog_sizes"][key] = [w,h] y persiste en disco.
    (Versión interna con 3 parámetros: cfg, key, size)
    """
    if not isinstance(cfg, dict):
        return
    try:
        w, h = int(size[0]), int(size[1])
        if w <= 0 or h <= 0:
            return
    except Exception:
        return

    node = cfg.get("dialog_sizes")
    if not isinstance(node, dict):
        node = {}
    node[key] = [size[0], size[1]]
    cfg["dialog_sizes"] = node
    try:
        _config.save_config(cfg)
    except Exception:
        pass

def apply_saved_size(widget: QWidget, cfg: Dict[str, Any], key: str, default: Tuple[int, int]) -> None:
    """
    Aplica al widget el tamaño guardado o 'default' si no hay guardado.
    """
    w, h = get_size(cfg, key, default)
    widget.resize(w, h)

def save_current_size(widget: QWidget, cfg: Dict[str, Any], key: str) -> None:
    """
    Guarda el tamaño actual del widget bajo 'key'.
    """
    save_size_cfg(cfg, key, (widget.width(), widget.height()))


# ---------------------------
# WRAPPERS sin 'cfg' (para usar directo en ventanas principales)
# ---------------------------

def load_size(widget: QWidget, key: str, default: Tuple[int, int] = (800, 600)) -> None:
    """
    Wrapper cómodo para ventanas principales:
    - Carga la config global.
    - Aplica el tamaño guardado (o 'default' si no existe).

    Uso:
      ui_prefs.load_size(self, "main_window_basic", default=(1120, 720))
    """
    try:
        cfg = _config.load_config()
    except Exception:
        cfg = {}
    apply_saved_size(widget, cfg, key, default)

def save_size_global(widget: QWidget, key: str) -> None:
    """
    Wrapper cómodo para ventanas principales:
    - Carga la config global.
    - Guarda el tamaño actual bajo 'key'.

    Uso:
      ui_prefs.save_size_global(self, "main_window_basic")
    """
    try:
        cfg = _config.load_config()
    except Exception:
        cfg = {}
    save_current_size(widget, cfg, key)

# Alias para mantener el nombre usado en tu MainWindow anterior
# (si ya llamabas a ui_prefs.save_size(self, "clave"), seguirá funcionando).
def save_size(widget: QWidget, key: str) -> None:  # type: ignore[override]
    save_size_global(widget, key)


# ---------------------------
# Mixin opcional para QDialog/QWidget
# ---------------------------

class PersistentSizeMixin:
    """
    Mezcla para recordar el tamaño de un QDialog/QWidget sin duplicar código.
    Uso:
      class MyDialog(QDialog, PersistentSizeMixin):
          def __init__(..., cfg):
              ...
              self.init_persistent_size(cfg, key="settings", default=(560, 260))

    - Aplica automáticamente el tamaño guardado en init.
    - Persiste al cerrar con la X (closeEvent), y al cerrar con botones (accept/reject/done).
    """
    _ps_cfg: Dict[str, Any] | None = None
    _ps_key: str = ""
    _ps_default: Tuple[int, int] = (600, 400)

    def init_persistent_size(self, cfg: Dict[str, Any], key: str, default: Tuple[int, int] = (600, 400)) -> None:
        self._ps_cfg = cfg
        self._ps_key = key
        self._ps_default = default
        try:
            apply_saved_size(self, cfg, key, default)
        except Exception:
            pass


    def _ps_save(self) -> None:
        if self._ps_cfg and self._ps_key:
            try:
                save_current_size(self, self._ps_cfg, self._ps_key)
            except Exception:
                pass

    # -- cubrimos cerrar con la X --
    def closeEvent(self, event):
        self._ps_save()
        try:
            super().closeEvent(event)  # type: ignore[misc]
        except Exception:
            pass

    # -- cubrimos cerrar con botones (OK/Cancel) --
    def accept(self):
        self._ps_save()
        try:
            super().accept()  # type: ignore[misc]
        except Exception:
            pass

    def reject(self):
        self._ps_save()
        try:
            super().reject()  # type: ignore[misc]
        except Exception:
            pass

    # (opcional) algunas clases cierran vía done(code)
    def done(self, r: int):
        self._ps_save()
        try:
            super().done(r)  # type: ignore[misc]
        except Exception:
            pass
