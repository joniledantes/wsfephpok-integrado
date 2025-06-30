```python
#!/usr/bin/env python3
"""
procesar_completo.py

Un único script que:
 - Instala Pillow y piexif si no están.
 - Retoque de color, contraste, brillo y nitidez.
 - Añade EXIF de Samsung A21s (fechas 1–9 mayo 2025, GPS General Roca).
 - Renombra al estilo IMG_YYYYMMDD_HHMMSS_NN.jpg.
 - Procesa automáticamente los archivos 1.jpg a 9.jpg.

USO:
    python procesar_completo.py
"""

import sys, subprocess, datetime, os
from importlib import util

# ── 1) Instalar dependencias si faltan ─────────────────────────────────
def ensure(pkg, import_name=None):
    name = import_name or pkg
    if util.find_spec(name) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

ensure("Pillow", "PIL")
ensure("piexif")

from PIL import Image, ImageEnhance, ImageFilter
import piexif

# ── 2) Configuración de fechas (1–9 mayo 2025) ─────────────────────────────
FECHAS = []
for offset, dia in enumerate(range(1, 10)):
    # horas 14:30 + offset segundos
    FECHAS.append(datetime.datetime(2025, 5, dia, 14, 30, offset))

# ── 3) Coordenadas EXIF de General Roca ──────────────────────────────────
LAT, LNG, ALT = -38.6408, -67.3654, 230

def dms(deg):
    d = int(abs(deg))
    m = int((abs(deg) - d) * 60)
    s = round((((abs(deg) - d) * 60 - m) * 60) * 100)
    return ((d,1),(m,1),(s,100))

EXIF_BASE = {
    "0th": {
        piexif.ImageIFD.Make:    u"Samsung",
        piexif.ImageIFD.Model:   u"SM-A217M",
        piexif.ImageIFD.Software:u"Camera App",
    },
    "Exif": {
        piexif.ExifIFD.LensMake:  u"Samsung",
        piexif.ExifIFD.LensModel: u"SM-A217M",
        piexif.ExifIFD.ExposureTime:(1,60),
        piexif.ExifIFD.FNumber:(18,10),
        piexif.ExifIFD.ISOSpeedRatings:100,
        piexif.ExifIFD.Flash:0,
        piexif.ExifIFD.WhiteBalance:0,
    },
    "GPS": {
        piexif.GPSIFD.GPSLatitudeRef:  b"S",
        piexif.GPSIFD.GPSLatitude:     dms(LAT),
        piexif.GPSIFD.GPSLongitudeRef: b"W",
        piexif.GPSIFD.GPSLongitude:    dms(LNG),
        piexif.GPSIFD.GPSAltitudeRef:  0,
        piexif.GPSIFD.GPSAltitude:     (ALT,1),
    }
}

# ── 4) Función de procesado ───────────────────────────────────────────────
def procesar(path, fecha, index):
    img = Image.open(path)
    # retoques suaves
    img = ImageEnhance.Color(img).enhance(1.10)
    img = ImageEnhance.Contrast(img).enhance(1.05)
    img = ImageEnhance.Brightness(img).enhance(1.02)
    img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))

    # EXIF dinámico
    exif = {k: v.copy() if isinstance(v, dict) else v for k,v in EXIF_BASE.items()}
    exif['Exif'][piexif.ExifIFD.DateTimeOriginal] = fecha.strftime("%Y:%m:%d %H:%M:%S")
    exif_bytes = piexif.dump(exif)

    # nombre salida: IMG_YYYYMMDD_HHMMSS_NN.jpg
    ts = fecha.strftime("IMG_%Y%m%d_%H%M%S")
    out = f"{ts}_{index:02d}.jpg"
    cnt = 1
    while os.path.exists(out):
        out = f"{ts}_{index:02d}_{cnt}.jpg"
        cnt += 1

    img.save(out, format="JPEG", exif=exif_bytes, quality=95)
    print(f"[✓] {os.path.basename(path)} → {out}")

# ── 5) Main ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Procesar automáticamente 1.jpg a 9.jpg
    for i in range(1, 10):
        fname = f"{i}.jpg"
        if os.path.exists(fname):
            fecha = FECHAS[i-1]
            print(f"Procesando {fname} con fecha {fecha}")
            procesar(fname, fecha, i)
        else:
            print(f"[!] {fname} no existe, saltando.")
```
