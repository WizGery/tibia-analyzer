# app/ui/tools_panel.py
from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QWidget, QMessageBox
)
from PySide6.QtCore import Qt

from app.services import i18n
from app.services import ui_prefs
from app.services.dataset_fetch import download_dataset_to_library
from app.ui.tools_stats_dialog import ToolsStatsDialog


class ToolsDialog(ui_prefs.PersistentSizeMixin, QDialog):
    def __init__(self, parent: QWidget | None, cfg: dict):
        super().__init__(parent)
        self.cfg = cfg

        # Persistencia de tamaño con ui_prefs (Mixin)
        self.init_persistent_size(self.cfg, key="tools_dialog", default=(560, 260))

        # UI
        self.setWindowTitle(i18n.tr("tools.title", default="Herramientas"))

        root = QVBoxLayout(self)

        # Encabezado
        title = QLabel(i18n.tr("tools.header", default="Utilidades"))
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title.setStyleSheet("font-weight: 700;")
        root.addWidget(title)

        # Fila principal de botones
        row = QHBoxLayout()

        # Descargar dataset (JSON verificados)
        self.btn_download = QPushButton(i18n.tr("tools.dataset.download", default="Descargar biblioteca"))
        self.btn_download.clicked.connect(self.on_download_dataset)
        row.addWidget(self.btn_download)

        # Estadísticas
        self.btn_stats = QPushButton(i18n.tr("tools.stats.open", default="Estadísticas…"))
        self.btn_stats.clicked.connect(self.on_open_stats)
        row.addWidget(self.btn_stats)

        row.addStretch(1)
        root.addLayout(row)

        # Pie / hint
        hint = QLabel("")
        hint.setStyleSheet("color: #aaaaaa;")
        root.addWidget(hint)

        # Botonera inferior (Cerrar)
        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        btn_close = QPushButton(i18n.tr("pending.close"))
        btn_close.clicked.connect(self.accept)
        btn_row.addWidget(btn_close)
        root.addLayout(btn_row)

    # Acciones
    def on_download_dataset(self):
        try:
            copied, identical, errors = download_dataset_to_library()
        except Exception as e:
            QMessageBox.critical(
                self,
                i18n.tr("tools.dataset.download", default="Descargar biblioteca"),
                f"{i18n.tr('tools.dataset.err', default='Error al descargar:')} {e}",
            )
            return

        msg = i18n.tr(
            "tools.dataset.result",
            default="Copiados: {copied} | Idénticos: {identical} | Errores: {errors}",
            copied=copied, identical=identical, errors=errors
        )
        QMessageBox.information(
            self,
            i18n.tr("tools.dataset.download", default="Descargar biblioteca"),
            msg
        )

    def on_open_stats(self):
        dlg = ToolsStatsDialog(self, self.cfg)
        dlg.exec()
