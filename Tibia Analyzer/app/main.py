import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase

# Cargamos la ventana principal y la config tal como están en tu proyecto
from app.services.config import load_config
from app.ui.main_window import MainWindow


def _base_dir() -> str:
    """
    Devuelve la carpeta base del bundle:
    - En desarrollo: .../app/..
    - En .exe (PyInstaller): sys._MEIPASS
    """
    if getattr(sys, "_MEIPASS", None):
        return sys._MEIPASS  # type: ignore[attr-defined]
    # /app/main.py -> base es un nivel arriba
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _res_path(*parts: str) -> str:
    """Ruta absoluta robusta para assets y qss."""
    return os.path.abspath(os.path.join(_base_dir(), *parts))


def _load_fonts():
    """
    Intenta registrar verdana.ttf (para mantener el look del cliente).
    Si no está, no pasa nada: PySide usará la fuente del sistema.
    """
    verdana = _res_path("assets", "verdana.ttf")
    if os.path.exists(verdana):
        ok_id = QFontDatabase.addApplicationFont(verdana)
        if ok_id == -1:
            print(f"[STYLE] No se pudo registrar la fuente: {verdana}")
        else:
            print(f"[STYLE] Fuente registrada: {verdana}")
    else:
        print(f"[STYLE] Fuente no encontrada (se ignora): {verdana}")


def _load_qss(app: QApplication):
    """
    Lee style.qss y sustituye {{ASSETS}} por la ruta absoluta de /assets,
    para que el QSS pueda encontrar ui_bg_dark.png y demás.
    Busca primero en app/ui/style.qss y luego en la raíz del proyecto.
    """
    candidates = [
        _res_path("app", "ui", "style.qss"),
        _res_path("style.qss"),
    ]
    qss_path = next((p for p in candidates if os.path.exists(p)), "")
    if not qss_path:
        print("[STYLE] style.qss no encontrado (se ejecutará sin tema).")
        return

    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            qss = f.read()
    except Exception as e:
        print(f"[STYLE] Error leyendo QSS: {e}")
        return

    assets_dir = _res_path("assets").replace("\\", "/")
    qss = qss.replace("{{ASSETS}}", assets_dir)

    app.setStyleSheet(qss)
    print(f"[STYLE] QSS cargado desde: {qss_path}")
    print(f"[STYLE] Assets dir: {assets_dir}")
    # Nota: en tu style.qss debe haber algo así:
    # QWidget { background-image: url({{ASSETS}}/ui_bg_dark.png); ... }
    # Con la sustitución anterior, quedará con la ruta absoluta correcta.


def main():
    cfg = load_config()
    app = QApplication(sys.argv)

    _load_fonts()
    _load_qss(app)

    win = MainWindow(cfg)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
