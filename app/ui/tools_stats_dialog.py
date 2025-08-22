from __future__ import annotations

from collections import Counter
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout, QFrame
)
from PySide6.QtCore import Qt

from app.services import i18n, ui_prefs
from app.data.loader import load_hunts_from_library


class ToolsStatsDialog(ui_prefs.PersistentSizeMixin, QDialog):
    """Estadísticas básicas de hunts. Recuerda tamaño con ui_prefs."""
    def __init__(self, parent, cfg: dict):
        super().__init__(parent)
        self.cfg = cfg

        self.init_persistent_size(self.cfg, key="tools_stats_dialog", default=(440, 320))
        self.setWindowTitle(i18n.tr("tools.stats.title", default="Estadísticas"))

        root = QVBoxLayout(self)

        hunts = load_hunts_from_library()
        total = len(hunts)
        voc_counter = Counter([h.vocation for h in hunts if getattr(h, "vocation", None)])
        mode_counter = Counter([h.mode for h in hunts if getattr(h, "mode", None)])

        # Totales
        box_total = QFrame()
        lt_total = QGridLayout(box_total)
        lt_total.addWidget(QLabel(i18n.tr("tools.stats.total", default="Total")), 0, 0, Qt.AlignLeft)
        lt_total.addWidget(QLabel(str(total)), 0, 1, Qt.AlignRight)
        root.addWidget(box_total)

        # Vocaciones
        box_voc = QFrame()
        lt_voc = QGridLayout(box_voc)
        voc_names = ["Knight", "Paladin", "Druid", "Sorcerer", "Monk"]
        row = 1
        for v in voc_names:
            lt_voc.addWidget(QLabel(i18n.tr(f"tools.stats.voc.{v.lower()}", default=v)), row, 0, Qt.AlignLeft)
            lt_voc.addWidget(QLabel(str(voc_counter.get(v, 0))), row, 1, Qt.AlignRight)
            row += 1
        root.addWidget(box_voc)

        # Modo
        box_mode = QFrame()
        lt_mode = QGridLayout(box_mode)
        lt_mode.addWidget(QLabel(i18n.tr("tools.stats.solo", default="Solo")), 1, 0, Qt.AlignLeft)
        lt_mode.addWidget(QLabel(str(mode_counter.get("Solo", 0))), 1, 1, Qt.AlignRight)
        lt_mode.addWidget(QLabel(i18n.tr("tools.stats.duo", default="Duo")), 2, 0, Qt.AlignLeft)
        lt_mode.addWidget(QLabel(str(mode_counter.get("Duo", 0))), 2, 1, Qt.AlignRight)
        root.addWidget(box_mode)

        # Botón cerrar
        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        btn_close = QPushButton(i18n.tr("pending.close"))
        btn_close.clicked.connect(self.accept)
        btn_row.addWidget(btn_close)
        root.addLayout(btn_row)
