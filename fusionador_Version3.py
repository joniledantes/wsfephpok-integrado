"""
fusionador.py
Script para automatizar la fusión de archivos según arbol.txt y fusion_plan.txt

- Lee arbol.txt (árbol de archivos con rutas relativas o absolutas).
- Lee fusion_plan.txt (plan de archivos [ELEGIDO] a conservar).
- Copia todos los archivos marcados como [ELEGIDO] a una carpeta destino (por ejemplo, /custom/wsfephpok/).
- Genera un log de archivos copiados y una lista de los que requieren revisión manual.
- Si hay conflictos de nombres, añade sufijo incremental.
- Uso: python fusionador.py ORIGEN DESTINO
  (por defecto ORIGEN="." y DESTINO="./custom/wsfephpok/")
"""

import os
import sys
import shutil
import re

ARBOLE = "arbol.txt"
PLAN = "fusion_plan.txt"
DEFAULT_ORIGEN = "."
DEFAULT_DESTINO = "./custom/wsfephpok/"
LOG_COPIADOS = "fusion_log.txt"
LOG_PENDIENTES = "fusion_pendientes.txt"

def leer_elegidos(plan_path):
    elegidos = set()
    pendientes = set()
    actual = None
    with open(plan_path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "[ELEGIDO]" in line:
                # Ejemplo: "   [ELEGIDO] wsfe_doli.php"
                archivo = line.split("[ELEGIDO]")[-1].strip()
                elegidos.add(archivo)
                actual = archivo
            elif "Sugerencia" in line or "revisa/integra" in line or "revisar/integra" in line:
                if actual:
                    pendientes.add(actual)
    return elegidos, pendientes

def listar_rutas_arbol(arbol_path):
    rutas = {}
    with open(arbol_path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            # Buscar líneas con una ruta de archivo
            match = re.search(r'([A-Za-z]:)?[\\/][^:*?"<>|\r\n]+?\.\w+', line)
            if match:
                ruta = line.strip().replace("│", "").replace("�", "").replace("├", "").replace("─", "").replace("└", "").replace(" ", "")
                nombre = os.path.basename(ruta)
                if nombre not in rutas:
                    rutas[nombre] = []
                rutas[nombre].append(ruta)
    return rutas

def copiar_archivos(elegidos, rutas, origen, destino):
    copiados = []
    conflictos = []
    os.makedirs(destino, exist_ok=True)
    for nombre in elegidos:
        if nombre in rutas:
            for idx, ruta_rel in enumerate(rutas[nombre]):
                ruta_abs = os.path.join(origen, ruta_rel) if not os.path.isabs(ruta_rel) else ruta_rel
                if not os.path.isfile(ruta_abs):
                    continue
                nombre_final = nombre
                dest_file = os.path.join(destino, nombre_final)
                # Si ya existe, agrega sufijo incremental
                suf = 1
                while os.path.exists(dest_file):
                    nombre_final = f"{os.path.splitext(nombre)[0]}_{suf}{os.path.splitext(nombre)[1]}"
                    dest_file = os.path.join(destino, nombre_final)
                    suf += 1
                shutil.copy2(ruta_abs, dest_file)
                copiados.append(dest_file)
                if suf > 1:
                    conflictos.append(dest_file)
                break  # Solo copia una instancia por archivo elegido
    return copiados, conflictos

def main():
    origen = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ORIGEN
    destino = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_DESTINO
    elegidos, pendientes = leer_elegidos(PLAN)
    rutas = listar_rutas_arbol(ARBOLE)
    copiados, conflictos = copiar_archivos(elegidos, rutas, origen, destino)
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
    print(f"COPIA COMPLETA: {len(copiados)} archivos copiados a {destino}")
    print(f"Revisa '{LOG_PENDIENTES}' para ver archivos que requieren integración manual.")

if __name__ == "__main__":
    main()