"""
fusionador_modulos.py

Script para analizar un árbol de directorios (como arbol.txt) y guardar el plan de fusión de archivos/clases/plantillas duplicadas en C:\Temp\fusion_plan.txt automáticamente.

Uso:
    python fusionador_modulos.py arbol.txt

Requiere: Python 3.x
"""

import sys
import os
import re
from collections import defaultdict

# Configuración de patrones relevantes
PATTERNS = [
    re.compile(r'\.php$'),
    re.compile(r'\.tpl\.php$'),
    re.compile(r'\.js$'),
    re.compile(r'\.lang$'),
    re.compile(r'\.pdf$'),
]

MODERN_KEYWORDS = ['FINAL', 'v2', '2104', 'sept24', '3.php', '4.php']

def parse_arbol(path):
    files = []
    with open(path, encoding='utf-8', errors='ignore') as f:
        for line in f:
            l = line.strip(' \r\n')
            if l.startswith('�') or l.startswith('│') or not l:
                continue
            if any(pat.search(l) for pat in PATTERNS):
                l = l.replace('�', '').replace('├', '').replace('─', '').replace('│', '').replace('└', '')
                l = l.strip()
                files.append(l)
    return files

def agrupa_por_nombre(files):
    by_name = defaultdict(list)
    for f in files:
        base = os.path.basename(f)
        by_name[base].append(f)
    return by_name

def escoge_moderno(paths):
    for kw in MODERN_KEYWORDS:
        for p in paths:
            if kw.lower() in p.lower():
                return p
    return sorted(paths, key=len)[0]

def genera_comandos_fusion(by_name):
    result = []
    for base, paths in by_name.items():
        if len(paths) > 1:
            moderno = escoge_moderno(paths)
            result.append(f"# {base} está duplicado en:")
            for p in paths:
                if p == moderno:
                    result.append(f"#   [ELEGIDO] {p}")
                else:
                    result.append(f"#   {p}")
            result.append(f"# Sugerencia: CONSERVA '{moderno}' y revisa/integra manualmente el resto en esta versión.\n")
            for p in paths:
                if p != moderno:
                    result.append(f"# Elimina: {p}")
            result.append("# ----\n")
        else:
            result.append(f"# {base} único en {paths[0]}\n")
    return "\n".join(result)

def main():
    if len(sys.argv) < 2:
        print("Uso: python fusionador_modulos.py arbol.txt")
        sys.exit(1)
    files = parse_arbol(sys.argv[1])
    by_name = agrupa_por_nombre(files)
    fusion_plan = genera_comandos_fusion(by_name)
    # Guardar en C:\Temp
    out_path = r"C:\Temp\fusion_plan.txt"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(fusion_plan)
    print(f"El plan de fusión ha sido guardado en {out_path}")

if __name__ == "__main__":
    main()