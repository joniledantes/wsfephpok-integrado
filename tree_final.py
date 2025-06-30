import os
import json
import csv
import zipfile

# Cambiá esta ruta a una que seguro exista y tengas permisos, por ejemplo C:\Temp
EXPORT_BASE_DIR = r"C:\Temp"
EXPORT_DIR = os.path.join(EXPORT_BASE_DIR, "export_tree")

# Ruta base para escanear, por defecto carpeta actual
BASE_DIR = "."

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

def export_csv(start_path, file):
    writer = csv.writer(file)
    writer.writerow(["Tipo", "Ruta"])
    for root, dirs, files in os.walk(start_path):
        for d in dirs:
            writer.writerow(["Carpeta", os.path.join(root, d)])
        for f in files:
            writer.writerow(["Archivo", os.path.join(root, f)])

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

def comprimir_resultado(export_dir):
    zip_path = os.path.join(export_dir, "estructura_completa.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filename in ["tree.txt", "tree.csv", "tree.json"]:
            full_path = os.path.join(export_dir, filename)
            zipf.write(full_path, arcname=filename)
    print(f"📦 Archivo comprimido: {zip_path}")

def generar_reportes(base_dir):
    print(f"Intentando crear carpeta en: {EXPORT_DIR}")
    os.makedirs(EXPORT_DIR, exist_ok=True)

    txt_path = os.path.join(EXPORT_DIR, "tree.txt")
    csv_path = os.path.join(EXPORT_DIR, "tree.csv")
    json_path = os.path.join(EXPORT_DIR, "tree.json")

    with open(txt_path, "w", encoding="utf-8") as txt_file:
        print_tree_txt(base_dir, file=txt_file)

    with open(csv_path, "w", newline='', encoding="utf-8") as csv_file:
        export_csv(base_dir, csv_file)

    tree = build_json_tree(base_dir)
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(tree, json_file, indent=2)

    print("✔️ Archivos generados en carpeta:")
    print(f"- {txt_path}")
    print(f"- {csv_path}")
    print(f"- {json_path}")

    comprimir_resultado(EXPORT_DIR)

if __name__ == "__main__":
    generar_reportes(BASE_DIR)
