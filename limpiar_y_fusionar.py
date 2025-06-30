import os
import shutil
import hashlib
from collections import defaultdict

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def limpiar_y_fusionar(origen, destino):
    os.makedirs(destino, exist_ok=True)

    archivos_por_nombre = defaultdict(list)
    archivos_por_hash = defaultdict(list)

    # Recorrer recursivamente todo origen, incluyendo raíz
    for root, _, files in os.walk(origen):
        for f in files:
            if f.endswith(".py"):
                ruta = os.path.join(root, f)
                h = hash_file(ruta)
                archivos_por_nombre[f].append((ruta, h))
                archivos_por_hash[h].append(ruta)

    log = []

    # Detectar duplicados por contenido
    duplicados_por_contenido = {h: rutas for h, rutas in archivos_por_hash.items() if len(rutas) > 1}
    if duplicados_por_contenido:
        log.append("Duplicados detectados por contenido (hash SHA256):")
        for h, rutas in duplicados_por_contenido.items():
            log.append(f" Hash: {h}")
            for r in rutas:
                log.append(f"  - {r}")
        log.append("")

    # Procesar por nombre y elegir la versión más reciente
    for nombre, lista in archivos_por_nombre.items():
        # Ordenar por fecha de modificación (más reciente primero)
        lista.sort(key=lambda x: os.path.getmtime(x[0]), reverse=True)
        mejor_ruta, mejor_hash = lista[0]

        destino_final = os.path.join(destino, nombre)

        # Si el archivo ya existe en destino y es idéntico, no copiar
        if os.path.exists(destino_final):
            if hash_file(destino_final) == mejor_hash:
                log.append(f"{nombre}: archivo idéntico ya existe en destino, no se copia.")
                continue

        shutil.copy2(mejor_ruta, destino_final)
        log.append(f"Copiado {nombre} desde {mejor_ruta}")

        if len(lista) > 1:
            log.append(f" Duplicados con nombre '{nombre}':")
            for ruta, h in lista:
                log.append(f"  - {ruta} (hash {h})")

    # Detectar archivos con distinto nombre pero mismo contenido
    hash_a_nombres = defaultdict(set)
    for nombre, lista in archivos_por_nombre.items():
        for _, h in lista:
            hash_a_nombres[h].add(nombre)

    for h, nombres in hash_a_nombres.items():
        if len(nombres) > 1:
            log.append(f"Atención: mismo contenido (hash {h}) con distintos nombres: {', '.join(nombres)}")

    # Guardar log completo
    log_path = os.path.join(destino, "resumen_fusion_completo.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log))

    print("\n".join(log))
    print(f"\nRegistro guardado en {log_path}")

if __name__ == "__main__":
    origen = r"C:\Temp\scripts_limpios_wsfephpok"
    destino = r"C:\Temp\scripts_limpios_wsfephpok_limpio"

    limpiar_y_fusionar(origen, destino)
