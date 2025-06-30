import os
import shutil
import sys

ORIGEN = './origen'
DESTINO = './custom/wsfephpok'
ARBOLE = 'arbol.txt'
PLAN = 'plan_fusion.txt'

def leer_arbol():
    with open(ARBOLE) as f:
        return [line.strip() for line in f if line.strip()]

def detectar_duplicados(archivos):
    nombres = {}
    duplicados = []
    for path in archivos:
        nombre = os.path.basename(path)
        if nombre in nombres:
            duplicados.append((nombres[nombre], path))
        else:
            nombres[nombre] = path
    return duplicados

def generar_plan(archivos):
    comandos = []
    for path in archivos:
        nombre = os.path.basename(path)
        destino = os.path.join(DESTINO, nombre)
        comandos.append(f'cp "{path}" "{destino}"')
    return comandos

def main(apply=False):
    archivos = leer_arbol()
    duplicados = detectar_duplicados(archivos)
    with open(PLAN, 'w') as f:
        f.write('# Duplicados encontrados:\n')
        for a, b in duplicados:
            f.write(f'DUPLICADO: {a} <-> {b}\n')
        f.write('\n# Plan de copiado:\n')
        for cmd in generar_plan(archivos):
            f.write(cmd + '\n')
    if apply:
        os.makedirs(DESTINO, exist_ok=True)
        for path in archivos:
            nombre = os.path.basename(path)
            destino = os.path.join(DESTINO, nombre)
            shutil.copy2(path, destino)
        print(f"Archivos copiados a {DESTINO}")

if __name__ == '__main__':
    apply = '--apply' in sys.argv
    main(apply)