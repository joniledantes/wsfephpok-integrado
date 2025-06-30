"""
normalizador_nombres.py
Script para renombrar archivos en una carpeta (por ejemplo c:/temp/wsfephp-vw) siguiendo convenciones:
- Elimina espacios y los reemplaza por guiones bajos.
- Convierte nombres a minúsculas (opcional, configurable).
- Cambia extensiones conocidas a estándar (ej: .class (1).php → .class.php).
- Elimina paréntesis, corchetes, tildes, caracteres raros.
- Genera un log de los cambios realizados (normalizacion_log.txt).

Uso:
    python normalizador_nombres.py [CARPETA]
    (por defecto CARPETA = c:/temp/wsfephp-vw)
"""

import os
import sys
import re
import unicodedata

CARPETA = r"c:/temp/wsfephp-vw"
LOG_NORM = "normalizacion_log.txt"
TO_LOWER = True  # Cambia a False si no quieres forzar minúsculas

def limpiar_nombre(nombre):
    # Elimina tildes y caracteres raros, reemplaza espacios por _
    nombre_base, ext = os.path.splitext(nombre)
    nombre_base = unicodedata.normalize('NFKD', nombre_base).encode('ascii', 'ignore').decode()
    nombre_base = nombre_base.replace(" ", "_")
    nombre_base = re.sub(r"[\(\)\[\]\{\}]", "", nombre_base)
    nombre_base = re.sub(r"_{2,}", "_", nombre_base)
    nombre_base = re.sub(r"-{2,}", "-", nombre_base)
    nombre_base = re.sub(r"[^A-Za-z0-9_\-.]", "", nombre_base)
    # Normaliza extensiones tipo .class (1).php → .class.php
    nombre_base = re.sub(r"\.class_\d+", ".class", nombre_base)
    nombre_base = re.sub(r"\.class\s*\d*", ".class", nombre_base)
    nombre_base = re.sub(r"_\d+$", "", nombre_base)
    ext = ext.lower()
    if TO_LOWER:
        nombre_base = nombre_base.lower()
    return nombre_base + ext

def renombrar_recursivo(carpeta):
    cambios = []
    for root, dirs, files in os.walk(carpeta):
        for file in files:
            nuevo = limpiar_nombre(file)
            old_path = os.path.join(root, file)
            new_path = os.path.join(root, nuevo)
            if nuevo != file:
                # Si existe, añade sufijo incremental
                suf = 1
                base, ext = os.path.splitext(nuevo)
                while os.path.exists(new_path):
                    nuevo_temp = f"{base}_{suf}{ext}"
                    new_path = os.path.join(root, nuevo_temp)
                    suf += 1
                os.rename(old_path, new_path)
                cambios.append((old_path, new_path))
    return cambios

def main():
    carpeta = sys.argv[1] if len(sys.argv) > 1 else CARPETA
    cambios = renombrar_recursivo(carpeta)
    with open(LOG_NORM, "w", encoding="utf-8") as f:
        f.write("# Log de normalización de nombres de archivo\n")
        for old, new in cambios:
            f.write(f"{old} => {new}\n")
    print(f"NORMALIZACION COMPLETA: {len(cambios)} archivos renombrados.")
    print(f"Revisa '{LOG_NORM}' para ver los cambios realizados.")

if __name__ == "__main__":
    main()