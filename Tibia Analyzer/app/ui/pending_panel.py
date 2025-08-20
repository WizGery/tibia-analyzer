from __future__ import annotations

import os
import json
import re
from functools import partial
from typing import List, Dict, Optional

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QComboBox,
    QPushButton, QHBoxLayout, QMessageBox, QLabel, QPlainTextEdit, QAbstractItemView,
    QCheckBox
)
from PySide6.QtCore import Qt, Slot

from app.services.pending_service import (
    ALLOWED_VOCS, ALLOWED_MODES, ALLOWED_LEVELS
)
from app.data.writer import write_meta_to_json
from app.services import profiles as profiles_service
from app.services import i18n
from app.services import config  # para persistir tamaño del diálogo


# ---------- helpers de centrado ----------
def _center_widget(w: QWidget) -> QWidget:
    box = QWidget()
    lay = QHBoxLayout(box)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.addStretch(1)
    lay.addWidget(w)
    lay.addStretch(1)
    return box

def _extract_centered_child(cell: QWidget) -> Optional[QWidget]:
    """Devuelve el widget centrado dentro del contenedor si existe."""
    if not isinstance(cell, QWidget) or cell.layout() is None:
        return None
    lay = cell.layout()
    if lay.count() >= 3 and lay.itemAt(1) and lay.itemAt(1).widget():
        return lay.itemAt(1).widget()
    return None


# ------------------------- Diálogo: lista completa de Monsters -------------------------
class MonstersDialog(QDialog):
    def __init__(self, parent: QWidget | None, json_path: str):
        super().__init__(parent)
        self.setWindowTitle(i18n.tr("monsters.title"))
        self.resize(520, 540)

        layout = QVBoxLayout(self)
        title = QLabel(os.path.basename(json_path))
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title)

        from PySide6.QtWidgets import QTableWidget
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels([i18n.tr("monsters.col.name"), i18n.tr("monsters.col.count")])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        btn_close = QPushButton(i18n.tr("monsters.btn.close"))
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            QMessageBox.warning(self, i18n.tr("monsters.title"), i18n.tr("monsters.msg.read_error", err=str(e)))
            return

        monsters = data.get("Killed Monsters") or []
        try:
            monsters = sorted(monsters, key=lambda m: int(m.get("Count", 0)), reverse=True)
        except Exception:
            pass

        for m in monsters:
            name = str(m.get("Name", "")).strip()
            count = str(m.get("Count", ""))
            row = self.table.rowCount()
            self.table.insertRow(row)
            it_name = QTableWidgetItem(name)
            it_cnt = QTableWidgetItem(count)
            it_cnt.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 0, it_name)
            self.table.setItem(row, 1, it_cnt)


# ------------------------- Diálogo: cálculo de Balance (Duo) -------------------------
class DuoBalanceDialog(QDialog):
    def __init__(self, parent: QWidget | None, json_path: str):
        super().__init__(parent)
        self.setWindowTitle(i18n.tr("pending.calc_balance"))
        self.resize(600, 460)
        self.json_path = json_path

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Pega aquí el texto de Party Hunt (bloque) o el mensaje de Transfer:"))
        self.edit = QPlainTextEdit()
        layout.addWidget(self.edit)

        btns = QHBoxLayout()
        self.btn_calc = QPushButton(i18n.tr("pending.calc_balance"))
        self.btn_cancel = QPushButton(i18n.tr("pending.close"))
        btns.addStretch(1)
        btns.addWidget(self.btn_calc)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)

        self.btn_calc.clicked.connect(self.on_calc)
        self.btn_cancel.clicked.connect(self.reject)

        self.result_value: int | None = None

    def _parse_int(self, s: str) -> int:
        return int(re.sub(r"[^\d-]", "", s or "0") or "0")

    def _parse_party(self, text: str) -> int | None:
        m_total = re.search(r"Balance:\s*([\d.,-]+)", text)
        if not m_total:
            return None
        total = self._parse_int(m_total.group(1))
        players = re.findall(r"^\s*([^\n]+)\r?\n\s+Loot:", text, flags=re.MULTILINE)
        count = len(players) if players else 0
        if count <= 0:
            count = 2
        per_head = round(total / count) if count > 0 else total
        return int(per_head)

    def _parse_transfer(self, text: str) -> int | None:
        m = re.search(r"Transfer\s+([\d.,-]+)\s+to\s+.+", text, flags=re.IGNORECASE)
        if not m:
            return None
        amount = self._parse_int(m.group(1))
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            bal_json = self._parse_int(str(data.get("Balance", 0)))
        except Exception:
            bal_json = 0
        return int(bal_json - amount)

    def on_calc(self):
        text = self.edit.toPlainText().strip()
        if not text:
            QMessageBox.information(self, i18n.tr("pending.calc_balance"), i18n.tr("pending.msg.calc.paste"))
            return
        val = self._parse_party(text)
        if val is None:
            val = self._parse_transfer(text)
        if val is None:
            QMessageBox.warning(self, i18n.tr("pending.calc_balance"), i18n.tr("pending.msg.calc.not_detected"))
            return
        self.result_value = val
        pretty = f"{val:,}".replace(",", ".")
        QMessageBox.information(self, i18n.tr("pending.msg.calc.result.title"),
                                i18n.tr("pending.msg.calc.result.body", val=pretty))
        self.accept()


# ------------------------- Panel de pendientes -------------------------
COLS_KEYS = [
    "pending.col.file", "pending.col.vocation", "pending.col.mode", "pending.col.vocation_duo",
    "pending.col.zone", "pending.col.level", "pending.col.balance_real",
    "pending.col.ignore_duo", "pending.col.issues"
]

class PendingDialog(QDialog):
    def __init__(self, parent: QWidget | None, pending_rows: List[Dict], existing_zones: List[str]):
        super().__init__(parent)
        self.setWindowTitle(i18n.tr("pending.title"))

        # ---- Restaurar tamaño guardado (persistencia real) ----
        cfg = config.load_config() if hasattr(config, "load_config") else {}
        ws = cfg.get("window_sizes", {})
        sz = ws.get("pending")
        if self._valid_size(sz):
            self.resize(int(sz[0]), int(sz[1]))
        else:
            self.resize(1160, 640)  # por defecto

        self.pending_rows = pending_rows
        self.existing_zones = sorted({z for z in existing_zones if z})

        layout = QVBoxLayout(self)

        info = QLabel(i18n.tr("pending.info"))
        layout.addWidget(info)

        # Selector de perfil y acciones
        profiles_row = QHBoxLayout()
        profiles_row.addWidget(QLabel(i18n.tr("pending.profile")))
        self.cb_profiles = QComboBox()
        self.cb_profiles.addItem("")
        for p in profiles_service.list_profiles():
            self.cb_profiles.addItem(p.get("name", ""))
        profiles_row.addWidget(self.cb_profiles)

        self.btn_apply_profile = QPushButton(i18n.tr("pending.load_profile_all"))
        self.btn_apply_profile.clicked.connect(self.apply_profile_to_all)
        profiles_row.addWidget(self.btn_apply_profile)

        self.btn_view_monsters = QPushButton(i18n.tr("pending.view_monsters"))
        self.btn_view_monsters.clicked.connect(self.on_view_monsters)
        profiles_row.addWidget(self.btn_view_monsters)

        self.btn_calc_balance = QPushButton(i18n.tr("pending.calc_balance"))
        self.btn_calc_balance.clicked.connect(self.calc_balance_for_selected)
        profiles_row.addWidget(self.btn_calc_balance)

        profiles_row.addStretch(1)
        layout.addLayout(profiles_row)

        # Tabla
        self.table = QTableWidget(len(pending_rows), len(COLS_KEYS))
        self._set_headers()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.doubleClicked.connect(self.on_view_monsters)
        layout.addWidget(self.table)

        for r, row in enumerate(pending_rows):
            full_path = row["path"]
            filename = os.path.basename(full_path)

            # Archivo: izquierda
            it_file = QTableWidgetItem(filename)
            it_file.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            it_file.setData(Qt.UserRole, full_path)
            it_file.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(r, 0, it_file)

            # Vocación — centrado
            cb_voc = QComboBox(); cb_voc.addItem("")
            for v in ALLOWED_VOCS: cb_voc.addItem(v)
            cb_voc.setCurrentText(row.get("vocation", ""))
            cb_voc.currentTextChanged.connect(lambda _t, rr=r: self._on_vocation_changed(rr))
            self.table.setCellWidget(r, 1, _center_widget(cb_voc))

            # Modo — centrado
            cb_mode = QComboBox(); cb_mode.addItem("")
            for m in ALLOWED_MODES: cb_mode.addItem(m)
            cb_mode.setCurrentText(row.get("mode", ""))
            cb_mode.currentTextChanged.connect(lambda _t, rr=r: self._on_mode_changed(rr))
            self.table.setCellWidget(r, 2, _center_widget(cb_mode))

            # Vocación Duo — centrado (se llena según _refresh_duo_choices)
            cb_duo = QComboBox()
            self.table.setCellWidget(r, 3, _center_widget(cb_duo))

            # Zona — centrado (editable)
            cb_zona = QComboBox(); cb_zona.setEditable(True)
            cb_zona.addItem("")
            for z in self.existing_zones: cb_zona.addItem(z)
            cb_zona.setCurrentText(row.get("zona", ""))
            self.table.setCellWidget(r, 4, _center_widget(cb_zona))

            # Level — centrado (combo)
            cb_level = QComboBox()
            cb_level.addItem("")
            for lv in ALLOWED_LEVELS: cb_level.addItem(lv)
            cb_level.setCurrentText(row.get("level", ""))
            cb_level.setEditable(False)
            self.table.setCellWidget(r, 5, _center_widget(cb_level))

            # Balance Real — centrado
            bal_real_txt, bal_real_raw = self._read_balance_real(full_path)
            it_bal_real = QTableWidgetItem(bal_real_txt)
            it_bal_real.setTextAlignment(Qt.AlignCenter)
            it_bal_real.setData(Qt.UserRole, bal_real_raw)
            self.table.setItem(r, 6, it_bal_real)

            # Ignorar Balance (Duo) — checkbox centrado
            chk_ignore = QCheckBox()
            ignore_default = self._read_ignore_flag(full_path)
            chk_ignore.setChecked(ignore_default)
            mode_now = row.get("mode", "")
            chk_ignore.setEnabled(mode_now == "Duo" and bal_real_raw is None)
            self.table.setCellWidget(r, 7, _center_widget(chk_ignore))

            # Problemas: izquierda
            it_issues = QTableWidgetItem("; ".join(row.get("issues", [])))
            it_issues.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            it_issues.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(r, 8, it_issues)

            self._refresh_duo_choices(r, preset_value=row.get("vocation_duo", ""))

        # Botonera inferior
        btn_row = QHBoxLayout()
        self.btn_save = QPushButton(i18n.tr("pending.save"))
        self.btn_save.clicked.connect(self.save_all)
        self.btn_close = QPushButton(i18n.tr("pending.close"))
        self.btn_close.clicked.connect(self.reject)

        btn_row.addStretch(1)
        btn_row.addWidget(self.btn_save)
        btn_row.addWidget(self.btn_close)
        layout.addLayout(btn_row)

    # Headers traducibles
    def _set_headers(self):
        self.table.setHorizontalHeaderLabels([i18n.tr(k) for k in COLS_KEYS])

    # Helpers: obtener el widget interior centrado
    def _w_voc(self, row: int) -> QComboBox:
        return _extract_centered_child(self.table.cellWidget(row, 1))  # type: ignore

    def _w_mode(self, row: int) -> QComboBox:
        return _extract_centered_child(self.table.cellWidget(row, 2))  # type: ignore

    def _w_duo(self, row: int) -> QComboBox:
        return _extract_centered_child(self.table.cellWidget(row, 3))  # type: ignore

    def _w_zona(self, row: int) -> QComboBox:
        return _extract_centered_child(self.table.cellWidget(row, 4))  # type: ignore

    def _w_level(self, row: int) -> QComboBox:
        return _extract_centered_child(self.table.cellWidget(row, 5))  # type: ignore

    def _w_ignore(self, row: int) -> QCheckBox:
        return _extract_centered_child(self.table.cellWidget(row, 7))  # type: ignore

    def _read_balance_real(self, path: str) -> tuple[str, int | None]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                d = json.load(f)
            if "Balance Real" in d and str(d.get("Balance Real", "")).strip() != "":
                val = int(re.sub(r"[^\d-]", "", str(d["Balance Real"])))
                return f"{val:,}".replace(",", "."), val
        except Exception:
            pass
        return "", None

    def _read_ignore_flag(self, path: str) -> bool:
        try:
            with open(path, "r", encoding="utf-8") as f:
                d = json.load(f)
            raw = str(d.get("Ignore Duo Balance", "")).strip().lower()
            return raw in ("1", "true", "yes", "y", "on")
        except Exception:
            return False

    def _refresh_duo_choices(self, row_index: int, preset_value: str | None = None):
        cb_mode = self._w_mode(row_index)
        cb_voc = self._w_voc(row_index)
        cb_duo = self._w_duo(row_index)
        if not (cb_mode and cb_voc and cb_duo):
            return
        mode = cb_mode.currentText().strip()
        vocation = cb_voc.currentText().strip()

        cb_duo.blockSignals(True)
        cb_duo.clear()
        if mode == "Solo":
            cb_duo.addItem("none")
            cb_duo.setCurrentText("none")
            cb_duo.setEnabled(False)
        else:
            options = [v for v in ALLOWED_VOCS if v != vocation]
            for v in options:
                cb_duo.addItem(v)
            if preset_value and preset_value in options:
                cb_duo.setCurrentText(preset_value)
            else:
                cb_duo.setCurrentIndex(-1)
            cb_duo.setEnabled(True)
        cb_duo.blockSignals(False)
        
    def accept(self):
        # Guardar tamaño también cuando se cierra con "Guardar cambios"
        try:
            self._save_pending_size()
        finally:
            super().accept()

    def reject(self):
        # Guardar tamaño también cuando se cierra con "Cerrar"
        try:
            self._save_pending_size()
        finally:
            super().reject()


    @Slot()
    def _on_mode_changed(self, row_index: int):
        current_duo = self._w_duo(row_index).currentText().strip()
        self._refresh_duo_choices(row_index, preset_value=current_duo)

        cb_mode = self._w_mode(row_index)
        bal_item = self.table.item(row_index, 6)
        has_bal_real = (bal_item and bal_item.data(Qt.UserRole) is not None)
        if cb_mode:
            self._w_ignore(row_index).setEnabled(cb_mode.currentText().strip() == "Duo" and not has_bal_real)

    @Slot()
    def _on_vocation_changed(self, row_index: int):
        current_duo = self._w_duo(row_index).currentText().strip()
        self._refresh_duo_choices(row_index, preset_value=current_duo)

    # Acciones
    @Slot()
    def on_view_monsters(self):
        sel = self.table.currentRow()
        if sel < 0:
            QMessageBox.information(self, i18n.tr("pending.title"), i18n.tr("pending.msg.select_row"))
            return
        path_item = self.table.item(sel, 0)
        full_path = path_item.data(Qt.UserRole)
        if not full_path:
            QMessageBox.warning(self, i18n.tr("pending.title"), "No path")
            return
        dlg = MonstersDialog(self, full_path)
        dlg.exec()

    def calc_balance_for_selected(self):
        r = self.table.currentRow()
        if r < 0:
            QMessageBox.information(self, i18n.tr("pending.calc_balance"), i18n.tr("pending.msg.select_row"))
            return
        if self._w_mode(r).currentText().strip() != "Duo":
            QMessageBox.information(self, i18n.tr("pending.calc_balance"), i18n.tr("pending.msg.not_duo"))
            return

        path_item = self.table.item(r, 0)
        full_path = path_item.data(Qt.UserRole)
        dlg = DuoBalanceDialog(self, full_path)
        if dlg.exec():
            val = dlg.result_value
            it: QTableWidgetItem = self.table.item(r, 6)
            it.setText(f"{val:,}".replace(",", "."))
            it.setData(Qt.UserRole, int(val))
            self._w_ignore(r).setChecked(False)
            self._w_ignore(r).setEnabled(False)

    def apply_profile_to_all(self):
        name = self.cb_profiles.currentText().strip()
        if not name:
            QMessageBox.information(self, i18n.tr("profiles.title"), i18n.tr("pending.msg.profile_select"))
            return
        p = profiles_service.get_profile(name)
        if not p:
            QMessageBox.warning(self, i18n.tr("profiles.title"), i18n.tr("pending.msg.profile_not_found"))
            return

        voc = p.get("vocation", "")
        lvl = p.get("level", "")
        ok = QMessageBox.question(
            self,
            i18n.tr("pending.msg.profile.apply.title"),
            i18n.tr("pending.msg.profile.apply.body", voc=voc, lvl=lvl),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if ok != QMessageBox.Yes:
            return

        for r in range(self.table.rowCount()):
            cb_voc: QComboBox = self._w_voc(r)
            cb_duo: QComboBox = self._w_duo(r)
            cb_lvl: QComboBox = self._w_level(r)
            cb_voc.setCurrentText(voc)
            self._refresh_duo_choices(r, preset_value=cb_duo.currentText().strip())
            cb_lvl.setCurrentText(lvl)

    # Guardado
    def _row_updates(self, r: int) -> Dict[str, str]:
        cb_voc  = self._w_voc(r)
        cb_mode = self._w_mode(r)
        cb_duo  = self._w_duo(r)
        cb_zona = self._w_zona(r)
        cb_lvl  = self._w_level(r)
        bal_item: QTableWidgetItem = self.table.item(r, 6)
        ignore_chk: QCheckBox = self._w_ignore(r)

        updates: Dict[str, str] = {
            "Vocation": cb_voc.currentText().strip() if cb_voc else "",
            "Mode": cb_mode.currentText().strip() if cb_mode else "",
            "Vocation duo": cb_duo.currentText().strip() if cb_duo else "",
            "Zona": cb_zona.currentText().strip() if cb_zona else "",
            "Level": cb_lvl.currentText().strip() if cb_lvl else "",
            "Ignore Duo Balance": "true" if (ignore_chk and ignore_chk.isChecked()) else "false",
        }
        bal_user = bal_item.data(Qt.UserRole) if bal_item else None
        if bal_user is not None:
            updates["Balance Real"] = str(int(bal_user))
        if updates.get("Mode") == "Solo":
            updates["Vocation duo"] = "none"
        return updates

    def save_all(self):
        ok_count = 0
        fail: List[str] = []
        for r in range(self.table.rowCount()):
            path_item = self.table.item(r, 0)
            full_path = (path_item.data(Qt.UserRole) or path_item.text()) if path_item else ""
            if write_meta_to_json(full_path, self._row_updates(r)):
                ok_count += 1
            else:
                fail.append(os.path.basename(full_path) if full_path else f"row{r+1}")

        if fail:
            QMessageBox.warning(
                self, i18n.tr("pending.save"),
                i18n.tr("pending.msg.saved_partial", ok=ok_count, names="\n".join(fail))
            )
        else:
            QMessageBox.information(self, i18n.tr("pending.save"), i18n.tr("pending.msg.saved_ok", n=ok_count))
        self.accept()

    # -------- persistencia tamaño del diálogo --------
    @staticmethod
    def _valid_size(v) -> bool:
        try:
            return isinstance(v, (list, tuple)) and len(v) == 2 and int(v[0]) > 0 and int(v[1]) > 0
        except Exception:
            return False

    def _save_pending_size(self):
        """Guarda el tamaño actual en config['window_sizes']['pending']."""
        try:
            cfg = config.load_config() if hasattr(config, "load_config") else {}
            ws = cfg.get("window_sizes", {})
            ws["pending"] = [self.width(), self.height()]
            cfg["window_sizes"] = ws
            config.save_config(cfg)
        except Exception:
            pass

    def closeEvent(self, event):
        # Guardar el tamaño siempre que se cierre el diálogo (Guardar, Cerrar o X)
        self._save_pending_size()
        super().closeEvent(event)
