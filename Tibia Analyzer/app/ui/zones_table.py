from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt
from app.services import i18n

# ---------------------------
# Ítems con ordenación numérica
# ---------------------------
class _NumericItem(QTableWidgetItem):
    def __init__(self, display_text: str, number_value: float):
        super().__init__(display_text)
        self._num = float(number_value or 0.0)
        # centrado para columnas numéricas
        self.setTextAlignment(Qt.AlignCenter)
        # no editable/seleccionable como antes
        self.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def __lt__(self, other):
        # Si el otro también es numérico, comparamos por número
        if isinstance(other, _NumericItem):
            return self._num < other._num
        # Si no, caemos al comportamiento por defecto (texto)
        return super().__lt__(other)


class ZonesTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._show_hi_lo = False

        self.table = QTableWidget(0, 6)
        self.table.setSortingEnabled(True)  # ← habilita ordenación por cabeceras
        self._set_headers_basic()

        lay = QVBoxLayout(self)
        lay.addWidget(self.table)

    # ---------------------------
    # Encabezados
    # ---------------------------
    def _set_headers_basic(self):
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            i18n.tr("zones.col.zone"),
            i18n.tr("zones.col.hunts"),
            i18n.tr("zones.col.hours"),
            i18n.tr("zones.col.xp_h"),
            i18n.tr("zones.col.raw_h"),
            i18n.tr("zones.col.balance_h"),
        ])
        self.table.resizeColumnsToContents()

    def _set_headers_hilo(self):
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            i18n.tr("zones.col.zone"),
            i18n.tr("zones.col.hunts"),
            i18n.tr("zones.col.hours"),
            i18n.tr("zones.col.xp_h.min"),
            i18n.tr("zones.col.xp_h"),
            i18n.tr("zones.col.xp_h.max"),
            i18n.tr("zones.col.raw_h.min"),
            i18n.tr("zones.col.raw_h"),
            i18n.tr("zones.col.raw_h.max"),
            i18n.tr("zones.col.balance_h.min"),
            i18n.tr("zones.col.balance_h"),
            i18n.tr("zones.col.balance_h.max"),
        ])
        self.table.resizeColumnsToContents()

    # ---------------------------
    # API pública
    # ---------------------------
    def set_show_hi_lo(self, enabled: bool):
        self._show_hi_lo = enabled
        if enabled:
            self._set_headers_hilo()
        else:
            self._set_headers_basic()

    def set_rows(self, rows):
        self.table.setRowCount(0)
        if not rows:
            return

        # Mantener el estado de orden actual (columna/dirección)
        sort_enabled = self.table.isSortingEnabled()
        self.table.setSortingEnabled(False)

        self.table.setRowCount(len(rows))

        if not self._show_hi_lo:
            for r, row in enumerate(rows):
                self._set_item(r, 0, row.zona)  # Zona (texto)
                self._set_int(r, 1, row.hunts)
                self._set_hours(r, 2, row.hours_total)
                self._set_float0(r, 3, row.xp_gain_per_h)
                self._set_float0(r, 4, row.raw_xp_gain_per_h)
                self._set_float0(r, 5, row.balance_per_h)
        else:
            for r, row in enumerate(rows):
                self._set_item(r, 0, row.zona)  # Zona (texto)
                self._set_int(r, 1, row.hunts)
                self._set_hours(r, 2, row.hours_total)

                self._set_float0(r, 3, row.xp_gain_per_h_min)
                self._set_float0(r, 4, row.xp_gain_per_h)
                self._set_float0(r, 5, row.xp_gain_per_h_max)

                self._set_float0(r, 6, row.raw_xp_gain_per_h_min)
                self._set_float0(r, 7, row.raw_xp_gain_per_h)
                self._set_float0(r, 8, row.raw_xp_gain_per_h_max)

                self._set_float0(r, 9, row.balance_per_h_min)
                self._set_float0(r, 10, row.balance_per_h)
                self._set_float0(r, 11, row.balance_per_h_max)

        self.table.setSortingEnabled(sort_enabled)
        self.table.resizeColumnsToContents()

    def retranslate_ui(self):
        if self._show_hi_lo:
            self._set_headers_hilo()
        else:
            self._set_headers_basic()

    # ---------------------------
    # Helpers de formateo
    # ---------------------------
    @staticmethod
    def _fmt_number(val: float, decimals: int) -> str:
        s = f"{val:,.{decimals}f}"
        s = s.replace(",", "§").replace(".", ",").replace("§", ".")
        return s

    # --------- celdas (Zona = texto alineado izq.; resto = numérico centrado) ---------
    def _set_item(self, r, c, text: str):
        it = QTableWidgetItem(text or "")
        it.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Zona a la izquierda
        it.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table.setItem(r, c, it)

    def _set_int(self, r, c, val: int):
        num = int(val or 0)
        disp = self._fmt_number(num, 0)
        it = _NumericItem(disp, float(num))
        self.table.setItem(r, c, it)

    def _set_float0(self, r, c, val: float):
        num = float(val or 0.0)
        disp = self._fmt_number(round(num), 0)
        it = _NumericItem(disp, num)
        self.table.setItem(r, c, it)

    def _set_hours(self, r, c, val: float):
        num = float(val or 0.0)
        disp = self._fmt_number(num, 2)
        it = _NumericItem(disp, num)
        self.table.setItem(r, c, it)
