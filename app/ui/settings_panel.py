from __future__ import annotations

import os
from typing import Callable, Optional

from PySide6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QFileDialog
)
from PySide6.QtCore import Qt

from app.services import i18n, config
from app.services import ui_prefs


class SettingsDialog(ui_prefs.PersistentSizeMixin, QDialog):
    """
    Ajustes de la aplicación (idioma, carpeta fuente).
    Ahora recuerda su tamaño con ui_prefs.PersistentSizeMixin.
    """
    def __init__(
        self,
        parent: QWidget | None,
        cfg: dict,
        on_sync_done: Optional[Callable[[], None]] = None,
        on_language_changed: Optional[Callable[[], None]] = None,
    ):
        super().__init__(parent)
        self.cfg = cfg
        self._on_sync_done = on_sync_done
        self._on_language_changed = on_language_changed

        # Persistencia de tamaño
        self.init_persistent_size(self.cfg, key="settings_dialog", default=(460, 340))

        self.setWindowTitle(i18n.tr("settings.title"))

        root = QVBoxLayout(self)

        # Idioma
        row_lang = QHBoxLayout()
        self.lbl_language = QLabel(i18n.tr("settings.section.language"))
        self.cb_language = QComboBox()
        self.cb_language.addItem(i18n.tr("language.es"), userData="es")
        self.cb_language.addItem(i18n.tr("language.en"), userData="en")
        self.cb_language.setCurrentIndex(0 if (i18n.get_language() == "es") else 1)
        self.cb_language.currentIndexChanged.connect(self._on_language_combo_changed)
        row_lang.addWidget(self.lbl_language)
        row_lang.addWidget(self.cb_language, 1)
        root.addLayout(row_lang)

        # Origen JSON
        self.lbl_src_title = QLabel(i18n.tr("settings.section.source"))
        self.lbl_src_title.setStyleSheet("font-weight: 600;")
        root.addWidget(self.lbl_src_title)

        self.lbl_status = QLabel("")
        root.addWidget(self.lbl_status)

        self.btn_choose_src = QPushButton(i18n.tr("source.choose"))
        self.btn_choose_src.clicked.connect(self._choose_source_folder)
        root.addWidget(self.btn_choose_src)

        # Cerrar
        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        self.btn_close = QPushButton(i18n.tr("pending.close"))
        self.btn_close.clicked.connect(self.accept)
        btn_row.addWidget(self.btn_close)
        root.addLayout(btn_row)

        self._refresh_source_status()

    # --- eventos ---
    def _on_language_combo_changed(self, _idx: int):
        lang = self.cb_language.currentData() or "es"
        i18n.set_language(lang)
        self.cfg["language"] = i18n.get_language()
        config.save_config(self.cfg)
        if self._on_language_changed:
            self._on_language_changed()
        self._refresh_source_status()

    def _choose_source_folder(self):
        base = self.cfg.get("source_folder") or os.path.expanduser("~")
        folder = QFileDialog.getExistingDirectory(self, i18n.tr("source.choose"), base)
        if not folder:
            return
        self.cfg["source_folder"] = folder
        config.save_config(self.cfg)
        self._refresh_source_status()
        if self._on_sync_done:
            self._on_sync_done()

    def _refresh_source_status(self):
        src = self.cfg.get("source_folder") or ""
        if not src or not os.path.isdir(src):
            status = f"{i18n.tr('settings.status')} {i18n.tr('settings.source.none')}"
        else:
            count = len([f for f in os.listdir(src) if f.lower().endswith(".json")])
            status = f"{i18n.tr('settings.status')} {i18n.tr('settings.source.count', n=count)}"
        self.lbl_status.setText(status)
