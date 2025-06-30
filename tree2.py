import os
import json
import csv

# Ruta base desde donde empieza a recorrer
BASE_DIR = "."

# TXT - estilo árbol visual
def print_tree_txt(start_path, prefix="", file=None):
    try:
        items = sorted(os.listdir(start_path))
    except PermissionError:
        return
    for index, item in enumerate(items):
        path = os.path.join(start_path, item)
        is_last = index == len(items) - 1
        connector = "└── " if is_last else "├── "
        line = prefix + connector + item
        if file:
            file.write(line + "\n")
        if os.path.isdir(path):
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_tree_txt(path, new_prefix, file)

# CSV - tipo y ruta
def export_csv(start_path, file):
    writer = csv.writer(file)
    writer.writerow(["Tipo", "Ruta"])
    for root, dirs, files in os.walk(start_path):
        for d in dirs:
            writer.writerow(["Carpeta", os.path.join(root, d)])
        for f in files:
            writer.writerow(["Archivo", os.path.join(root, f)])

# JSON - árbol estructurado
def build_json_tree(path):
    node = {"name": os.path.basename(path), "children": []}
    try:
        for item in sorted(os.listdir(path)):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                node["children"].append(build_json_tree(full_path))
            else:
                node["children"].append({"name": item})
    except PermissionError:
        pass
    return node

def generar_reportes(base_dir):
    export_dir = os.path.abspath("export_tree")
    os.makedirs(export_dir, exist_ok=True)  # crea carpeta si no existe

    txt_path = os.path.join(export_dir, "tree.txt")
    csv_path = os.path.join(export_dir, "tree.csv")
    json_path = os.path.join(export_dir, "tree.json")

    with open(txt_path, "w", encoding="utf-8") as txt_file:
        print_tree_txt(base_dir, file=txt_file)

    with open(csv_path, "w", newline='', encoding="utf-8") as csv_file:
        export_csv(base_dir, csv_file)

    tree = build_json_tree(base_dir)
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(tree, json_file, indent=2)

    print("✔️ Archivos generados en carpeta 'export_tree':")
    print(f"- {txt_path}")
    print(f"- {csv_path}")
    print(f"- {json_path}")

# Ejecutar
if __name__ == "__main__":
    generar_reportes(BASE_DIR)
