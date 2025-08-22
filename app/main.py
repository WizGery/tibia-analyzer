import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from app.services.paths import asset_path
from app.services.config import load_config
from app.ui.main_window import MainWindow


def _load_fonts():
    """Intenta registrar Verdana (opcional)."""
    verdana = asset_path("assets", "fonts", "verdana.ttf")
    if verdana.exists():
        ok_id = QFontDatabase.addApplicationFont(str(verdana))
        if ok_id == -1:
            print(f"[STYLE] No se pudo registrar la fuente: {verdana}")
        else:
            print(f"[STYLE] Fuente registrada: {verdana}")
    else:
        print(f"[STYLE] Fuente no encontrada (se ignora): {verdana}")


def _load_qss(app: QApplication):
    """
    Lee assets/style.qss y sustituye {{ASSETS}} por la ruta absoluta a /assets
    para que las imágenes (backgrounds, iconos) funcionen también en .exe.
    """
    qss_path = asset_path("assets", "style.qss")
    if not qss_path.exists():
        print("[STYLE] style.qss no encontrado en assets/ (se ejecutará sin tema).")
        return

    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            qss = f.read()
    except Exception as e:
        print(f"[STYLE] Error leyendo QSS: {e}")
        return

    assets_dir = asset_path("assets").as_posix()
    qss = qss.replace("{{ASSETS}}", assets_dir)

    app.setStyleSheet(qss)
    print(f"[STYLE] QSS cargado desde: {qss_path}")
    print(f"[STYLE] Assets dir: {assets_dir}")


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
