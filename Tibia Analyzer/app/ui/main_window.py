import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QLabel, QFileDialog, QHBoxLayout, QSplitter, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt

from app.services import config
from app.services import i18n
from app.services.library_sync import import_from_source
from app.data.loader import load_hunts_from_library
from app.services.pending_service import find_pending
from app.ui.pending_panel import PendingDialog
from app.ui.filters_panel import FiltersPanel
from app.ui.zones_table import ZonesTable
from app.services.aggregator import aggregate_by_zone
from app.services.paths import library_dir
from app.ui.profiles_dialog import ProfilesDialog

class MainWindow(QMainWindow):
    def __init__(self, cfg: dict):
        super().__init__()

        # idioma inicial
        self.config = cfg
        self.source_folder = cfg.get("source_folder", "")
        lang = cfg.get("language", "es")
        i18n.set_language(lang)

        self._default_voc = "Knight"
        self._default_mode = "Solo"

        self._build_ui()
        self.load_data()

    def _build_ui(self):
        self.setWindowTitle(i18n.tr("app.title"))
        # tamaño inicial gestionado por presets (ver _ensure_window_sizes_defaults / _apply_window_size_for_mode)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        # Barra superior
        top = QHBoxLayout()

        # Idioma
        self.lbl_language = QLabel(i18n.tr("language"))
        self.cb_language = QComboBox()
        self.cb_language.addItem(i18n.tr("language.es"), userData="es")
        self.cb_language.addItem(i18n.tr("language.en"), userData="en")
        self.cb_language.setCurrentIndex(0 if i18n.get_language() == "es" else 1)
        self.cb_language.currentIndexChanged.connect(self.on_language_changed)
        top.addWidget(self.lbl_language)
        top.addWidget(self.cb_language)

        # Origen + sincronizar (sin mostrar ruta de biblioteca)
        self.btn_choose_source = QPushButton(i18n.tr("source.choose"))
        self.btn_choose_source.clicked.connect(self.choose_source)
        top.addWidget(self.btn_choose_source)

        # Estado/contador en vez de ruta
        self.lbl_source = QLabel(self._source_status_text())
        self.lbl_source.setToolTip("Carpeta donde Tibia guarda los JSON de Hunt Analyzer")
        top.addWidget(self.lbl_source, 1)

        self.btn_sync = QPushButton(i18n.tr("sync.now"))
        self.btn_sync.setToolTip("Copia a la biblioteca interna los JSON nuevos desde la carpeta de Tibia")
        self.btn_sync.clicked.connect(self.sync_now)
        top.addWidget(self.btn_sync)

        # Ocultar biblioteca en la UI (se mantiene para no romper nada, pero invisible)
        self.lbl_library_title = QLabel(i18n.tr("library.label"))
        self.lbl_library_value = QLabel(f"{library_dir()}")
        top.addWidget(self.lbl_library_title)
        top.addWidget(self.lbl_library_value)
        self.lbl_library_title.setVisible(False)
        self.lbl_library_value.setVisible(False)

        self.lbl_pending = QLabel(i18n.tr("pending.count", n=0))
        top.addWidget(self.lbl_pending)

        self.btn_manage_pending = QPushButton(i18n.tr("pending.manage"))
        self.btn_manage_pending.clicked.connect(self.open_pending_dialog)
        top.addWidget(self.btn_manage_pending)

        # Botón de Perfiles
        self.btn_profiles = QPushButton(i18n.tr("profiles.open"))
        self.btn_profiles.clicked.connect(self.open_profiles_dialog)
        top.addWidget(self.btn_profiles)

        root.addLayout(top)

        # Filtros + tabla
        splitter = QSplitter(Qt.Horizontal)
        self.filters = FiltersPanel()
        splitter.addWidget(self.filters)

        self.table = ZonesTable()
        splitter.addWidget(self.table)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        root.addWidget(splitter, 1)

        # señales filtros
        # Vocación y Modo -> primero recalcular opciones dependientes, luego refrescar tabla
        self.filters.cb_vocation.currentTextChanged.connect(self.on_filters_changed)
        self.filters.cb_mode.currentTextChanged.connect(self.on_filters_changed)
        # Level solo refresca tabla
        self.filters.cb_level.currentTextChanged.connect(self.refresh_table)
        self.filters.chk_hilo.toggled.connect(self.on_hi_lo_toggled)

        # ---- Presets de tamaño por modo (inicialización + aplicar) ----
        self._ensure_window_sizes_defaults()
        self._apply_window_size_for_mode(self.filters.show_hi_lo())

    # Idioma
    def on_language_changed(self):
        lang = self.cb_language.currentData() or "es"
        i18n.set_language(lang)
        self.config["language"] = lang
        config.save_config(self.config)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(i18n.tr("app.title"))
        self.lbl_language.setText(i18n.tr("language"))

        self.cb_language.blockSignals(True)
        cur = i18n.get_language()
        self.cb_language.clear()
        self.cb_language.addItem(i18n.tr("language.es"), userData="es")
        self.cb_language.addItem(i18n.tr("language.en"), userData="en")
        self.cb_language.setCurrentIndex(0 if cur == "es" else 1)
        self.cb_language.blockSignals(False)

        self.btn_choose_source.setText(i18n.tr("source.choose"))
        self.lbl_source.setText(self._source_status_text())
        self.btn_sync.setText(i18n.tr("sync.now"))

        self.lbl_library_title.setText(i18n.tr("library.label"))
        self.btn_manage_pending.setText(i18n.tr("pending.manage"))
        self.btn_profiles.setText(i18n.tr("profiles.open"))
        self.lbl_pending.setText(i18n.tr("pending.count", n=len(find_pending(self.hunts)) if hasattr(self, "hunts") else 0))

        self.filters.retranslate_ui()
        self.table.retranslate_ui()

        # Recalcular opciones inteligentes
        self._refresh_mode_options()
        self._refresh_level_options()
        self.refresh_table()

    # Sincronización
    def choose_source(self):
        folder = QFileDialog.getExistingDirectory(self, i18n.tr("source.choose"))
        if folder:
            self.source_folder = folder
            self.lbl_source.setText(self._source_status_text())
            self.config["source_folder"] = folder
            config.save_config(self.config)
            self.sync_now()

    def sync_now(self):
        if not self.source_folder:
            QMessageBox.information(self, i18n.tr("sync.now"), i18n.tr("sync.msg.need_source"))
            return
        copied, ignored = import_from_source(self.source_folder)
        msg = i18n.tr("sync.msg.result", copied=copied)
        if ignored:
            msg += i18n.tr("sync.msg.duplicates", ignored=ignored)
        QMessageBox.information(self, i18n.tr("sync.now"), msg)
        self.lbl_source.setText(self._source_status_text())
        self.load_data()

    # Carga / pendientes / filtros
    def load_data(self):
        self.hunts = load_hunts_from_library()
        pend = find_pending(self.hunts)
        self.lbl_pending.setText(i18n.tr("pending.count", n=len(pend)))

        vocs  = sorted({h.vocation for h in self.hunts if h.has_all_meta and h.vocation})
        modes = sorted({h.mode for h in self.hunts if h.has_all_meta and h.mode})
        lvls  = sorted({h.level_bucket for h in self.hunts if h.has_all_meta and h.level_bucket})

        if not vocs:  vocs = ["Knight"]
        if not modes: modes = ["Solo"]

        self.filters.set_available_vocations(vocs, default=self._default_voc)
        self.filters.set_available_modes(modes, default=self._default_mode)
        self.filters.set_available_levels(lvls)

        # Ajustes inteligentes iniciales
        self._refresh_mode_options()
        self._refresh_level_options()

        self.refresh_table()

    def open_pending_dialog(self):
        pend = find_pending(self.hunts)
        if not pend:
            QMessageBox.information(self, i18n.tr("pending.manage"), i18n.tr("pending.none"))
            return
        existing_zones = sorted({h.zona for h in self.hunts if h.zona})
        dlg = PendingDialog(self, pend, existing_zones)
        if dlg.exec():
            self.load_data()

    def open_profiles_dialog(self):
        dlg = ProfilesDialog(self)
        dlg.exec()

    def on_hi_lo_toggled(self, checked: bool):
        # Guardar tamaño del modo anterior antes de cambiar
        prev_mode_is_hilo = not checked
        self._save_current_window_size_for_mode(prev_mode_is_hilo)

        # Cambiar tabla y refrescar
        self.table.set_show_hi_lo(checked)
        self.refresh_table()

        # Aplicar tamaño del modo nuevo
        self._apply_window_size_for_mode(checked)

    def on_filters_changed(self):
        # Recalcular modos (por vocación) y niveles (por vocación+modo)
        self._refresh_mode_options()
        self._refresh_level_options()
        self.refresh_table()

    def refresh_table(self):
        if not hasattr(self, "hunts") or not self.hunts:
            self.table.set_rows([])
            return
        self.table.set_show_hi_lo(self.filters.show_hi_lo())
        voc = self.filters.current_vocation()
        mode = self.filters.current_mode()
        level = self.filters.current_level()
        rows = aggregate_by_zone(self.hunts, vocation=voc, mode=mode, level_filter=level)
        self.table.set_rows(rows)

    # -----------------------
    # Helpers: filtros inteligentes + estado origen
    # -----------------------
    def _source_status_text(self) -> str:
        folder = self.source_folder
        if not folder or not os.path.isdir(folder):
            return "Carpeta no seleccionada"
        # Contador NO recursivo para que coincida con import_from_source()
        return f"JSON encontrados: {self._count_json_recursive(folder)}"

    @staticmethod
    def _count_json_recursive(folder: str) -> int:
        """
        Cuenta SOLO los .json directamente dentro de 'folder' (NO recursivo),
        para que el contador refleje exactamente lo que importará import_from_source().
        """
        if not folder or not os.path.isdir(folder):
            return 0
        try:
            return sum(
                1
                for entry in os.scandir(folder)
                if entry.is_file() and entry.name.lower().endswith(".json")
            )
        except Exception:
            return 0

    def _refresh_level_options(self):
        if not hasattr(self, "hunts") or not self.hunts:
            self.filters.set_available_levels([])
            return

        sel_voc = self.filters.current_vocation()
        sel_mode = self.filters.current_mode()

        def matches(h):
            if not h.has_all_meta:
                return False
            if sel_voc and sel_voc != "All" and h.vocation != sel_voc:
                return False
            if sel_mode and sel_mode != "All" and h.mode != sel_mode:
                return False
            return bool(h.level_bucket)

        levels = sorted({h.level_bucket for h in self.hunts if matches(h)})
        self.filters.set_available_levels(levels)

    def _refresh_mode_options(self):
        if not hasattr(self, "hunts") or not self.hunts:
            self.filters.set_available_modes([])
            return

        sel_voc = self.filters.current_vocation()

        def matches(h):
            if not h.has_all_meta:
                return False
            if sel_voc and sel_voc != "All" and h.vocation != sel_voc:
                return False
            return bool(h.mode)

        modes = sorted({h.mode for h in self.hunts if matches(h)})
        self.filters.set_available_modes(modes)

    # -----------------------
    # Helpers: tamaños por modo + persistencia
    # -----------------------
    def _ensure_window_sizes_defaults(self):
        """
        Estructura en config:
        self.config["window_sizes"] = {
            "basic": [1120, 720],
            "hilo":  [1320, 760]
        }
        """
        ws = self.config.get("window_sizes")
        if not isinstance(ws, dict):
            ws = {}
        if "basic" not in ws or not self._valid_size(ws.get("basic")):
            ws["basic"] = [1120, 720]
        if "hilo" not in ws or not self._valid_size(ws.get("hilo")):
            ws["hilo"] = [1320, 760]
        self.config["window_sizes"] = ws
        config.save_config(self.config)

    @staticmethod
    def _valid_size(val):
        try:
            return isinstance(val, (list, tuple)) and len(val) == 2 and int(val[0]) > 0 and int(val[1]) > 0
        except Exception:
            return False

    def _apply_window_size_for_mode(self, hilo: bool):
        ws = self.config.get("window_sizes", {})
        key = "hilo" if hilo else "basic"
        size = ws.get(key, [1120, 720] if not hilo else [1320, 760])
        try:
            w, h = int(size[0]), int(size[1])
        except Exception:
            w, h = (1320, 760) if hilo else (1120, 720)
        self.resize(w, h)

    def _save_current_window_size_for_mode(self, hilo: bool):
        ws = self.config.get("window_sizes") or {}
        key = "hilo" if hilo else "basic"
        ws[key] = [self.width(), self.height()]
        self.config["window_sizes"] = ws
        config.save_config(self.config)

    # Guardar al cerrar
    def closeEvent(self, event):
        # Guarda el tamaño del modo actual
        self._save_current_window_size_for_mode(self.filters.show_hi_lo())
        super().closeEvent(event)
