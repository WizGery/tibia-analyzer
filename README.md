# 🐉 Tibia Analyzer

[Español](#español) | [English](#english)

---

## Español

**Tibia Analyzer** es una aplicación de escritorio para organizar, visualizar y analizar sesiones de caza de *Tibia* a partir de los archivos JSON exportados desde el cliente oficial.  

### ✨ Características
- 📂 Importa automáticamente los JSON de tus hunts.  
- 📊 Muestra medias por zona (XP/h, loot/h, supplies, balance).  
- 🛠️ Panel de pendientes para revisar y completar metadatos.  
- 🔍 Filtros inteligentes por vocación, modo y nivel.  
- 🔄 Sincronización con biblioteca interna de la aplicación.  

### 🚀 Instalación
1. Descarga la última versión desde la pestaña **Releases** en GitHub.  
2. Ejecuta el `.exe` standalone (no requiere instalación).  
3. ¡Listo para usar!  

📌 **Requisitos**: Windows 10/11 (64-bit).  

### ⚠️ Aviso sobre antivirus
Algunos antivirus o Windows SmartScreen pueden marcar el `.exe` como malicioso debido a heurísticas de compresión.  
👉 Esto es un **falso positivo**, muy común en aplicaciones empaquetadas con **PyInstaller** y sin firma digital.  

- El binario **no utiliza UPX**.  
- El código fuente está disponible en el repositorio para compilarlo localmente si lo prefieres.  

Pasos recomendados si aparece SmartScreen:  
1. Haz clic en “Más información”.  
2. Selecciona “Ejecutar de todas formas”.  

### 📂 Estructura de carpetas
- `app/` → Código principal.  
- `assets/` → Iconos y recursos gráficos.  
- `dist/` → Builds generadas.  
- `build/` → Archivos temporales.  
- `JSON Ready/` → Carpeta donde se guardan los JSON limpios/listos para compartir.  

### 🔧 Compilación manual
Si quieres generar tu propio `.exe`:  
```powershell
pyinstaller --onefile --noconsole --icon=assets/icon.ico --name "TibiaAnalyzer" --paths=. --add-data "assets;assets" --add-data "app/ui;app/ui" app/main.py
```

### 🤝 Contribuciones
Las contribuciones son bienvenidas: reporta bugs, sugiere mejoras o envía *pull requests*.  

---

## English

**Tibia Analyzer** is a desktop application to organize, visualize and analyze hunting sessions from *Tibia*, based on the JSON files exported by the official client.  

### ✨ Features
- 📂 Automatically imports your hunt JSON files.  
- 📊 Displays per-zone averages (XP/h, loot/h, supplies, balance).  
- 🛠️ Pending panel to review and complete metadata.  
- 🔍 Smart filters by vocation, mode, and level.  
- 🔄 Synchronization with the app’s internal library.  

### 🚀 Installation
1. Download the latest release from the **Releases** tab on GitHub.  
2. Run the standalone `.exe` (no installation required).  
3. Ready to go!  

📌 **Requirements**: Windows 10/11 (64-bit).  

### ⚠️ Antivirus warning
Some antivirus engines or Windows SmartScreen may flag the `.exe` as suspicious due to heuristic scanning.  
👉 This is a **false positive**, very common for binaries built with **PyInstaller** and without code signing.  

- The binary is built **without UPX**.  
- Source code is available so anyone can build it locally.  

If SmartScreen appears:  
1. Click “More info”.  
2. Select “Run anyway”.  

### 📂 Folder structure
- `app/` → Main code.  
- `assets/` → Icons and graphical resources.  
- `dist/` → Generated builds.  
- `build/` → Temporary files.  
- `JSON Ready/` → Folder where clean/ready JSON files are stored for sharing.  

### 🔧 Manual build
If you want to create your own `.exe`:  
```powershell
pyinstaller --onefile --noconsole --icon=assets/icon.ico --name "TibiaAnalyzer" --paths=. --add-data "assets;assets" --add-data "app/ui;app/ui" app/main.py
```

### 🤝 Contributing
Contributions are welcome: report bugs, suggest improvements, or send pull requests.  

---

📌 *Este proyecto no está afiliado a CipSoft GmbH. Tibia es una marca registrada de CipSoft GmbH.*  
📌 *This project is not affiliated with CipSoft GmbH. Tibia is a registered trademark of CipSoft GmbH.*  
