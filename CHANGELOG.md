# 📜 Changelog

---

## v0.3.6.1 – 2025-08-21

**ES**  
### 🔧 Arreglado  
- Corrección en la carga de estilos desde `style.qss`.  
- Ajustadas las rutas en `main.py` y `paths.py` para que funcionen correctamente en la versión compilada.  
- Ahora los assets se cargan de forma completa en el ejecutable.  

**EN**  
### 🔧 Fixed  
- Fixed loading of styles from `style.qss`.  
- Adjusted paths in `main.py` and `paths.py` for proper executable compatibility.  
- Assets are now fully loaded in the compiled version.  

---

## v0.3.6.0 – 2025-08-20

**ES**  
### ✨ Añadido  
- Soporte para guardar y recordar dos configuraciones de tamaño de ventana, dependiendo del filtro High/Low.  
- Panel Pendientes con tamaño de ventana independiente y recordado entre sesiones.  
### 🔧 Arreglado  
- Los cambios en metadatos de JSON ahora se guardan correctamente desde el Panel Pendientes.  
- Ajustes de centrado en las tablas (columnas y casillas de verificación).  

**EN**  
### ✨ Added  
- Support for saving and remembering two window size configurations, depending on High/Low filter.  
- Pending Panel with independent window size, remembered across sessions.  
### 🔧 Fixed  
- Metadata changes in JSON now save correctly from the Pending Panel.  
- Table alignment adjustments (columns and checkboxes).  

---

## v0.3.5.2 – 2025-08-19

**ES**  
### 🔧 Arreglado  
- Corregido el error en el Panel Pendientes que generaba excepciones al cambiar vocación o modo.  
- Ahora el botón **Guardar cambios** aplica correctamente las modificaciones en los JSON.  

**EN**  
### 🔧 Fixed  
- Fixed the Pending Panel error causing exceptions when changing vocation or mode.  
- The **Save changes** button now correctly applies modifications to JSON files.  

---

## v0.3.5.0 – 2025-08-18

**ES**  
### ✨ Añadido  
- Ordenamiento en la tabla por columnas:  
  - Númerico (↑↓) en todas las métricas.  
  - Alfabético en la columna Zona.  

**EN**  
### ✨ Added  
- Table sorting by columns:  
  - Numeric (↑↓) for all metrics.  
  - Alphabetical for Zone column.  

---

## v0.3.4.0 – 2025-08-15

**ES**  
### ✨ Añadido  
- Implementación inicial de exportación a CSV desde la ventana principal.  
- Añadido panel de pendientes para mostrar archivos con metadatos faltantes.  
- Integración con sistema de filtros por vocación y modo.  

**EN**  
### ✨ Added  
- Initial implementation of CSV export from main window.  
- Added pending panel to show files with missing metadata.  
- Integrated with vocation and mode filtering system.  

---

## v0.3.0.0 – 2025-08-12

**ES**  
### ✨ Añadido  
- Estructura inicial de la app con interfaz en PySide6.  
- Barra superior con opciones: elegir carpeta JSON, contador de pendientes, exportar CSV.  
- Vista central con tabla de medias por zona.  
- Configuración de proyecto para build con PyInstaller.  

**EN**  
### ✨ Added  
- Initial app structure with PySide6 UI.  
- Top bar with options: choose JSON folder, pending counter, export CSV.  
- Central view with per-zone averages table.  
- Project setup for PyInstaller build.  

---

## v0.0.0.0 – 2025-08-11

**ES**  
### 🛠️ Inicio del proyecto  
- Creación de estructura base del repositorio.  
- Definición del modelo de datos (`HuntRecord`, `AggregatedZone`, enums `Vocation` y `Mode`).  
- Primeros pasos con lectura y normalización de JSON exportados desde el cliente Tibia.  

**EN**  
### 🛠️ Project start  
- Created base repository structure.  
- Defined data model (`HuntRecord`, `AggregatedZone`, enums `Vocation` and `Mode`).  
- First steps with reading and normalizing JSON exported from Tibia client.  
