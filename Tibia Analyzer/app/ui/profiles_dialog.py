from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from app.data.schema import Vocation
from app.data.normalizer import LEVEL_BUCKETS
from app.services import profiles
from app.services import i18n

class ProfilesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(i18n.tr("profiles.title"))
        self.resize(520, 420)

        layout = QVBoxLayout(self)

        top = QHBoxLayout()
        self.list = QListWidget()
        self.list.itemSelectionChanged.connect(self._on_select)
        top.addWidget(self.list, 1)

        form = QVBoxLayout()
        self.lbl_name = QLabel(i18n.tr("profiles.name"))
        self.ed_name = QLineEdit()
        form.addWidget(self.lbl_name)
        form.addWidget(self.ed_name)

        self.lbl_voc = QLabel(i18n.tr("profiles.vocation"))
        self.cb_vocation = QComboBox()
        self.cb_vocation.addItems([v.value for v in Vocation])
        form.addWidget(self.lbl_voc)
        form.addWidget(self.cb_vocation)

        self.lbl_level = QLabel(i18n.tr("profiles.level"))
        self.cb_level = QComboBox()
        self.cb_level.addItems(LEVEL_BUCKETS)
        form.addWidget(self.lbl_level)
        form.addWidget(self.cb_level)

        btns = QHBoxLayout()
        self.btn_new = QPushButton(i18n.tr("profiles.new"))
        self.btn_save = QPushButton(i18n.tr("profiles.save"))
        self.btn_delete = QPushButton(i18n.tr("profiles.delete"))
        self.btn_new.clicked.connect(self._new)
        self.btn_save.clicked.connect(self._save)
        self.btn_delete.clicked.connect(self._delete)
        btns.addWidget(self.btn_new)
        btns.addWidget(self.btn_save)
        btns.addWidget(self.btn_delete)
        form.addStretch(1)
        form.addLayout(btns)

        top.addLayout(form, 1)
        layout.addLayout(top)

        self._reload_list()

    def _reload_list(self):
        self.list.clear()
        for p in profiles.list_profiles():
            item = QListWidgetItem(p.get("name", ""))
            item.setData(Qt.UserRole, p)
            self.list.addItem(item)

    def _on_select(self):
        items = self.list.selectedItems()
        if not items:
            self.ed_name.clear()
            self.cb_vocation.setCurrentIndex(0)
            self.cb_level.setCurrentIndex(0)
            return
        p = items[0].data(Qt.UserRole)
        self.ed_name.setText(p.get("name", ""))
        self.cb_vocation.setCurrentText(p.get("vocation", "Knight"))
        self.cb_level.setCurrentText(p.get("level", LEVEL_BUCKETS[0]))

    def _new(self):
        self.list.clearSelection()
        self.ed_name.clear()
        self.cb_vocation.setCurrentIndex(0)
        self.cb_level.setCurrentIndex(0)

    def _save(self):
        name = self.ed_name.text().strip()
        if not name:
            QMessageBox.warning(self, i18n.tr("profiles.title"), i18n.tr("profiles.msg.name_required"))
            return
        profiles.upsert_profile(
            name=name,
            vocation=self.cb_vocation.currentText(),
            level=self.cb_level.currentText()
        )
        self._reload_list()
        matches = self.list.findItems(name, Qt.MatchExactly)
        if matches:
            self.list.setCurrentItem(matches[0])

    def _delete(self):
        items = self.list.selectedItems()
        if not items:
            QMessageBox.information(self, i18n.tr("profiles.title"), i18n.tr("profiles.msg.select_first"))
            return
        name = items[0].text()
        ok = QMessageBox.question(
            self,
            i18n.tr("profiles.msg.delete.title"),
            i18n.tr("profiles.msg.delete.body", name=name),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if ok == QMessageBox.Yes:
            profiles.delete_profile(name)
            self._reload_list()
            self._new()
