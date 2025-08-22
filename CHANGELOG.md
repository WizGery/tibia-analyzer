# 📜 Changelog

---

## [v0.3.7.5] — 2025-08-22
### [ES]
### Cambiado
- **pending_panel**: unificación a **PySide6** (eliminada importación de PyQt5).
- **Diálogos con tamaño persistente**: ahora `MonstersDialog` y `DuoBalanceDialog` usan `PersistentSizeMixin` (keys: `monsters_dialog`, `duo_balance_dialog`).
- **MonstersDialog**: columnas autoajustadas al contenido (`QHeaderView.ResizeToContents`) y sin word-wrap en cabeceras/filas.
- **Confirmaciones localizadas**: botones **Sí/No** en `QMessageBox` forzados vía i18n (`action.yes` / `action.no`).

### Corregido
- **Tipado**: corrección en `_extract_centered_child` que podía provocar `SyntaxError`.
- Pequeñas limpiezas de estilo sin cambios funcionales.

### [EN]
### Changed
- **pending_panel**: unified to **PySide6** (removed PyQt5 import).
- **Persistent size dialogs**: `MonstersDialog` and `DuoBalanceDialog` now use `PersistentSizeMixin` (keys: `monsters_dialog`, `duo_balance_dialog`).
- **MonstersDialog**: auto-resize columns (`QHeaderView.ResizeToContents`) and disabled word-wrap for headers/rows.
- **Localized confirmations**: **Yes/No** buttons in `QMessageBox` forced via i18n (`action.yes` / `action.no`).

### Fixed
- **Typing**: fixed `_extract_centered_child` annotation that could cause `SyntaxError`.
- Minor style cleanups with no functional changes.

---

## [v0.3.7.4] — 2025-08-22
### [ES]
### Cambiado
- **i18n**: refactor con **alias** para eliminar duplicados sin tocar llamadas de UI.
  - Ej.: `tools.header` → `tools.title`, `pending.col.file` → `pending.col.name`.
  - Alias para etiquetas repetidas por contexto (zona, horas, hunts, etc.) hacia claves canónicas `label.*` y acciones `action.*`.
- Reorganización del catálogo en **claves canónicas**:
  - `label.zone`, `label.hunts`, `label.hours`, `label.xp_h`, `label.raw_h`, `label.balance_h`, `label.voc.*`, `label.total`, `label.solo`, `label.duo`.
  - Acciones: `action.save`, `action.close`, `action.new`, `action.delete`, `action.yes`, `action.no`.

### Corregido
- Claves que aparecían “en crudo” en la UI (ej. `tools.stats.total`, `tools.stats.voc.*`, `tools.stats.solo/duo`).
- Normalización de variantes: `pending.msg.profile_select` → `pending.msg.profile.select` mediante alias.

### [EN]
### Changed
- **i18n**: refactor with **aliases** to remove duplicates without changing UI calls.
  - Ex.: `tools.header` → `tools.title`, `pending.col.file` → `pending.col.name`.
  - Aliases for repeated context labels (zone, hours, hunts, etc.) to canonical keys `label.*` and actions `action.*`.
- Catalog reorganized into **canonical keys**:
  - `label.zone`, `label.hunts`, `label.hours`, `label.xp_h`, `label.raw_h`, `label.balance_h`, `label.voc.*`, `label.total`, `label.solo`, `label.duo`.
  - Actions: `action.save`, `action.close`, `action.new`, `action.delete`, `action.yes`, `action.no`.

### Fixed
- Keys that appeared “raw” in UI (e.g. `tools.stats.total`, `tools.stats.voc.*`, `tools.stats.solo/duo`).
- Normalized variants: `pending.msg.profile_select` → `pending.msg.profile.select` via alias.

---

## [v0.3.7.3] — 2025-08-22
### [ES]
### Corregido
- El botón **Cerrar** en paneles con `PersistentSizeMixin` ahora guarda el tamaño correctamente (antes solo lo hacía al cerrar con la X).
- Ajustes de layout en `tools_panel.py` tras integrar el mixin.

### Actualizado
- `tools_stats_dialog.py`: los títulos **“Vocación”** y **“Modo”** ahora aparecen centrados.

### Refactorizado
- Aplicado `ui_prefs.PersistentSizeMixin` en **todos** los diálogos y paneles:  
  `pending_panel.py`, `settings_panel.py`, `tools_panel.py`, `tools_stats_dialog.py`, `profiles_dialog.py`.

### [EN]
### Fixed
- The **Close** button in panels using `PersistentSizeMixin` now correctly saves the size (previously only when closed with the X).
- Minor layout fixes in `tools_panel.py` after mixin integration.

### Updated
- `tools_stats_dialog.py`: titles **“Vocation”** and **“Mode”** are now centered.

### Refactored
- Applied `ui_prefs.PersistentSizeMixin` to **all** dialogs and panels:  
  `pending_panel.py`, `settings_panel.py`, `tools_panel.py`, `tools_stats_dialog.py`, `profiles_dialog.py`.

---

## [v0.3.7.2] — 2025-08-21
### [ES]
### Refactorizado
- `pending_panel.py`: reemplazado el guardado manual de tamaño (con `config`) por `PersistentSizeMixin`.

### Añadido
- `app/services/ui_prefs.py`: helpers centralizados para recordar tamaños y mixin `PersistentSizeMixin`.

### [EN]
### Refactored
- `pending_panel.py`: replaced manual size saving (with `config`) by `PersistentSizeMixin`.

### Added
- `app/services/ui_prefs.py`: centralized helpers for remembering window sizes and `PersistentSizeMixin`.

---

## [v0.3.7.1] — 2025-08-19
### [ES]
### Añadido
- **Herramientas → Estadísticas** (`tools_stats_dialog.py`): diálogo con 3 bloques tipo tarjeta:  
  **Total** de hunts, **Vocación** (Knight, Paladin, Druid, Sorcerer, Monk) y **Modo** (Solo/Duo).

### Actualizado
- `tools/export_ready_json.py`: exporta JSON listos (no pendientes) y omite `_dataset_seen_hashes.json`.

### [EN]
### Added
- **Tools → Statistics** (`tools_stats_dialog.py`): dialog with 3 card-style sections:  
  **Total** hunts, **Vocation** (Knight, Paladin, Druid, Sorcerer, Monk), **Mode** (Solo/Duo).

### Updated
- `tools/export_ready_json.py`: exports ready JSON (non-pending) and skips `_dataset_seen_hashes.json`.

---

## [v0.3.7.0] — 2025-08-18
### [ES]
### Refactorizado
- Migración inicial de ventanas/paneles a `ui_prefs` para recordar tamaño.
- Preparación de estilo unificado para botones cuadrados.

### [EN]
### Refactored
- Initial migration of windows/panels to `ui_prefs` for persistent size.
- Preparation for unified square button styling.

---

## [v0.3.6.13]
### [ES]
### Añadido
- Diálogo **Estadísticas** inicial en Herramientas (conteos básicos).  
  *(Mejorado en v0.3.7.1)*

### [EN]
### Added
- Initial **Statistics** dialog in Tools (basic counts).  
  *(Improved in v0.3.7.1)*

---

## [v0.3.6.12] — 2025-08-16
### [ES]
### Cambiado
- `aggregator.py`: en modo **Duo**, el **Balance/h** solo se calcula con hunts que tengan **Balance Real** válido.

### [EN]
### Changed
- `aggregator.py`: in **Duo** mode, **Balance/h** is only calculated from hunts with valid **Real Balance**.

---

## [v0.3.6.11]
### [ES]
### Corregido
- `load_hunts_from_library()`: ignora `_dataset_seen_hashes.json` para evitar errores.

### [EN]
### Fixed
- `load_hunts_from_library()`: skips `_dataset_seen_hashes.json` to avoid errors.

---

## [v0.3.6.10] — 2025-08-15
### [ES]
### Añadido
- Botón en Herramientas para **Descargar biblioteca** de JSON verificados.
- Registro local `_dataset_seen_hashes.json` para evitar duplicados.

### Corregido
- Manejo robusto de `MANIFEST` en distintos formatos.

### [EN]
### Added
- Tools button to **Download verified JSON library**.
- Local `_dataset_seen_hashes.json` file to prevent duplicates.

### Fixed
- Robust handling of `MANIFEST` in different formats.

---

## [v0.3.6.9]
### [ES]
### Corregido
- Dataset: si un archivo se borra localmente, la siguiente descarga lo recupera.

### [EN]
### Fixed
- Dataset: if a file is deleted locally, the next download restores it.

---

## [v0.3.6.8]
### [ES]
### Actualizado
- Traducciones en `i18n`: corregido bug de **idioma invertido** en Settings.

### [EN]
### Updated
- `i18n` translations: fixed **inverted language** bug in Settings.

---

## [v0.3.6.7] — 2025-08-14
### [ES]
### Refactorizado
- **Manifest** en AppData para deduplicación por hash en la biblioteca local.

### [EN]
### Refactored
- **Manifest** in AppData for deduplication by hash in the local library.

---

## [v0.3.6.6]
### [ES]
### Actualizado
- Reestructuración de `assets/` (`icons/`, `fonts/`, `backgrounds/`).
- Comando **PyInstaller** actualizado para incluir assets en el .exe.

### [EN]
### Updated
- Restructured `assets/` folders (`icons/`, `fonts/`, `backgrounds/`).
- Updated **PyInstaller** command to package assets into the .exe.

---

## [v0.3.6.5]
### [ES]
### Cambiado
- En la barra superior, el label “Pendientes: X” ahora es un **botón**.

### [EN]
### Changed
- In the top bar, “Pending: X” label is now a **button**.

---

## [v0.3.6.4]
### [ES]
### Actualizado
- Botón **Sincronizar ahora** sustituido por **icono cuadrado** (`sync_now.png`).

### [EN]
### Updated
- **Sync Now** button replaced with **square icon** (`sync_now.png`).

---

## [v0.3.6.3]
### [ES]
### Actualizado
- Botón **Ajustes** sustituido por **icono de engranaje** (`settings_gear.png`).

### [EN]
### Updated
- **Settings** button replaced with **gear icon** (`settings_gear.png`).

---

## [v0.3.6.2] — 2025-08-13
### [ES]
### Añadido
- Nuevos botones en la ventana principal: **Ajustes** y **Herramientas**.
- **SettingsDialog**: selección de idioma y carpeta de JSON.

### [EN]
### Added
- New buttons in the main window: **Settings** and **Tools**.
- **SettingsDialog**: language selection and Tibia JSON folder.

---

## [v0.3.6.1] — 2025-08-21
### [ES]
### Corregido
- Corrección en la carga de estilos desde `style.qss`.
- Ajustadas las rutas en `main.py` y `paths.py` para que funcionen correctamente en la versión compilada.
- Ahora los assets se cargan de forma completa en el ejecutable.

### [EN]
### Fixed
- Fixed loading of styles from `style.qss`.
- Adjusted paths in `main.py` and `paths.py` for proper executable compatibility.
- Assets are now fully loaded in the compiled version.

---

## [v0.3.6.0] — 2025-08-20
### [ES]
### Añadido
- Soporte para recordar dos configuraciones de tamaño de ventana según el filtro High/Low.
- Panel Pendientes con tamaño de ventana independiente, recordado entre sesiones.

### Corregido
- Los cambios en metadatos de JSON ahora se guardan correctamente desde el Panel Pendientes.
- Ajustes de centrado en las tablas (columnas y casillas de verificación).

### [EN]
### Added
- Support for saving and remembering two window size configurations depending on High/Low filter.
- Pending Panel with independent window size, remembered across sessions.

### Fixed
- Metadata changes in JSON now save correctly from the Pending Panel.
- Table alignment adjustments (columns and checkboxes).

---

## [v0.3.5.2] — 2025-08-19
### [ES]
### Corregido
- Corregido el error en el Panel Pendientes que generaba excepciones al cambiar vocación o modo.
- El botón **Guardar cambios** ahora aplica correctamente las modificaciones en los JSON.

### [EN]
### Fixed
- Fixed the Pending Panel error causing exceptions when changing vocation or mode.
- The **Save changes** button now correctly applies modifications to JSON files.

---

## [v0.3.5.0] — 2025-08-18
### [ES]
### Añadido
- Ordenamiento en la tabla por columnas: numérico (↑↓) en todas las métricas y alfabético en la columna **Zona**.

### [EN]
### Added
- Table sorting by columns: numeric (↑↓) for all metrics and alphabetical for the **Zone** column.

---

## [v0.3.4.0] — 2025-08-15
### [ES]
### Añadido
- Implementación inicial de exportación a CSV desde la ventana principal.
- Añadido panel de pendientes para mostrar archivos con metadatos faltantes.
- Integración con sistema de filtros por vocación y modo.

### [EN]
### Added
- Initial implementation of CSV export from main window.
- Added pending panel to show files with missing metadata.
- Integrated with vocation and mode filtering system.

---

## [v0.3.0.0] — 2025-08-12
### [ES]
### Añadido
- Estructura inicial de la app con interfaz en PySide6.
- Barra superior con opciones: elegir carpeta JSON, contador de pendientes, exportar CSV.
- Vista central con tabla de medias por zona.
- Configuración de proyecto para build con PyInstaller.

### [EN]
### Added
- Initial app structure with PySide6 UI.
- Top bar with options: choose JSON folder, pending counter, export CSV.
- Central view with per-zone averages table.
- Project setup for PyInstaller build.

---

## [v0.0.0.0] — 2025-08-11
### [ES]
### Añadido
- Creación de estructura base del repositorio.
- Definición del modelo de datos (`HuntRecord`, `AggregatedZone`, enums `Vocation` y `Mode`).
- Lectura y normalización inicial de JSON exportados desde el cliente Tibia.

### [EN]
### Added
- Created base repository structure.
- Defined data model (`HuntRecord`, `AggregatedZone`, enums `Vocation` and `Mode`).
- Initial reading and normalization of JSON exported from Tibia client.
