from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox
from app.services import i18n

class FiltersPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._lbl_voc = QLabel()
        self._lbl_mode = QLabel()
        self._lbl_level = QLabel()

        self.cb_vocation = QComboBox()
        self.cb_mode = QComboBox()
        self.cb_level = QComboBox()
        self.chk_hilo = QCheckBox()

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)

        lay.addWidget(self._lbl_voc)
        lay.addWidget(self.cb_vocation)

        lay.addWidget(self._lbl_mode)
        lay.addWidget(self.cb_mode)

        lay.addWidget(self._lbl_level)
        lay.addWidget(self.cb_level)

        lay.addWidget(self.chk_hilo)
        lay.addStretch(1)

        self.retranslate_ui()

    # setters dinámicos (solo con datos)
    def set_available_vocations(self, vocs: list[str], default: str | None = None):
        cur = self.cb_vocation.currentText()
        self.cb_vocation.blockSignals(True)
        self.cb_vocation.clear()
        for v in sorted(vocs):
            self.cb_vocation.addItem(v)
        if default and default in vocs:
            self.cb_vocation.setCurrentText(default)
        elif cur in vocs:
            self.cb_vocation.setCurrentText(cur)
        elif self.cb_vocation.count():
            self.cb_vocation.setCurrentIndex(0)
        self.cb_vocation.blockSignals(False)

    def set_available_modes(self, modes: list[str], default: str | None = None):
        cur = self.cb_mode.currentText()
        self.cb_mode.blockSignals(True)
        self.cb_mode.clear()
        for m in sorted(modes):
            self.cb_mode.addItem(m)
        if default and default in modes:
            self.cb_mode.setCurrentText(default)
        elif cur in modes:
            self.cb_mode.setCurrentText(cur)
        elif self.cb_mode.count():
            self.cb_mode.setCurrentIndex(0)
        self.cb_mode.blockSignals(False)

    def set_available_levels(self, levels: list[str]):
        cur = self.cb_level.currentText()
        self.cb_level.blockSignals(True)
        self.cb_level.clear()
        self.cb_level.addItem("All")
        for lv in sorted(levels, key=lambda s: (len(s), s)):
            self.cb_level.addItem(lv)
        if cur == "All" or cur in levels:
            self.cb_level.setCurrentText(cur)
        else:
            self.cb_level.setCurrentText("All")
        self.cb_level.blockSignals(False)

    # getters
    def current_vocation(self) -> str:
        return self.cb_vocation.currentText()

    def current_mode(self) -> str:
        return self.cb_mode.currentText()

    def current_level(self) -> str:
        return self.cb_level.currentText()

    def show_hi_lo(self) -> bool:
        return self.chk_hilo.isChecked()

    def retranslate_ui(self):
        self._lbl_voc.setText(i18n.tr("filters.vocation"))
        self._lbl_mode.setText(i18n.tr("filters.mode"))
        self._lbl_level.setText(i18n.tr("filters.level"))
        self.chk_hilo.setText(i18n.tr("filters.hilo"))
