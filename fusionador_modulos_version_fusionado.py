"""
fusionador_modulos.py

Script para analizar un árbol de directorios (como arbol.txt) y generar comandos para fusionar archivos/clases/plantillas duplicadas en una única ubicación limpia y moderna.
- Detecta duplicados por nombre.
- Prioriza versiones modernas (por nombre, por ubicación, o puedes agregar reglas).
- Genera comandos de fusión/migración.
- Pensado para proyectos Dolibarr/AFIP WSFE pero adaptable.

Uso:
    python fusionador_modulos.py arbol.txt > fusion_plan.txt

Requiere: Python 3.x
"""

import sys
import os
import re
from collections import defaultdict

# Configuración: patrones de archivos relevantes por tipo
PATTERNS = [
    re.compile(r'\.php$'),
    re.compile(r'\.tpl\.php$'),
    re.compile(r'\.js$'),
    re.compile(r'\.lang$'),
    re.compile(r'\.pdf$'),
]

# Criterios de modernidad (puedes ampliar)
MODERN_KEYWORDS = ['FINAL', 'v2', '2104', 'sept24', '3.php', '4.php']

def parse_arbol(path):
    """
    Obtiene todas las rutas de archivo del arbol.txt
    """
    files = []
    with open(path, encoding='utf-8', errors='ignore') as f:
        for line in f:
            # Limpiar y detectar líneas de archivos (las que terminan en .php, .js, etc)
            l = line.strip(' \r\n')
            if l.startswith('�') or l.startswith('│') or not l:
                continue
            if any(pat.search(l) for pat in PATTERNS):
                # Normaliza separador de directorio
                l = l.replace('�', '').replace('├', '').replace('─', '').replace('│', '').replace('└', '')
                l = l.strip()
                files.append(l)
    return files

def agrupa_por_nombre(files):
    """
    Agrupa rutas de archivo por nombre base
    """
    by_name = defaultdict(list)
    for f in files:
        base = os.path.basename(f)
        by_name[base].append(f)
    return by_name

def escoge_moderno(paths):
    """
    Elige la versión más moderna de una lista de rutas.
    """
    # Prioridad por palabras clave de modernidad
    for kw in MODERN_KEYWORDS:
        for p in paths:
            if kw.lower() in p.lower():
                return p
    # Si no hay clave, prioriza el path más corto (normalmente más "top-level" o menos backup)
    return sorted(paths, key=len)[0]

def genera_comandos_fusion(by_name):
    """
    Genera comandos para fusionar los duplicados.
    """
    for base, paths in by_name.items():
        if len(paths) > 1:
            moderno = escoge_moderno(paths)
            print(f"# {base} está duplicado en:")
            for p in paths:
                if p == moderno:
                    print(f"#   [ELEGIDO] {p}")
                else:
                    print(f"#   {p}")
            print(f"# Sugerencia: CONSERVA '{moderno}' y revisa/integra manualmente el resto en esta versión.")
            print()
            for p in paths:
                if p != moderno:
                    print(f"# Elimina: {p}")
            print("# ----\n")
        else:
            # No duplicado, solo muestra
            print(f"# {base} único en {paths[0]}")
            print()

def main():
    if len(sys.argv) < 2:
        print("Uso: python fusionador_modulos.py arbol.txt")
        sys.exit(1)
    files = parse_arbol(sys.argv[1])
    by_name = agrupa_por_nombre(files)
    genera_comandos_fusion(by_name)

if __name__ == "__main__":
    main()