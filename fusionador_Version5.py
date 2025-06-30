"""
fusionador.py
Script para automatizar la fusión de archivos según arbol.txt y fusion_plan.txt

- Busca recursivamente en C:/Users/Viaweb/Documents/GitHub todos los archivos marcados como [ELEGIDO] en fusion_plan.txt.
- Copia los archivos encontrados a c:/temp/wsfephp-vw (crea la carpeta si no existe).
- Genera un log de archivos copiados (fusion_log.txt) y los que requieren revisión manual (fusion_pendientes.txt).
- Si hay conflictos de nombres, añade sufijo incremental (_1, _2, etc.).
- Uso: python fusionador.py
"""

import os
import sys
import shutil

PLAN = "fusion_plan.txt"
ORIGEN_ROOT = r"C:\Users\Viaweb\Documents\GitHub"
DESTINO = r"c:\temp\wsfephp-vw"
LOG_COPIADOS = "fusion_log.txt"
LOG_PENDIENTES = "fusion_pendientes.txt"

def leer_elegidos(plan_path):
    elegidos = set()
    pendientes = set()
    actual = None
    with open(plan_path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "[ELEGIDO]" in line:
                archivo = line.split("[ELEGIDO]")[-1].strip()
                elegidos.add(archivo)
                actual = archivo
            elif "Sugerencia" in line or "revisa/integra" in line or "revisar/integra" in line:
                if actual:
                    pendientes.add(actual)
    return elegidos, pendientes

def buscar_archivos(raiz, nombres):
    encontrados = {nombre: [] for nombre in nombres}
    for root, dirs, files in os.walk(raiz):
        for file in files:
            if file in nombres:
                encontrados[file].append(os.path.join(root, file))
    return encontrados

def copiar_archivos(encontrados, destino):
    copiados = []
    conflictos = []
    os.makedirs(destino, exist_ok=True)
    for nombre, rutas in encontrados.items():
        if rutas:
            # Si hay varias rutas para el mismo archivo, se copian todas con sufijo incremental
            for idx, ruta_abs in enumerate(rutas):
                nombre_final = nombre if idx == 0 else f"{os.path.splitext(nombre)[0]}_{idx}{os.path.splitext(nombre)[1]}"
                dest_file = os.path.join(destino, nombre_final)
                shutil.copy2(ruta_abs, dest_file)
                copiados.append(dest_file)
                if idx > 0:
                    conflictos.append(dest_file)
    return copiados, conflictos

def main():
    elegidos, pendientes = leer_elegidos(PLAN)
    encontrados = buscar_archivos(ORIGEN_ROOT, elegidos)
    copiados, conflictos = copiar_archivos(encontrados, DESTINO)
    with open(LOG_COPIADOS, "w", encoding="utf-8") as f:
        f.write("# Archivos copiados automáticamente\n")
        for path in copiados:
            f.write(path + "\n")
        if conflictos:
            f.write("\n# Archivos con conflictos de nombre (sufijo incremental):\n")
            for path in conflictos:
                f.write(path + "\n")
    with open(LOG_PENDIENTES, "w", encoding="utf-8") as f:
        f.write("# Archivos marcados para revisión/integración manual\n")
        for p in pendientes:
            f.write(p + "\n")
    print(f"COPIA COMPLETA: {len(copiados)} archivos copiados a {DESTINO}")
    print(f"Revisa '{LOG_PENDIENTES}' para ver archivos que requieren integración manual.")

if __name__ == "__main__":
    main()