from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox
)
from PySide6.QtCore import Qt

from app.services import i18n, profiles as profiles_service, config, ui_prefs


class ProfilesDialog(ui_prefs.PersistentSizeMixin, QDialog):
    """Gestión de perfiles (personajes). Usa PersistentSizeMixin."""
    def __init__(self, parent=None):
        super().__init__(parent)
        cfg = config.load_config()
        self.init_persistent_size(cfg, key="profiles_dialog", default=(520, 420))

        self.setWindowTitle(i18n.tr("profiles.title"))

        root = QVBoxLayout(self)

        self.list = QListWidget()
        root.addWidget(self.list)

        # Campos
        form = QVBoxLayout()
        row_name = QHBoxLayout()
        row_name.addWidget(QLabel(i18n.tr("profiles.name")))
        self.ed_name = QLineEdit()
        row_name.addWidget(self.ed_name)
        form.addLayout(row_name)

        row_voc = QHBoxLayout()
        row_voc.addWidget(QLabel(i18n.tr("profiles.vocation")))
        self.cb_voc = QComboBox()
        self.cb_voc.addItems(["", "Knight", "Paladin", "Druid", "Sorcerer", "Monk"])
        row_voc.addWidget(self.cb_voc)
        form.addLayout(row_voc)

        row_lvl = QHBoxLayout()
        row_lvl.addWidget(QLabel(i18n.tr("profiles.level")))
        self.ed_level = QLineEdit()
        row_lvl.addWidget(self.ed_level)
        form.addLayout(row_lvl)
        root.addLayout(form)

        # Botonera
        btns = QHBoxLayout()
        self.btn_new = QPushButton(i18n.tr("profiles.new"))
        self.btn_save = QPushButton(i18n.tr("profiles.save"))
        self.btn_del = QPushButton(i18n.tr("profiles.delete"))
        btns.addStretch(1)
        btns.addWidget(self.btn_new)
        btns.addWidget(self.btn_save)
        btns.addWidget(self.btn_del)
        root.addLayout(btns)

        # Signals
        self.list.currentItemChanged.connect(self._on_select)
        self.btn_new.clicked.connect(self._on_new)
        self.btn_save.clicked.connect(self._on_save)
        self.btn_del.clicked.connect(self._on_delete)

        self._reload_list()

    # --- lógica perfiles ---
    def _reload_list(self):
        self.list.clear()
        for p in profiles_service.list_profiles():
            self.list.addItem(QListWidgetItem(p.get("name", "")))

    def _on_select(self, cur, _prev):
        if not cur:
            self.ed_name.clear()
            self.cb_voc.setCurrentIndex(0)
            self.ed_level.clear()
            return
        p = profiles_service.get_profile(cur.text())
        if p:
            self.ed_name.setText(p.get("name", ""))
            self.cb_voc.setCurrentText(p.get("vocation", ""))
            self.ed_level.setText(str(p.get("level", "")))

    def _on_new(self):
        self.list.clearSelection()
        self.ed_name.clear()
        self.cb_voc.setCurrentIndex(0)
        self.ed_level.clear()

    def _on_save(self):
        name = self.ed_name.text().strip()
        if not name:
            QMessageBox.warning(self, i18n.tr("profiles.title"), i18n.tr("profiles.msg.name_required"))
            return
        data = {"name": name, "vocation": self.cb_voc.currentText().strip(), "level": self.ed_level.text().strip()}
        profiles_service.save_profile(data)
        self._reload_list()
        items = self.list.findItems(name, Qt.MatchExactly)
        if items:
            self.list.setCurrentItem(items[0])

    def _on_delete(self):
        it = self.list.currentItem()
        if not it:
            QMessageBox.information(self, i18n.tr("profiles.title"), i18n.tr("profiles.msg.select_first"))
            return
        name = it.text()
        ok = QMessageBox.question(
            self, i18n.tr("profiles.title"),
            i18n.tr("profiles.msg.delete.body", name=name),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if ok == QMessageBox.Yes:
            profiles_service.delete_profile(name)
            self._reload_list()
            self._on_new()
