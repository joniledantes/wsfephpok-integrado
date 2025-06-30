###>>> VERSION: fusionador_Version3.py"""
###>>> VERSION: fusionador_Version1.pyimport os
###>>> VERSION: fusionador_Version2.py"""
###>>> VERSION: fusionador_Version4.py"""
###>>> VERSION: fusionador_Version5.py"""
###---
###>>> VERSION: fusionador_Version3.pyfusionador.py
###>>> VERSION: fusionador_Version1.pyimport shutil
###>>> VERSION: fusionador_Version2.pyfusionador.py
###>>> VERSION: fusionador_Version4.pyfusionador.py
###>>> VERSION: fusionador_Version5.pyfusionador.py
###---
###>>> VERSION: fusionador_Version3.pyScript para automatizar la fusión de archivos según arbol.txt y fusion_plan.txt
###>>> VERSION: fusionador_Version1.pyimport sys
###>>> VERSION: fusionador_Version2.pyScript para automatizar la fusión de archivos según arbol.txt y fusion_plan.txt
###>>> VERSION: fusionador_Version4.pyScript para automatizar la fusión de archivos según arbol.txt y fusion_plan.txt
###>>> VERSION: fusionador_Version5.pyScript para automatizar la fusión de archivos según arbol.txt y fusion_plan.txt
###---

###>>> VERSION: fusionador_Version3.py- Lee arbol.txt (árbol de archivos con rutas relativas o absolutas).
###>>> VERSION: fusionador_Version1.pyORIGEN = './origen'
###>>> VERSION: fusionador_Version2.py- Lee arbol.txt (árbol de archivos con rutas relativas o absolutas).
###>>> VERSION: fusionador_Version4.py- Busca recursivamente en C:/Users/Viaweb/Documents/GitHub todos los archivos marcados como [ELEGIDO] en fusion_plan.txt.
###>>> VERSION: fusionador_Version5.py- Busca recursivamente en C:/Users/Viaweb/Documents/GitHub todos los archivos marcados como [ELEGIDO] en fusion_plan.txt.
###---
###>>> VERSION: fusionador_Version3.py- Lee fusion_plan.txt (plan de archivos [ELEGIDO] a conservar).
###>>> VERSION: fusionador_Version1.pyDESTINO = './custom/wsfephpok'
###>>> VERSION: fusionador_Version2.py- Lee fusion_plan.txt (plan de archivos [ELEGIDO] a conservar).
###>>> VERSION: fusionador_Version4.py- Copia los archivos encontrados a c:/temp/wsfephp-vw (crea la carpeta si no existe).
###>>> VERSION: fusionador_Version5.py- Copia los archivos encontrados a c:/temp/wsfephp-vw (crea la carpeta si no existe).
###---
###>>> VERSION: fusionador_Version3.py- Copia todos los archivos marcados como [ELEGIDO] a una carpeta destino (por ejemplo, /custom/wsfephpok/).
###>>> VERSION: fusionador_Version1.pyARBOLE = 'arbol.txt'
###>>> VERSION: fusionador_Version2.py- Copia todos los archivos marcados como [ELEGIDO] a una carpeta destino (por ejemplo, /custom/wsfephpok/).
###>>> VERSION: fusionador_Version4.py- Genera un log de archivos copiados (fusion_log.txt) y los que requieren revisión manual (fusion_pendientes.txt).
###>>> VERSION: fusionador_Version5.py- Genera un log de archivos copiados (fusion_log.txt) y los que requieren revisión manual (fusion_pendientes.txt).
###---
###>>> VERSION: fusionador_Version3.py- Genera un log de archivos copiados y una lista de los que requieren revisión manual.
###>>> VERSION: fusionador_Version1.pyPLAN = 'plan_fusion.txt'
###>>> VERSION: fusionador_Version2.py- Genera un log de archivos copiados y una lista de los que requieren revisión manual.
###>>> VERSION: fusionador_Version4.py- Si hay conflictos de nombres, añade sufijo incremental (_1, _2, etc.).
###>>> VERSION: fusionador_Version5.py- Si hay conflictos de nombres, añade sufijo incremental (_1, _2, etc.).
###---
###>>> VERSION: fusionador_Version3.py- Si hay conflictos de nombres, añade sufijo incremental.
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py- Si hay conflictos de nombres, añade sufijo incremental.
###>>> VERSION: fusionador_Version4.py- Uso: python fusionador.py
###>>> VERSION: fusionador_Version5.py- Uso: python fusionador.py
###---
###>>> VERSION: fusionador_Version3.py- Uso: python fusionador.py ORIGEN DESTINO
###>>> VERSION: fusionador_Version1.pydef leer_arbol():
###>>> VERSION: fusionador_Version2.py- Uso: python fusionador.py ORIGEN DESTINO
###>>> VERSION: fusionador_Version4.py"""
###>>> VERSION: fusionador_Version5.py"""
###---
###>>> VERSION: fusionador_Version3.py  (por defecto ORIGEN="." y DESTINO="./custom/wsfephpok/")
###>>> VERSION: fusionador_Version1.py    with open(ARBOLE) as f:
###>>> VERSION: fusionador_Version2.py  (por defecto ORIGEN="." y DESTINO="./custom/wsfephpok/")
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py"""
###>>> VERSION: fusionador_Version1.py        return [line.strip() for line in f if line.strip()]
###>>> VERSION: fusionador_Version2.py"""
###>>> VERSION: fusionador_Version4.pyimport os
###>>> VERSION: fusionador_Version5.pyimport os
###---
###>>> VERSION: fusionador_Version3.py
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py
###>>> VERSION: fusionador_Version4.pyimport sys
###>>> VERSION: fusionador_Version5.pyimport sys
###---
###>>> VERSION: fusionador_Version3.pyimport os
###>>> VERSION: fusionador_Version1.pydef detectar_duplicados(archivos):
###>>> VERSION: fusionador_Version2.pyimport os
###>>> VERSION: fusionador_Version4.pyimport shutil
###>>> VERSION: fusionador_Version5.pyimport shutil
###---
###>>> VERSION: fusionador_Version3.pyimport sys
###>>> VERSION: fusionador_Version1.py    nombres = {}
###>>> VERSION: fusionador_Version2.pyimport sys
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.pyimport shutil
###>>> VERSION: fusionador_Version1.py    duplicados = []
###>>> VERSION: fusionador_Version2.pyimport shutil
###>>> VERSION: fusionador_Version4.pyARBOLE = "arbol.txt"
###>>> VERSION: fusionador_Version5.pyPLAN = "fusion_plan.txt"
###---
###>>> VERSION: fusionador_Version3.pyimport re
###>>> VERSION: fusionador_Version1.py    for path in archivos:
###>>> VERSION: fusionador_Version2.pyimport re
###>>> VERSION: fusionador_Version4.pyPLAN = "fusion_plan.txt"
###>>> VERSION: fusionador_Version5.pyORIGEN_ROOT = r"C:\Users\Viaweb\Documents\GitHub"
###---
###>>> VERSION: fusionador_Version3.py
###>>> VERSION: fusionador_Version1.py        nombre = os.path.basename(path)
###>>> VERSION: fusionador_Version2.py
###>>> VERSION: fusionador_Version4.pyORIGEN_ROOT = r"C:\Users\Viaweb\Documents\GitHub"
###>>> VERSION: fusionador_Version5.pyDESTINO = r"c:\temp\wsfephp-vw"
###---
###>>> VERSION: fusionador_Version3.pyARBOLE = "arbol.txt"
###>>> VERSION: fusionador_Version1.py        if nombre in nombres:
###>>> VERSION: fusionador_Version2.pyARBOLE = "arbol.txt"
###>>> VERSION: fusionador_Version4.pyDESTINO = r"c:\temp\wsfephp-vw"
###>>> VERSION: fusionador_Version5.pyLOG_COPIADOS = "fusion_log.txt"
###---
###>>> VERSION: fusionador_Version3.pyPLAN = "fusion_plan.txt"
###>>> VERSION: fusionador_Version1.py            duplicados.append((nombres[nombre], path))
###>>> VERSION: fusionador_Version2.pyPLAN = "fusion_plan.txt"
###>>> VERSION: fusionador_Version4.pyLOG_COPIADOS = "fusion_log.txt"
###>>> VERSION: fusionador_Version5.pyLOG_PENDIENTES = "fusion_pendientes.txt"
###---
###>>> VERSION: fusionador_Version3.pyDEFAULT_ORIGEN = "."
###>>> VERSION: fusionador_Version1.py        else:
###>>> VERSION: fusionador_Version2.pyDEFAULT_ORIGEN = "."
###>>> VERSION: fusionador_Version4.pyLOG_PENDIENTES = "fusion_pendientes.txt"
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.pyDEFAULT_DESTINO = "./custom/wsfephpok/"
###>>> VERSION: fusionador_Version1.py            nombres[nombre] = path
###>>> VERSION: fusionador_Version2.pyDEFAULT_DESTINO = "./custom/wsfephpok/"
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.pydef leer_elegidos(plan_path):
###---
###>>> VERSION: fusionador_Version3.pyLOG_COPIADOS = "fusion_log.txt"
###>>> VERSION: fusionador_Version1.py    return duplicados
###>>> VERSION: fusionador_Version2.pyLOG_COPIADOS = "fusion_log.txt"
###>>> VERSION: fusionador_Version4.pydef leer_elegidos(plan_path):
###>>> VERSION: fusionador_Version5.py    elegidos = set()
###---
###>>> VERSION: fusionador_Version3.pyLOG_PENDIENTES = "fusion_pendientes.txt"
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.pyLOG_PENDIENTES = "fusion_pendientes.txt"
###>>> VERSION: fusionador_Version4.py    elegidos = set()
###>>> VERSION: fusionador_Version5.py    pendientes = set()
###---
###>>> VERSION: fusionador_Version3.py
###>>> VERSION: fusionador_Version1.pydef generar_plan(archivos):
###>>> VERSION: fusionador_Version2.py
###>>> VERSION: fusionador_Version4.py    pendientes = set()
###>>> VERSION: fusionador_Version5.py    actual = None
###---
###>>> VERSION: fusionador_Version3.pydef leer_elegidos(plan_path):
###>>> VERSION: fusionador_Version1.py    comandos = []
###>>> VERSION: fusionador_Version2.pydef leer_elegidos(plan_path):
###>>> VERSION: fusionador_Version4.py    actual = None
###>>> VERSION: fusionador_Version5.py    with open(plan_path, encoding="utf-8", errors="ignore") as f:
###---
###>>> VERSION: fusionador_Version3.py    elegidos = set()
###>>> VERSION: fusionador_Version1.py    for path in archivos:
###>>> VERSION: fusionador_Version2.py    elegidos = set()
###>>> VERSION: fusionador_Version4.py    with open(plan_path, encoding="utf-8", errors="ignore") as f:
###>>> VERSION: fusionador_Version5.py        for line in f:
###---
###>>> VERSION: fusionador_Version3.py    pendientes = set()
###>>> VERSION: fusionador_Version1.py        nombre = os.path.basename(path)
###>>> VERSION: fusionador_Version2.py    pendientes = set()
###>>> VERSION: fusionador_Version4.py        for line in f:
###>>> VERSION: fusionador_Version5.py            if "[ELEGIDO]" in line:
###---
###>>> VERSION: fusionador_Version3.py    actual = None
###>>> VERSION: fusionador_Version1.py        destino = os.path.join(DESTINO, nombre)
###>>> VERSION: fusionador_Version2.py    actual = None
###>>> VERSION: fusionador_Version4.py            if "[ELEGIDO]" in line:
###>>> VERSION: fusionador_Version5.py                archivo = line.split("[ELEGIDO]")[-1].strip()
###---
###>>> VERSION: fusionador_Version3.py    with open(plan_path, encoding="utf-8", errors="ignore") as f:
###>>> VERSION: fusionador_Version1.py        comandos.append(f'cp "{path}" "{destino}"')
###>>> VERSION: fusionador_Version2.py    with open(plan_path, encoding="utf-8", errors="ignore") as f:
###>>> VERSION: fusionador_Version4.py                archivo = line.split("[ELEGIDO]")[-1].strip()
###>>> VERSION: fusionador_Version5.py                elegidos.add(archivo)
###---
###>>> VERSION: fusionador_Version3.py        for line in f:
###>>> VERSION: fusionador_Version1.py    return comandos
###>>> VERSION: fusionador_Version2.py        for line in f:
###>>> VERSION: fusionador_Version4.py                elegidos.add(archivo)
###>>> VERSION: fusionador_Version5.py                actual = archivo
###---
###>>> VERSION: fusionador_Version3.py            if "[ELEGIDO]" in line:
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py            if "[ELEGIDO]" in line:
###>>> VERSION: fusionador_Version4.py                actual = archivo
###>>> VERSION: fusionador_Version5.py            elif "Sugerencia" in line or "revisa/integra" in line or "revisar/integra" in line:
###---
###>>> VERSION: fusionador_Version3.py                # Ejemplo: "   [ELEGIDO] wsfe_doli.php"
###>>> VERSION: fusionador_Version1.pydef main(apply=False):
###>>> VERSION: fusionador_Version2.py                # Ejemplo: "   [ELEGIDO] wsfe_doli.php"
###>>> VERSION: fusionador_Version4.py            elif "Sugerencia" in line or "revisa/integra" in line or "revisar/integra" in line:
###>>> VERSION: fusionador_Version5.py                if actual:
###---
###>>> VERSION: fusionador_Version3.py                archivo = line.split("[ELEGIDO]")[-1].strip()
###>>> VERSION: fusionador_Version1.py    archivos = leer_arbol()
###>>> VERSION: fusionador_Version2.py                archivo = line.split("[ELEGIDO]")[-1].strip()
###>>> VERSION: fusionador_Version4.py                if actual:
###>>> VERSION: fusionador_Version5.py                    pendientes.add(actual)
###---
###>>> VERSION: fusionador_Version3.py                elegidos.add(archivo)
###>>> VERSION: fusionador_Version1.py    duplicados = detectar_duplicados(archivos)
###>>> VERSION: fusionador_Version2.py                elegidos.add(archivo)
###>>> VERSION: fusionador_Version4.py                    pendientes.add(actual)
###>>> VERSION: fusionador_Version5.py    return elegidos, pendientes
###---
###>>> VERSION: fusionador_Version3.py                actual = archivo
###>>> VERSION: fusionador_Version1.py    with open(PLAN, 'w') as f:
###>>> VERSION: fusionador_Version2.py                actual = archivo
###>>> VERSION: fusionador_Version4.py    return elegidos, pendientes
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py            elif "Sugerencia" in line or "revisa/integra" in line or "revisar/integra" in line:
###>>> VERSION: fusionador_Version1.py        f.write('# Duplicados encontrados:\n')
###>>> VERSION: fusionador_Version2.py            elif "Sugerencia" in line or "revisa/integra" in line or "revisar/integra" in line:
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.pydef buscar_archivos(raiz, nombres):
###---
###>>> VERSION: fusionador_Version3.py                if actual:
###>>> VERSION: fusionador_Version1.py        for a, b in duplicados:
###>>> VERSION: fusionador_Version2.py                if actual:
###>>> VERSION: fusionador_Version4.pydef buscar_archivos(raiz, nombres):
###>>> VERSION: fusionador_Version5.py    encontrados = {nombre: [] for nombre in nombres}
###---
###>>> VERSION: fusionador_Version3.py                    pendientes.add(actual)
###>>> VERSION: fusionador_Version1.py            f.write(f'DUPLICADO: {a} <-> {b}\n')
###>>> VERSION: fusionador_Version2.py                    pendientes.add(actual)
###>>> VERSION: fusionador_Version4.py    encontrados = {nombre: [] for nombre in nombres}
###>>> VERSION: fusionador_Version5.py    for root, dirs, files in os.walk(raiz):
###---
###>>> VERSION: fusionador_Version3.py    return elegidos, pendientes
###>>> VERSION: fusionador_Version1.py        f.write('\n# Plan de copiado:\n')
###>>> VERSION: fusionador_Version2.py    return elegidos, pendientes
###>>> VERSION: fusionador_Version4.py    for root, dirs, files in os.walk(raiz):
###>>> VERSION: fusionador_Version5.py        for file in files:
###---
###>>> VERSION: fusionador_Version3.py
###>>> VERSION: fusionador_Version1.py        for cmd in generar_plan(archivos):
###>>> VERSION: fusionador_Version2.py
###>>> VERSION: fusionador_Version4.py        for file in files:
###>>> VERSION: fusionador_Version5.py            if file in nombres:
###---
###>>> VERSION: fusionador_Version3.pydef listar_rutas_arbol(arbol_path):
###>>> VERSION: fusionador_Version1.py            f.write(cmd + '\n')
###>>> VERSION: fusionador_Version2.pydef listar_rutas_arbol(arbol_path):
###>>> VERSION: fusionador_Version4.py            if file in nombres:
###>>> VERSION: fusionador_Version5.py                encontrados[file].append(os.path.join(root, file))
###---
###>>> VERSION: fusionador_Version3.py    rutas = {}
###>>> VERSION: fusionador_Version1.py    if apply:
###>>> VERSION: fusionador_Version2.py    rutas = {}
###>>> VERSION: fusionador_Version4.py                encontrados[file].append(os.path.join(root, file))
###>>> VERSION: fusionador_Version5.py    return encontrados
###---
###>>> VERSION: fusionador_Version3.py    with open(arbol_path, encoding="utf-8", errors="ignore") as f:
###>>> VERSION: fusionador_Version1.py        os.makedirs(DESTINO, exist_ok=True)
###>>> VERSION: fusionador_Version2.py    with open(arbol_path, encoding="utf-8", errors="ignore") as f:
###>>> VERSION: fusionador_Version4.py    return encontrados
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py        for line in f:
###>>> VERSION: fusionador_Version1.py        for path in archivos:
###>>> VERSION: fusionador_Version2.py        for line in f:
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.pydef copiar_archivos(encontrados, destino):
###---
###>>> VERSION: fusionador_Version3.py            # Buscar líneas con una ruta de archivo
###>>> VERSION: fusionador_Version1.py            nombre = os.path.basename(path)
###>>> VERSION: fusionador_Version2.py            # Buscar líneas con una ruta de archivo
###>>> VERSION: fusionador_Version4.pydef copiar_archivos(encontrados, destino):
###>>> VERSION: fusionador_Version5.py    copiados = []
###---
###>>> VERSION: fusionador_Version3.py            match = re.search(r'([A-Za-z]:)?[\\/][^:*?"<>|\r\n]+?\.\w+', line)
###>>> VERSION: fusionador_Version1.py            destino = os.path.join(DESTINO, nombre)
###>>> VERSION: fusionador_Version2.py            match = re.search(r'([A-Za-z]:)?[\\/][^:*?"<>|\r\n]+?\.\w+', line)
###>>> VERSION: fusionador_Version4.py    copiados = []
###>>> VERSION: fusionador_Version5.py    conflictos = []
###---
###>>> VERSION: fusionador_Version3.py            if match:
###>>> VERSION: fusionador_Version1.py            shutil.copy2(path, destino)
###>>> VERSION: fusionador_Version2.py            if match:
###>>> VERSION: fusionador_Version4.py    conflictos = []
###>>> VERSION: fusionador_Version5.py    os.makedirs(destino, exist_ok=True)
###---
###>>> VERSION: fusionador_Version3.py                ruta = line.strip().replace("│", "").replace("�", "").replace("├", "").replace("─", "").replace("└", "").replace(" ", "")
###>>> VERSION: fusionador_Version1.py        print(f"Archivos copiados a {DESTINO}")
###>>> VERSION: fusionador_Version2.py                ruta = line.strip().replace("│", "").replace("�", "").replace("├", "").replace("─", "").replace("└", "").replace(" ", "")
###>>> VERSION: fusionador_Version4.py    os.makedirs(destino, exist_ok=True)
###>>> VERSION: fusionador_Version5.py    for nombre, rutas in encontrados.items():
###---
###>>> VERSION: fusionador_Version3.py                nombre = os.path.basename(ruta)
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py                nombre = os.path.basename(ruta)
###>>> VERSION: fusionador_Version4.py    for nombre, rutas in encontrados.items():
###>>> VERSION: fusionador_Version5.py        if rutas:
###---
###>>> VERSION: fusionador_Version3.py                if nombre not in rutas:
###>>> VERSION: fusionador_Version1.pyif __name__ == '__main__':
###>>> VERSION: fusionador_Version2.py                if nombre not in rutas:
###>>> VERSION: fusionador_Version4.py        if rutas:
###>>> VERSION: fusionador_Version5.py            # Si hay varias rutas para el mismo archivo, se copian todas con sufijo incremental
###---
###>>> VERSION: fusionador_Version3.py                    rutas[nombre] = []
###>>> VERSION: fusionador_Version1.py    apply = '--apply' in sys.argv
###>>> VERSION: fusionador_Version2.py                    rutas[nombre] = []
###>>> VERSION: fusionador_Version4.py            # Si hay varias rutas para el mismo archivo, se copian todas con sufijo incremental
###>>> VERSION: fusionador_Version5.py            for idx, ruta_abs in enumerate(rutas):
###---
###>>> VERSION: fusionador_Version3.py                rutas[nombre].append(ruta)
###>>> VERSION: fusionador_Version1.py    main(apply)
###>>> VERSION: fusionador_Version2.py                rutas[nombre].append(ruta)
###>>> VERSION: fusionador_Version4.py            for idx, ruta_abs in enumerate(rutas):
###>>> VERSION: fusionador_Version5.py                nombre_final = nombre if idx == 0 else f"{os.path.splitext(nombre)[0]}_{idx}{os.path.splitext(nombre)[1]}"
###---
###>>> VERSION: fusionador_Version3.py    return rutas
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py    return rutas
###>>> VERSION: fusionador_Version4.py                nombre_final = nombre if idx == 0 else f"{os.path.splitext(nombre)[0]}_{idx}{os.path.splitext(nombre)[1]}"
###>>> VERSION: fusionador_Version5.py                dest_file = os.path.join(destino, nombre_final)
###---
###>>> VERSION: fusionador_Version3.py
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py
###>>> VERSION: fusionador_Version4.py                dest_file = os.path.join(destino, nombre_final)
###>>> VERSION: fusionador_Version5.py                shutil.copy2(ruta_abs, dest_file)
###---
###>>> VERSION: fusionador_Version3.pydef copiar_archivos(elegidos, rutas, origen, destino):
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.pydef copiar_archivos(elegidos, rutas, origen, destino):
###>>> VERSION: fusionador_Version4.py                shutil.copy2(ruta_abs, dest_file)
###>>> VERSION: fusionador_Version5.py                copiados.append(dest_file)
###---
###>>> VERSION: fusionador_Version3.py    copiados = []
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py    copiados = []
###>>> VERSION: fusionador_Version4.py                copiados.append(dest_file)
###>>> VERSION: fusionador_Version5.py                if idx > 0:
###---
###>>> VERSION: fusionador_Version3.py    conflictos = []
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py    conflictos = []
###>>> VERSION: fusionador_Version4.py                if idx > 0:
###>>> VERSION: fusionador_Version5.py                    conflictos.append(dest_file)
###---
###>>> VERSION: fusionador_Version3.py    os.makedirs(destino, exist_ok=True)
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py    os.makedirs(destino, exist_ok=True)
###>>> VERSION: fusionador_Version4.py                    conflictos.append(dest_file)
###>>> VERSION: fusionador_Version5.py    return copiados, conflictos
###---
###>>> VERSION: fusionador_Version3.py    for nombre in elegidos:
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py    for nombre in elegidos:
###>>> VERSION: fusionador_Version4.py    return copiados, conflictos
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py        if nombre in rutas:
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py        if nombre in rutas:
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.pydef main():
###---
###>>> VERSION: fusionador_Version3.py            for idx, ruta_rel in enumerate(rutas[nombre]):
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py            for idx, ruta_rel in enumerate(rutas[nombre]):
###>>> VERSION: fusionador_Version4.pydef main():
###>>> VERSION: fusionador_Version5.py    elegidos, pendientes = leer_elegidos(PLAN)
###---
###>>> VERSION: fusionador_Version3.py                ruta_abs = os.path.join(origen, ruta_rel) if not os.path.isabs(ruta_rel) else ruta_rel
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py                ruta_abs = os.path.join(origen, ruta_rel) if not os.path.isabs(ruta_rel) else ruta_rel
###>>> VERSION: fusionador_Version4.py    elegidos, pendientes = leer_elegidos(PLAN)
###>>> VERSION: fusionador_Version5.py    encontrados = buscar_archivos(ORIGEN_ROOT, elegidos)
###---
###>>> VERSION: fusionador_Version3.py                if not os.path.isfile(ruta_abs):
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py                if not os.path.isfile(ruta_abs):
###>>> VERSION: fusionador_Version4.py    encontrados = buscar_archivos(ORIGEN_ROOT, elegidos)
###>>> VERSION: fusionador_Version5.py    copiados, conflictos = copiar_archivos(encontrados, DESTINO)
###---
###>>> VERSION: fusionador_Version3.py                    continue
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py                    continue
###>>> VERSION: fusionador_Version4.py    copiados, conflictos = copiar_archivos(encontrados, DESTINO)
###>>> VERSION: fusionador_Version5.py    with open(LOG_COPIADOS, "w", encoding="utf-8") as f:
###---
###>>> VERSION: fusionador_Version3.py                nombre_final = nombre
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py                nombre_final = nombre
###>>> VERSION: fusionador_Version4.py    with open(LOG_COPIADOS, "w", encoding="utf-8") as f:
###>>> VERSION: fusionador_Version5.py        f.write("# Archivos copiados automáticamente\n")
###---
###>>> VERSION: fusionador_Version3.py                dest_file = os.path.join(destino, nombre_final)
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py                dest_file = os.path.join(destino, nombre_final)
###>>> VERSION: fusionador_Version4.py        f.write("# Archivos copiados automáticamente\n")
###>>> VERSION: fusionador_Version5.py        for path in copiados:
###---
###>>> VERSION: fusionador_Version3.py                # Si ya existe, agrega sufijo incremental
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py                # Si ya existe, agrega sufijo incremental
###>>> VERSION: fusionador_Version4.py        for path in copiados:
###>>> VERSION: fusionador_Version5.py            f.write(path + "\n")
###---
###>>> VERSION: fusionador_Version3.py                suf = 1
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py                suf = 1
###>>> VERSION: fusionador_Version4.py            f.write(path + "\n")
###>>> VERSION: fusionador_Version5.py        if conflictos:
###---
###>>> VERSION: fusionador_Version3.py                while os.path.exists(dest_file):
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py                while os.path.exists(dest_file):
###>>> VERSION: fusionador_Version4.py        if conflictos:
###>>> VERSION: fusionador_Version5.py            f.write("\n# Archivos con conflictos de nombre (sufijo incremental):\n")
###---
###>>> VERSION: fusionador_Version3.py                    nombre_final = f"{os.path.splitext(nombre)[0]}_{suf}{os.path.splitext(nombre)[1]}"
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py                    nombre_final = f"{os.path.splitext(nombre)[0]}_{suf}{os.path.splitext(nombre)[1]}"
###>>> VERSION: fusionador_Version4.py            f.write("\n# Archivos con conflictos de nombre (sufijo incremental):\n")
###>>> VERSION: fusionador_Version5.py            for path in conflictos:
###---
###>>> VERSION: fusionador_Version3.py                    dest_file = os.path.join(destino, nombre_final)
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py                    dest_file = os.path.join(destino, nombre_final)
###>>> VERSION: fusionador_Version4.py            for path in conflictos:
###>>> VERSION: fusionador_Version5.py                f.write(path + "\n")
###---
###>>> VERSION: fusionador_Version3.py                    suf += 1
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py                    suf += 1
###>>> VERSION: fusionador_Version4.py                f.write(path + "\n")
###>>> VERSION: fusionador_Version5.py    with open(LOG_PENDIENTES, "w", encoding="utf-8") as f:
###---
###>>> VERSION: fusionador_Version3.py                shutil.copy2(ruta_abs, dest_file)
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py                shutil.copy2(ruta_abs, dest_file)
###>>> VERSION: fusionador_Version4.py    with open(LOG_PENDIENTES, "w", encoding="utf-8") as f:
###>>> VERSION: fusionador_Version5.py        f.write("# Archivos marcados para revisión/integración manual\n")
###---
###>>> VERSION: fusionador_Version3.py                copiados.append(dest_file)
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py                copiados.append(dest_file)
###>>> VERSION: fusionador_Version4.py        f.write("# Archivos marcados para revisión/integración manual\n")
###>>> VERSION: fusionador_Version5.py        for p in pendientes:
###---
###>>> VERSION: fusionador_Version3.py                if suf > 1:
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py                if suf > 1:
###>>> VERSION: fusionador_Version4.py        for p in pendientes:
###>>> VERSION: fusionador_Version5.py            f.write(p + "\n")
###---
###>>> VERSION: fusionador_Version3.py                    conflictos.append(dest_file)
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py                    conflictos.append(dest_file)
###>>> VERSION: fusionador_Version4.py            f.write(p + "\n")
###>>> VERSION: fusionador_Version5.py    print(f"COPIA COMPLETA: {len(copiados)} archivos copiados a {DESTINO}")
###---
###>>> VERSION: fusionador_Version3.py                break  # Solo copia una instancia por archivo elegido
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py                break  # Solo copia una instancia por archivo elegido
###>>> VERSION: fusionador_Version4.py    print(f"COPIA COMPLETA: {len(copiados)} archivos copiados a {DESTINO}")
###>>> VERSION: fusionador_Version5.py    print(f"Revisa '{LOG_PENDIENTES}' para ver archivos que requieren integración manual.")
###---
###>>> VERSION: fusionador_Version3.py    return copiados, conflictos
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py    return copiados, conflictos
###>>> VERSION: fusionador_Version4.py    print(f"Revisa '{LOG_PENDIENTES}' para ver archivos que requieren integración manual.")
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.pyif __name__ == "__main__":
###---
###>>> VERSION: fusionador_Version3.pydef main():
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.pydef main():
###>>> VERSION: fusionador_Version4.pyif __name__ == "__main__":
###>>> VERSION: fusionador_Version5.py    main()
###---
###>>> VERSION: fusionador_Version3.py    origen = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ORIGEN
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py    origen = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ORIGEN
###>>> VERSION: fusionador_Version4.py    main()
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py    destino = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_DESTINO
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py    destino = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_DESTINO
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py    elegidos, pendientes = leer_elegidos(PLAN)
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py    elegidos, pendientes = leer_elegidos(PLAN)
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py    rutas = listar_rutas_arbol(ARBOLE)
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py    rutas = listar_rutas_arbol(ARBOLE)
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py    copiados, conflictos = copiar_archivos(elegidos, rutas, origen, destino)
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py    copiados, conflictos = copiar_archivos(elegidos, rutas, origen, destino)
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py    with open(LOG_COPIADOS, "w", encoding="utf-8") as f:
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py    with open(LOG_COPIADOS, "w", encoding="utf-8") as f:
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py        f.write("# Archivos copiados automáticamente\n")
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py        f.write("# Archivos copiados automáticamente\n")
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py        for path in copiados:
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py        for path in copiados:
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py            f.write(path + "\n")
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py            f.write(path + "\n")
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py        if conflictos:
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py        if conflictos:
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py            f.write("\n# Archivos con conflictos de nombre (sufijo incremental):\n")
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py            f.write("\n# Archivos con conflictos de nombre (sufijo incremental):\n")
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py            for path in conflictos:
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py            for path in conflictos:
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py                f.write(path + "\n")
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py                f.write(path + "\n")
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py    with open(LOG_PENDIENTES, "w", encoding="utf-8") as f:
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py    with open(LOG_PENDIENTES, "w", encoding="utf-8") as f:
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py        f.write("# Archivos marcados para revisión/integración manual\n")
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py        f.write("# Archivos marcados para revisión/integración manual\n")
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py        for p in pendientes:
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py        for p in pendientes:
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py            f.write(p + "\n")
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py            f.write(p + "\n")
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py    print(f"COPIA COMPLETA: {len(copiados)} archivos copiados a {destino}")
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py    print(f"COPIA COMPLETA: {len(copiados)} archivos copiados a {destino}")
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py    print(f"Revisa '{LOG_PENDIENTES}' para ver archivos que requieren integración manual.")
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py    print(f"Revisa '{LOG_PENDIENTES}' para ver archivos que requieren integración manual.")
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---

###>>> VERSION: fusionador_Version3.pyif __name__ == "__main__":
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.pyif __name__ == "__main__":
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
###>>> VERSION: fusionador_Version3.py    main()
###>>> VERSION: fusionador_Version1.py
###>>> VERSION: fusionador_Version2.py    main()
###>>> VERSION: fusionador_Version4.py
###>>> VERSION: fusionador_Version5.py
###---
