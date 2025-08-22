# 📒 Cuaderno interno --- Tibia Analyzer (visor)

## 1) Alcance y contribuciones

-   **Aportes externos:** solo **JSON** "verificados" (Hunt Analyzer).\
-   **No se aceptan PR de código** de terceros. El código y la
    arquitectura quedan bajo nuestro control.
-   Librería pública en GitHub: `datasets/json/` (organizada por
    `by-hash/<sha>.json` + `MANIFEST.json`).

------------------------------------------------------------------------

## 2) Estructura de proyecto (actual)

    app/
      main.py
      data/
        loader.py
        normalizer.py
        schema.py
        writer.py
      services/
        aggregator.py
        config.py
        i18n.py
        library_sync.py
        paths.py
        ui_prefs.py
        dataset_fetch.py
      ui/
        main_window.py
        filters_panel.py
        zones_table.py
        pending_panel.py
        profiles_dialog.py
        settings_panel.py
        tools_panel.py
        tools_stats_dialog.py
        style.qss
    assets/
      icons/
      fonts/
      backgrounds/
    build/
    dist/
    tools/

------------------------------------------------------------------------

## 3) Estilos y UI

### 3.1 Tema global (style.qss)

-   Se mantiene en `app/ui/style.qss` **como hasta ahora** (no mover a
    assets).\
-   **No eliminar** el QSS base existente.\
-   Añadido **bloque** reutilizable para botones cuadrados:

``` css
.square-btn {
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    background-color: #242424;
    padding: 0px;
}
.square-btn:hover {
    background-color: #2e2e2e;
    border-color: #565656;
}
.square-btn:pressed {
    background-color: #1e1e1e;
    border-color: #6a6a6a;
}
```

------------------------------------------------------------------------

## 4) Persistencia de tamaño (regla obligatoria)

**Todas** las ventanas, paneles y diálogos deben usar
`app/services/ui_prefs.py`.

------------------------------------------------------------------------

## 5) Reglas de datos y agregación

-   **Filtros inteligentes**: Vocation y Mode filtran entre sí y con
    niveles.
-   **Duo**: el balance solo se computa si hay "Balance Real" y no está
    "Ignorar Balance".

------------------------------------------------------------------------

## 6) Sincronización de JSON

-   **Importar desde carpeta origen**: basado en hash, evita duplicados,
    maneja MANIFEST.
-   **Descargar dataset público**: entrada de verdad =
    `by-hash/*.json`.\
-   `_dataset_seen_hashes.json` ignorado por loader.

------------------------------------------------------------------------

## 7) Paneles y diálogos --- estado actual

-   MainWindow, SettingsDialog, PendingDialog, ToolsDialog,
    ToolsStatsDialog → todos con tamaño persistente.

------------------------------------------------------------------------

## 8) i18n

-   Todo texto visible debe estar en `services/i18n.py`.

------------------------------------------------------------------------

## 9) .gitignore / scripts personales

-   Ignorar `build/`, `dist/`, `*.spec`, `tools/*`, `app/data/json/`,
    `JSON Ready/`.

------------------------------------------------------------------------

## 10) Versionado

-   Esquema **0.major.minor.patch**.

------------------------------------------------------------------------

## 11) Build (.exe)

    py -m PyInstaller app/main.py --name TibiaAnalyzer --onefile --noconsole --icon "assets/icons/icon.ico" --add-data "assets;assets" --add-data "app/ui;app/ui"

------------------------------------------------------------------------

## 12) Directrices futuras

1.  Persistencia de tamaño → `ui_prefs`\
2.  Botones cuadrados → `.square-btn`\
3.  i18n obligatorio\
4.  Hash como fuente de verdad\
5.  Evitar duplicación (estilos/lógica)\
6.  Archivos frágiles (logs, seen hashes) nunca en flujo de datos\
7.  Regla Duo → balance solo si Balance Real + no ignorado
