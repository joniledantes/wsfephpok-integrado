"""
estructura_final.py
Script para organizar archivos en la estructura de carpetas definitiva de un módulo Dolibarr.
- Mueve archivos desde una carpeta (ej: c:/temp/wsfephp-vw) a subcarpetas según reglas predefinidas.
- Usa extensión, nombre y patrones para decidir la carpeta de destino (class, core, admin, sql, plantillas, lang, tools, docs, etc).
- Crea las carpetas si no existen.
- No sobreescribe archivos existentes; si hay conflicto, añade sufijo incremental.
- Genera un log de movimientos (estructura_final_log.txt) y de archivos no clasificados (estructura_no_clasificados.txt).

Uso:
    python estructura_final.py [ORIGEN] [DESTINO]
    Por defecto: ORIGEN = c:/temp/wsfephp-vw, DESTINO = c:/temp/wsfephp-vw/ordenado
"""

import os
import sys
import shutil
import re

ORIGEN = r"c:/temp/wsfephp-vw"
DESTINO = r"c:/temp/wsfephp-vw/ordenado"
LOG_MOV = "estructura_final_log.txt"
LOG_NOCLAS = "estructura_no_clasificados.txt"

# Reglas de clasificación: [(regex, subcarpeta)]
REGLAS = [
    (r"\.class\.php$", "class"),
    (r"^wsfe.*\.php$", "class"),
    (r"^dolibarr_adapter.*\.php$", "class"),
    (r"^errorhandler.*\.php$", "class"),
    (r"^util.*\.php$", "class"),
    (r"^comprobante.*\.php$", "class"),
    (r"^admin.*\.php$", "admin"),
    (r"\.sql$", "sql"),
    (r"\.md$", "docs"),
    (r"\.pdf$", "plantillas"),
    (r"\.png$|\.jpg$|\.jpeg$|\.svg$", "plantillas"),
    (r"\.xml$", "xml_examples"),
    (r"\.crt$|\.key$", "keys"),
    (r"\.lang$", "langs"),
    (r"\.sh$|\.bat$|\.py$", "tools"),
    (r"\.js$", "core/js"),
    (r"\.css$", "core/css"),
    (r"\.tpl\.php$", "templates"),
    (r"mod_facture_wsfe\.php$", "core/modules/facture"),
    (r"^pdf_fe\.modules.*\.php$", "core/modules/facture/doc"),
    (r".*dashboard.*\.php$", "scripts"),
    (r".*validate.*\.php$", "scripts"),
    (r".*backup.*\.php$", "scripts"),
    (r".*migration.*\.php$", "scripts"),
    (r".*compliance.*\.php$", "scripts"),
]

def clasificar_archivo(nombre):
    for patron, carpeta in REGLAS:
        if re.search(patron, nombre, re.IGNORECASE):
            return carpeta
    return None

def mover_archivos(origen, destino):
    movimientos = []
    no_clasificados = []
    for root, dirs, files in os.walk(origen):
        for file in files:
            rel_dir = os.path.relpath(root, origen)
            rel_dir = "" if rel_dir == "." else rel_dir
            nombre = file
            subcarpeta = clasificar_archivo(nombre)
            dest_dir = os.path.join(destino, subcarpeta) if subcarpeta else os.path.join(destino, "no_clasificados")
            os.makedirs(dest_dir, exist_ok=True)
            src_path = os.path.join(root, file)
            dest_path = os.path.join(dest_dir, nombre)
            # Si existe, añade sufijo incremental
            suf = 1
            base, ext = os.path.splitext(nombre)
            while os.path.exists(dest_path):
                dest_path = os.path.join(dest_dir, f"{base}_{suf}{ext}")
                suf += 1
            try:
                shutil.move(src_path, dest_path)
                movimientos.append((src_path, dest_path))
            except Exception as e:
                print(f"Error moviendo {src_path}: {e}")
                no_clasificados.append(src_path)
    return movimientos, no_clasificados

def main():
    origen = sys.argv[1] if len(sys.argv) > 1 else ORIGEN
    destino = sys.argv[2] if len(sys.argv) > 2 else DESTINO
    movimientos, no_clasificados = mover_archivos(origen, destino)
    with open(LOG_MOV, "w", encoding="utf-8") as f:
        f.write("# Log de movimientos de archivos a la estructura final\n")
        for old, new in movimientos:
            f.write(f"{old} => {new}\n")
    with open(LOG_NOCLAS, "w", encoding="utf-8") as f:
        f.write("# Archivos que no pudieron ser clasificados/movidos\n")
        for path in no_clasificados:
            f.write(path + "\n")
    print(f"ESTRUCTURACION COMPLETA: {len(movimientos)} archivos movidos a {destino}")
    print(f"Revisa '{LOG_NOCLAS}' para ver archivos no clasificados o con errores.")

if __name__ == "__main__":
    main()