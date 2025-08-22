import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QLabel, QHBoxLayout, QSplitter, QMessageBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from app.services.paths import asset_path, library_dir
from app.services import config, i18n
from app.services import ui_prefs
from app.services.library_sync import import_from_source
from app.data.loader import load_hunts_from_library
from app.services.pending_service import find_pending
from app.ui.pending_panel import PendingDialog
from app.ui.filters_panel import FiltersPanel
from app.ui.zones_table import ZonesTable
from app.services.aggregator import aggregate_by_zone
from app.ui.profiles_dialog import ProfilesDialog
from app.ui.settings_panel import SettingsDialog
from app.ui.tools_panel import ToolsDialog


class MainWindow(ui_prefs.PersistentSizeMixin, QMainWindow):
    def __init__(self, cfg: dict):
        super().__init__()

        # idioma inicial
        self.config = cfg
        self.source_folder = cfg.get("source_folder", "")
        lang = cfg.get("language", "es")
        i18n.set_language(lang)

        self._default_voc = "Knight"
        self._default_mode = "Solo"

        # Inicializa el mixin (tamaño general recordado)
        self.init_persistent_size(self.config, key="main_window_last", default=(1120, 720))

        self._build_ui()
        self.load_data()

        # cargar tamaño según modo (basic / hilo)
        hilo = self.filters.show_hi_lo()
        if hilo:
            ui_prefs.load_size(self, "main_window_hilo", default=(1320, 760))
        else:
            ui_prefs.load_size(self, "main_window_basic", default=(1120, 720))

    def _build_ui(self):
        self.setWindowTitle(i18n.tr("app.title"))

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        # Barra superior
        top = QHBoxLayout()

        # --- Botón Ajustes ---
        self.btn_settings = QPushButton()
        gear_png = asset_path("assets", "icons", "settings_gear.png")
        icon_fallback = asset_path("assets", "icons", "icon.ico")
        if gear_png.exists():
            self.btn_settings.setIcon(QIcon(str(gear_png)))
        elif icon_fallback.exists():
            self.btn_settings.setIcon(QIcon(str(icon_fallback)))

        self.btn_settings.setIconSize(QSize(22, 22))
        self.btn_settings.setFixedSize(34, 34)
        self.btn_settings.setToolTip(i18n.tr("settings.title"))
        self.btn_settings.setCursor(Qt.PointingHandCursor)
        self.btn_settings.setStyleSheet(self._square_btn_css())
        self.btn_settings.clicked.connect(self.open_settings_dialog)
        top.addWidget(self.btn_settings)

        # --- Botón Herramientas ---
        self.btn_tools = QPushButton()
        tools_png = asset_path("assets", "icons", "tools_panel.png")
        if tools_png.exists():
            self.btn_tools.setIcon(QIcon(str(tools_png)))
        elif icon_fallback.exists():
            self.btn_tools.setIcon(QIcon(str(icon_fallback)))
        self.btn_tools.setIconSize(QSize(22, 22))
        self.btn_tools.setFixedSize(34, 34)
        self.btn_tools.setToolTip(i18n.tr("tools.title"))
        self.btn_tools.setCursor(Qt.PointingHandCursor)
        self.btn_tools.setStyleSheet(self._square_btn_css())
        self.btn_tools.clicked.connect(self.open_tools_dialog)
        top.addWidget(self.btn_tools)

        # --- Botón Sincronizar ---
        self.btn_sync = QPushButton()
        sync_png = asset_path("assets", "icons", "sync_now.png")
        if sync_png.exists():
            self.btn_sync.setIcon(QIcon(str(sync_png)))
        elif icon_fallback.exists():
            self.btn_sync.setIcon(QIcon(str(icon_fallback)))
        self.btn_sync.setIconSize(QSize(22, 22))
        self.btn_sync.setFixedSize(34, 34)
        self.btn_sync.setToolTip(i18n.tr("sync.now"))
        self.btn_sync.setCursor(Qt.PointingHandCursor)
        self.btn_sync.setStyleSheet(self._square_btn_css())
        self.btn_sync.clicked.connect(self.sync_now)
        top.addWidget(self.btn_sync)

        # Ocultar biblioteca
        self.lbl_library_title = QLabel(i18n.tr("library.label"))
        self.lbl_library_value = QLabel(f"{library_dir()}")
        self.lbl_library_title.setVisible(False)
        self.lbl_library_value.setVisible(False)
        top.addWidget(self.lbl_library_title)
        top.addWidget(self.lbl_library_value)

        # Botón pendientes con contador
        self.btn_manage_pending = QPushButton(i18n.tr("pending.manage_with_count", n=0))
        self.btn_manage_pending.clicked.connect(self.open_pending_dialog)
        top.addWidget(self.btn_manage_pending)

        # Botón perfiles
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
        self.filters.cb_vocation.currentTextChanged.connect(self.on_filters_changed)
        self.filters.cb_mode.currentTextChanged.connect(self.on_filters_changed)
        self.filters.cb_level.currentTextChanged.connect(self.refresh_table)
        self.filters.chk_hilo.toggled.connect(self.on_hi_lo_toggled)

    # ---- Ajustes / Tools / Sync ----
    def open_settings_dialog(self):
        dlg = SettingsDialog(
            self,
            cfg=self.config,
            on_sync_done=self.load_data,
            on_language_changed=self.retranslate_ui,
        )
        dlg.exec()

    def open_tools_dialog(self):
        dlg = ToolsDialog(self, self.config)
        dlg.exec()

    def sync_now(self):
        if not self.source_folder:
            QMessageBox.information(self, i18n.tr("sync.now"), i18n.tr("sync.msg.need_source"))
            return
        copied, ignored = import_from_source(self.source_folder)
        msg = i18n.tr("sync.msg.result", copied=copied)
        if ignored:
            msg += i18n.tr("sync.msg.duplicates", ignored=ignored)
        QMessageBox.information(self, i18n.tr("sync.now"), msg)
        self.load_data()

    # ---- Carga / pendientes / filtros ----
    def load_data(self):
        self.hunts = load_hunts_from_library()
        pend = find_pending(self.hunts)
        self.btn_manage_pending.setText(i18n.tr("pending.manage_with_count", n=len(pend)))

        vocs = sorted({h.vocation for h in self.hunts if h.has_all_meta and h.vocation})
        modes = sorted({h.mode for h in self.hunts if h.has_all_meta and h.mode})
        lvls = sorted({h.level_bucket for h in self.hunts if h.has_all_meta and h.level_bucket})

        if not vocs:
            vocs = ["Knight"]
        if not modes:
            modes = ["Solo"]

        self.filters.set_available_vocations(vocs, default=self._default_voc)
        self.filters.set_available_modes(modes, default=self._default_mode)
        self.filters.set_available_levels(lvls)

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
        # guarda tamaño anterior del modo que dejamos
        ui_prefs.save_size(self, "main_window_hilo" if not checked else "main_window_basic")
        # aplica tamaño del modo activo
        if checked:
            ui_prefs.load_size(self, "main_window_hilo", default=(1320, 760))
        else:
            ui_prefs.load_size(self, "main_window_basic", default=(1120, 720))

        self.table.set_show_hi_lo(checked)
        self.refresh_table()

    def on_filters_changed(self):
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

    def retranslate_ui(self):
        self.setWindowTitle(i18n.tr("app.title"))

        # Tooltips
        self.btn_settings.setToolTip(i18n.tr("settings.title"))
        self.btn_sync.setToolTip(i18n.tr("sync.now"))

        # Botón "Gestionar pendientes: X"
        count = len(find_pending(self.hunts)) if hasattr(self, "hunts") else 0
        self.btn_manage_pending.setText(f"{i18n.tr('pending.manage')}: {count}")

        # Perfiles
        self.btn_profiles.setText(i18n.tr("profiles.open"))

        # Retraducir sub-UIs
        if hasattr(self, "filters"):
            self.filters.retranslate_ui()
        if hasattr(self, "table"):
            self.table.retranslate_ui()

        self.refresh_table()

    # ---- Guardar tamaño al cerrar ----
    def closeEvent(self, event):
        # Guardamos el tamaño del modo actual (basic/hilo)
        ui_prefs.save_size(self, "main_window_hilo" if self.filters.show_hi_lo() else "main_window_basic")
        # Dejamos que el mixin persista también su clave 'main_window_last'
        super().closeEvent(event)

    # ---- Helpers ----
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

    @staticmethod
    def _square_btn_css() -> str:
        return """
            QPushButton {
                border: 1px solid #3a3a3a;
                border-radius: 6px;
                background-color: #242424;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #2e2e2e;
                border-color: #565656;
            }
            QPushButton:pressed {
                background-color: #1e1e1e;
                border-color: #6a6a6a;
            }
        """
