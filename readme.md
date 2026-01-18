# 🎬 YouTube HD Downloader

![Demo](demo.gif)

**YouTube HD Downloader** es un descargador profesional de vídeos de YouTube en **HD, Full HD, 4K y audio MP3**, desarrollado en **Python** y basado en `yt-dlp`.  
Incluye una **CLI moderna**, salida con colores, barras de progreso, previsualización del contenido y soporte para descargas en lote.

---

## ✨ Características

- 🎨 **Interfaz CLI avanzada** con colores y progreso visual (`rich`)
- 📱 **Comandos profesionales** con ayuda y autocompletado (`typer`)
- 📺 **Vista previa del vídeo** antes de descargar
- ⚡ **Múltiples calidades**: mejor, 1080p, 720p o solo audio
- 📚 **Descargas en lote** desde archivo de texto
- 🔍 **Listado de formatos** disponibles sin descargar
- 🛡️ **Manejo robusto de errores**
- 🎵 **Extracción de audio MP3** en alta calidad

---

## 📦 Requisitos

### Dependencias del sistema
- Python **3.9+**
- `ffmpeg`

En sistemas Debian/Ubuntu:

```bash
sudo apt update
sudo apt install -y ffmpeg python3-pip python3-venv
```

---

## 📥 Instalación

### 1️⃣ Clonar el repositorio

```bash
git clone <repo>
cd youtube-downloader
```

> Alternativamente, descarga solo el archivo `yt_pro.py`.

### 2️⃣ Crear entorno virtual (recomendado)

```bash
python3 -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows
```

### 3️⃣ Instalar dependencias de Python

```bash
pip install yt-dlp typer rich
```

---

## 🚀 Uso rápido

### Descargar vídeo en máxima calidad (con preview)

```bash
python yt_pro.py descargar "https://youtube.com/watch?v=VIDEO_ID"
```

### Descargar solo audio en MP3

```bash
python yt_pro.py descargar "URL" --audio
```

### Elegir calidad y carpeta de destino

```bash
python yt_pro.py descargar "URL" --calidad 1080p --carpeta Videos
```

### Ver información del vídeo sin descargar

```bash
python yt_pro.py lista "URL"
```

### Descarga en lote desde archivo

```bash
echo -e "URL1\nURL2\nURL3" > urls.txt
python yt_pro.py batch urls.txt
```

---

## 📋 Comandos disponibles

```bash
python yt_pro.py --help
```

| Comando     | Descripción                         | Ejemplo |
|------------|--------------------------------------|--------|
| `descargar` | Descarga vídeo o audio              | `python yt_pro.py descargar "URL" --calidad 1080p` |
| `lista`     | Muestra info y formatos disponibles | `python yt_pro.py lista "URL"` |
| `batch`     | Descarga múltiples URLs             | `python yt_pro.py batch urls.txt` |

---

## ⚙️ Opciones avanzadas

### 🎥 Calidad de descarga

```bash
--calidad mejor     # Máxima disponible (hasta 8K)
--calidad 1080p    # Full HD
--calidad 720p     # HD
--calidad audio    # Solo audio MP3
```

### 📂 Configuración

```bash
--carpeta ./Videos   # Carpeta de destino personalizada
--audio              # Fuerza descarga solo de audio
```

> ⚠️ Si se usa `--audio`, la calidad de vídeo se ignora.

---

## 🗂️ Estructura del proyecto

```text
youtube-downloader/
├── yt_pro.py          # 🎬 Script principal
├── urls.txt           # 📄 URLs para batch (opcional)
├── videos/            # 📁 Descargas (auto-creada)
└── .venv/             # 🐍 Entorno virtual
```

---

## 🎨 Demo de ejecución

```text
$ python yt_pro.py descargar "https://youtube.com/watch?v=..."

╭───────────────── 📺 Obteniendo información... ─────────────────╮
│                                                                │
╰────────────────────────────────────────────────────────────────╯

╭─ 🎥 La mayoría de venezolanos apoyan... ───────────────────────╮
│ 👤 Juan Ramón Rallo │ ⏱️ 09:42 │ 👀 125,430                   │
╰────────────────────────────────────────────────────────────────╯

¿Descargar? [Enter=yes / n=no]:

📥 Descargando... (75.2%)
✅ /home/user/videos/La mayoría de venezolanos... (mp4)

🎉 ¡Completado!
📂 Guardado en: /home/user/videos
```

---

## 🔧 Solución de problemas

| Error | Solución |
|-----|---------|
| `ffmpeg not installed` | `sudo apt install ffmpeg` |
| Advertencia JS runtime | Puede ignorarse |
| `Permission denied` | `chmod +x yt_pro.py` |
| `Module not found` | `pip install yt-dlp typer rich` |

---

## 📈 Formatos soportados

- **Vídeo + audio:** MP4 (mejor calidad disponible)
- **Solo audio:** MP3 (alta calidad)
- **Resoluciones:** 8K, 4K, 1080p, 720p, 480p…
- **Plataformas:**  
  - YouTube  
  - YouTube Shorts  
  - Listas de reproducción (configurable con `--noplaylist`)
