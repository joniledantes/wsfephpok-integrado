import os
import json
import csv
###>>> VERSION: tree.pyimport zipfile
###>>> VERSION: tree2.py
###---
###>>> VERSION: tree.py
###>>> VERSION: tree2.py# Ruta base desde donde empieza a recorrer
###---
###>>> VERSION: tree.py# Cambiá esta ruta a una que seguro exista y tengas permisos, por ejemplo C:\Temp
###>>> VERSION: tree2.pyBASE_DIR = "."
###---
###>>> VERSION: tree.pyEXPORT_BASE_DIR = r"C:\Temp"
###>>> VERSION: tree2.py
###---
###>>> VERSION: tree.pyEXPORT_DIR = os.path.join(EXPORT_BASE_DIR, "export_tree")
###>>> VERSION: tree2.py# TXT - estilo árbol visual
###---
###>>> VERSION: tree.py
###>>> VERSION: tree2.pydef print_tree_txt(start_path, prefix="", file=None):
###---
###>>> VERSION: tree.py# Ruta base para escanear, por defecto carpeta actual
###>>> VERSION: tree2.py    try:
###---
###>>> VERSION: tree.pyBASE_DIR = "."
###>>> VERSION: tree2.py        items = sorted(os.listdir(start_path))
###---
###>>> VERSION: tree.py
###>>> VERSION: tree2.py    except PermissionError:
###---
###>>> VERSION: tree.pydef print_tree_txt(start_path, prefix="", file=None):
###>>> VERSION: tree2.py        return
###---
###>>> VERSION: tree.py    try:
###>>> VERSION: tree2.py    for index, item in enumerate(items):
###---
###>>> VERSION: tree.py        items = sorted(os.listdir(start_path))
###>>> VERSION: tree2.py        path = os.path.join(start_path, item)
###---
###>>> VERSION: tree.py    except PermissionError:
###>>> VERSION: tree2.py        is_last = index == len(items) - 1
###---
###>>> VERSION: tree.py        return
###>>> VERSION: tree2.py        connector = "└── " if is_last else "├── "
###---
###>>> VERSION: tree.py    for index, item in enumerate(items):
###>>> VERSION: tree2.py        line = prefix + connector + item
###---
###>>> VERSION: tree.py        path = os.path.join(start_path, item)
###>>> VERSION: tree2.py        if file:
###---
###>>> VERSION: tree.py        is_last = index == len(items) - 1
###>>> VERSION: tree2.py            file.write(line + "\n")
###---
###>>> VERSION: tree.py        connector = "└── " if is_last else "├── "
###>>> VERSION: tree2.py        if os.path.isdir(path):
###---
###>>> VERSION: tree.py        line = prefix + connector + item
###>>> VERSION: tree2.py            new_prefix = prefix + ("    " if is_last else "│   ")
###---
###>>> VERSION: tree.py        if file:
###>>> VERSION: tree2.py            print_tree_txt(path, new_prefix, file)
###---
###>>> VERSION: tree.py            file.write(line + "\n")
###>>> VERSION: tree2.py
###---
###>>> VERSION: tree.py        if os.path.isdir(path):
###>>> VERSION: tree2.py# CSV - tipo y ruta
###---
###>>> VERSION: tree.py            new_prefix = prefix + ("    " if is_last else "│   ")
###>>> VERSION: tree2.pydef export_csv(start_path, file):
###---
###>>> VERSION: tree.py            print_tree_txt(path, new_prefix, file)
###>>> VERSION: tree2.py    writer = csv.writer(file)
###---
###>>> VERSION: tree.py
###>>> VERSION: tree2.py    writer.writerow(["Tipo", "Ruta"])
###---
###>>> VERSION: tree.pydef export_csv(start_path, file):
###>>> VERSION: tree2.py    for root, dirs, files in os.walk(start_path):
###---
###>>> VERSION: tree.py    writer = csv.writer(file)
###>>> VERSION: tree2.py        for d in dirs:
###---
###>>> VERSION: tree.py    writer.writerow(["Tipo", "Ruta"])
###>>> VERSION: tree2.py            writer.writerow(["Carpeta", os.path.join(root, d)])
###---
###>>> VERSION: tree.py    for root, dirs, files in os.walk(start_path):
###>>> VERSION: tree2.py        for f in files:
###---
###>>> VERSION: tree.py        for d in dirs:
###>>> VERSION: tree2.py            writer.writerow(["Archivo", os.path.join(root, f)])
###---
###>>> VERSION: tree.py            writer.writerow(["Carpeta", os.path.join(root, d)])
###>>> VERSION: tree2.py
###---
###>>> VERSION: tree.py        for f in files:
###>>> VERSION: tree2.py# JSON - árbol estructurado
###---
###>>> VERSION: tree.py            writer.writerow(["Archivo", os.path.join(root, f)])
###>>> VERSION: tree2.pydef build_json_tree(path):
###---
###>>> VERSION: tree.py
###>>> VERSION: tree2.py    node = {"name": os.path.basename(path), "children": []}
###---
###>>> VERSION: tree.pydef build_json_tree(path):
###>>> VERSION: tree2.py    try:
###---
###>>> VERSION: tree.py    node = {"name": os.path.basename(path), "children": []}
###>>> VERSION: tree2.py        for item in sorted(os.listdir(path)):
###---
###>>> VERSION: tree.py    try:
###>>> VERSION: tree2.py            full_path = os.path.join(path, item)
###---
###>>> VERSION: tree.py        for item in sorted(os.listdir(path)):
###>>> VERSION: tree2.py            if os.path.isdir(full_path):
###---
###>>> VERSION: tree.py            full_path = os.path.join(path, item)
###>>> VERSION: tree2.py                node["children"].append(build_json_tree(full_path))
###---
###>>> VERSION: tree.py            if os.path.isdir(full_path):
###>>> VERSION: tree2.py            else:
###---
###>>> VERSION: tree.py                node["children"].append(build_json_tree(full_path))
###>>> VERSION: tree2.py                node["children"].append({"name": item})
###---
###>>> VERSION: tree.py            else:
###>>> VERSION: tree2.py    except PermissionError:
###---
###>>> VERSION: tree.py                node["children"].append({"name": item})
###>>> VERSION: tree2.py        pass
###---
###>>> VERSION: tree.py    except PermissionError:
###>>> VERSION: tree2.py    return node
###---
###>>> VERSION: tree.py        pass
###>>> VERSION: tree2.py
###---
###>>> VERSION: tree.py    return node
###>>> VERSION: tree2.pydef generar_reportes(base_dir):
###---
###>>> VERSION: tree.py
###>>> VERSION: tree2.py    export_dir = os.path.abspath("export_tree")
###---
###>>> VERSION: tree.pydef comprimir_resultado(export_dir):
###>>> VERSION: tree2.py    os.makedirs(export_dir, exist_ok=True)  # crea carpeta si no existe
###---
###>>> VERSION: tree.py    zip_path = os.path.join(export_dir, "estructura_completa.zip")
###>>> VERSION: tree2.py
###---
###>>> VERSION: tree.py    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
###>>> VERSION: tree2.py    txt_path = os.path.join(export_dir, "tree.txt")
###---
###>>> VERSION: tree.py        for filename in ["tree.txt", "tree.csv", "tree.json"]:
###>>> VERSION: tree2.py    csv_path = os.path.join(export_dir, "tree.csv")
###---
###>>> VERSION: tree.py            full_path = os.path.join(export_dir, filename)
###>>> VERSION: tree2.py    json_path = os.path.join(export_dir, "tree.json")
###---
###>>> VERSION: tree.py            zipf.write(full_path, arcname=filename)
###>>> VERSION: tree2.py
###---
###>>> VERSION: tree.py    print(f"📦 Archivo comprimido: {zip_path}")
###>>> VERSION: tree2.py    with open(txt_path, "w", encoding="utf-8") as txt_file:
###---
###>>> VERSION: tree.py
###>>> VERSION: tree2.py        print_tree_txt(base_dir, file=txt_file)
###---
###>>> VERSION: tree.pydef generar_reportes(base_dir):
###>>> VERSION: tree2.py
###---
###>>> VERSION: tree.py    print(f"Intentando crear carpeta en: {EXPORT_DIR}")
###>>> VERSION: tree2.py    with open(csv_path, "w", newline='', encoding="utf-8") as csv_file:
###---
###>>> VERSION: tree.py    os.makedirs(EXPORT_DIR, exist_ok=True)
###>>> VERSION: tree2.py        export_csv(base_dir, csv_file)
###---

###>>> VERSION: tree.py    txt_path = os.path.join(EXPORT_DIR, "tree.txt")
###>>> VERSION: tree2.py    tree = build_json_tree(base_dir)
###---
###>>> VERSION: tree.py    csv_path = os.path.join(EXPORT_DIR, "tree.csv")
###>>> VERSION: tree2.py    with open(json_path, "w", encoding="utf-8") as json_file:
###---
###>>> VERSION: tree.py    json_path = os.path.join(EXPORT_DIR, "tree.json")
###>>> VERSION: tree2.py        json.dump(tree, json_file, indent=2)
###---

###>>> VERSION: tree.py    with open(txt_path, "w", encoding="utf-8") as txt_file:
###>>> VERSION: tree2.py    print("✔️ Archivos generados en carpeta 'export_tree':")
###---
###>>> VERSION: tree.py        print_tree_txt(base_dir, file=txt_file)
###>>> VERSION: tree2.py    print(f"- {txt_path}")
###---
###>>> VERSION: tree.py
###>>> VERSION: tree2.py    print(f"- {csv_path}")
###---
###>>> VERSION: tree.py    with open(csv_path, "w", newline='', encoding="utf-8") as csv_file:
###>>> VERSION: tree2.py    print(f"- {json_path}")
###---
###>>> VERSION: tree.py        export_csv(base_dir, csv_file)
###>>> VERSION: tree2.py
###---
###>>> VERSION: tree.py
###>>> VERSION: tree2.py# Ejecutar
###---
###>>> VERSION: tree.py    tree = build_json_tree(base_dir)
###>>> VERSION: tree2.pyif __name__ == "__main__":
###---
###>>> VERSION: tree.py    with open(json_path, "w", encoding="utf-8") as json_file:
###>>> VERSION: tree2.py    generar_reportes(BASE_DIR)
###---
###>>> VERSION: tree.py        json.dump(tree, json_file, indent=2)
###>>> VERSION: tree2.py
###---

###>>> VERSION: tree.py    print("✔️ Archivos generados en carpeta:")
###>>> VERSION: tree2.py
###---
###>>> VERSION: tree.py    print(f"- {txt_path}")
###>>> VERSION: tree2.py
###---
###>>> VERSION: tree.py    print(f"- {csv_path}")
###>>> VERSION: tree2.py
###---
###>>> VERSION: tree.py    print(f"- {json_path}")
###>>> VERSION: tree2.py
###---

###>>> VERSION: tree.py    comprimir_resultado(EXPORT_DIR)
###>>> VERSION: tree2.py
###---

###>>> VERSION: tree.pyif __name__ == "__main__":
###>>> VERSION: tree2.py
###---
###>>> VERSION: tree.py    generar_reportes(BASE_DIR)
###>>> VERSION: tree2.py
###---
