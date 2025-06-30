import os
import difflib
import re

# Ruta base donde están los scripts organizados
RUTA_BASE = r"C:\temp\scripts_limpios_wsfephpok"
RUTA_SALIDA = os.path.join(RUTA_BASE, "fusionados")
os.makedirs(RUTA_SALIDA, exist_ok=True)

# Detecta similitud de nombre base (sin versión)
def nombre_base(nombre):
    return re.sub(r'(_Version\d+|\d+)?\.py$', '', nombre.lower())

# Agrupa por nombre base
def agrupar_por_similitud(ruta):
    grupos = {}
    for root, _, files in os.walk(ruta):
        for file in files:
            if file.endswith(".py"):
                base = nombre_base(file)
                grupos.setdefault(base, []).append(os.path.join(root, file))
    return {k: v for k, v in grupos.items() if len(v) > 1}

# Fusiona varios archivos en uno, anotando diferencias
def fusionar_archivos(grupo, base_name):
    bloques = []
    archivos = [open(f, encoding="utf-8").readlines() for f in grupo]
    nombres = [os.path.basename(f) for f in grupo]
    
    max_len = max(len(a) for a in archivos)
    archivos = [a + ['\n'] * (max_len - len(a)) for a in archivos]

    for i in range(max_len):
        lineas = [a[i] for a in archivos]
        if all(l == lineas[0] for l in lineas):
            bloques.append(lineas[0])
        else:
            for idx, l in enumerate(lineas):
                bloques.append(f"###>>> VERSION: {nombres[idx]}")
                bloques.append(l.rstrip() + "\n")
            bloques.append("###---\n")

    ruta_salida = os.path.join(RUTA_SALIDA, f"{base_name}_fusionado.py")
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.writelines(bloques)
    print(f"[✔] Fusionado: {ruta_salida}")

if __name__ == "__main__":
    print("[+] Buscando scripts con versiones similares...")
    grupos_similares = agrupar_por_similitud(RUTA_BASE)

    for base, grupo in grupos_similares.items():
        print(f"[~] Fusionando grupo: {base} ({len(grupo)} archivos)")
        fusionar_archivos(grupo, base)

    print("[✔] Todos los grupos similares han sido fusionados.")
