"""
deduplicador.py
Script para detectar y eliminar archivos duplicados (idénticos) en una carpeta destino (por ejemplo c:/temp/wsfephp-vw).
- Compara archivos por nombre y contenido (checksum SHA256).
- Elimina duplicados exactos, dejando solo uno por nombre y contenido.
- Si existen archivos con el mismo nombre pero diferente contenido, los reporta para revisión manual (NO elimina ninguno).
- Genera un log de archivos eliminados (deduplicados_log.txt) y de archivos con conflicto de contenido (deduplicados_conflictos.txt).

Uso:
    python deduplicador.py [CARPETA]
    (por defecto CARPETA = c:/temp/wsfephp-vw)
"""

import os
import sys
import hashlib

DESTINO = r"c:/temp/wsfephp-vw"
LOG_DEDUP = "deduplicados_log.txt"
LOG_CONFLICTOS = "deduplicados_conflictos.txt"

def sha256sum(filename, block_size=65536):
    h = hashlib.sha256()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            h.update(block)
    return h.hexdigest()

def encontrar_duplicados(carpeta):
    archivos = {}
    for root, dirs, files in os.walk(carpeta):
        for file in files:
            path = os.path.join(root, file)
            archivos.setdefault(file, []).append(path)
    return archivos

def main():
    carpeta = sys.argv[1] if len(sys.argv) > 1 else DESTINO
    archivos = encontrar_duplicados(carpeta)
    eliminados = []
    conflictos = []
    for nombre, paths in archivos.items():
        if len(paths) == 1:
            continue
        # Agrupa por hash
        hashes = {}
        for path in paths:
            try:
                h = sha256sum(path)
                hashes.setdefault(h, []).append(path)
            except Exception as e:
                print(f"Error leyendo {path}: {e}")
        # Si hay más de un hash, hay conflicto de contenido
        if len(hashes) > 1:
            conflictos.append((nombre, hashes))
            continue
        # Si todos son idénticos, elimina todos menos uno
        paths_to_delete = []
        for hash_val, iguales in hashes.items():
            if len(iguales) > 1:
                # Conserva el primero, elimina el resto
                paths_to_delete.extend(iguales[1:])
        for p in paths_to_delete:
            try:
                os.remove(p)
                eliminados.append(p)
            except Exception as e:
                print(f"Error eliminando {p}: {e}")

    # Logs
    with open(LOG_DEDUP, "w", encoding="utf-8") as f:
        f.write("# Archivos eliminados por ser duplicados exactos\n")
        for path in eliminados:
            f.write(path + "\n")
    with open(LOG_CONFLICTOS, "w", encoding="utf-8") as f:
        f.write("# Archivos con el mismo nombre pero diferente contenido\n")
        for nombre, hashes in conflictos:
            f.write(f"\n[{nombre}]\n")
            for hash_val, paths in hashes.items():
                f.write(f"  Hash: {hash_val}\n")
                for path in paths:
                    f.write(f"    {path}\n")
    print(f"DEDUPLICACIÓN COMPLETA: {len(eliminados)} duplicados eliminados.")
    print(f"Revisa '{LOG_CONFLICTOS}' para ver archivos con conflicto de contenido (requieren revisión manual).")

if __name__ == "__main__":
    main()