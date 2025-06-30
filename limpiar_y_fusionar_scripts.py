import os
import shutil
from collections import defaultdict
from pathlib import Path

ORIGEN = r"C:\Users\Viaweb\Documents\GitHub"
DESTINO = r"C:\temp\scripts_limpios_wsfephpok"
LOG = os.path.join(DESTINO, "resumen_fusion.txt")

# Crear carpeta destino si no existe
os.makedirs(DESTINO, exist_ok=True)

# Recopilar todos los archivos .py
scripts = defaultdict(list)
for root, _, files in os.walk(ORIGEN):
    for f in files:
        if f.endswith(".py"):
            ruta_completa = os.path.join(root, f)
            scripts[f].append(ruta_completa)

# Función para elegir el mejor duplicado
def elegir_mejor(archivos):
    if len(archivos) == 1:
        return archivos[0]
    
    archivos.sort(key=lambda f: (os.path.getsize(f), os.path.getmtime(f)), reverse=True)
    return archivos[0]

# Copiar el mejor archivo al destino
log = []
for nombre, versiones in scripts.items():
    mejor = elegir_mejor(versiones)
    destino_final = os.path.join(DESTINO, nombre)
    shutil.copy2(mejor, destino_final)
    
    log.append(f"{nombre} -> {mejor}")
    if len(versiones) > 1:
        log.append(f"  Duplicados detectados:")
        for v in versiones:
            log.append(f"    - {v}")

# Guardar log
with open(LOG, "w", encoding="utf-8") as f:
    f.write("\n".join(log))

print(f"\n✅ Limpieza completada. Archivos seleccionados copiados a:\n{DESTINO}\n")
print(f"📄 Registro de duplicados: {LOG}")
