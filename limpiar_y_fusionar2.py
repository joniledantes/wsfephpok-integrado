import os
import shutil

# Ruta donde están los scripts
BASE_DIR = r"C:\Temp\scripts_limpios_wsfephpok_limpio"

# Categorías y palabras clave para clasificar archivos
CATEGORIES = {
    "migradores": ["migrador", "migrar"],
    "reorganizadores": ["reorganizador", "reorganizar"],
    "fusionadores": ["fusionador", "fusionar"],
    "duplicados": ["deduplicador", "deduplicar"],
    "profesionalizadores": ["profesionalizar"],
    "verificadores": ["verificador"],
    "tests": ["test"],
    "otros": []
}

def get_category(filename):
    name = filename.lower()
    for category, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in name:
                return category
    return "otros"

def move_file(src_path, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    basename = os.path.basename(src_path)
    dest_path = os.path.join(dest_dir, basename)
    # Evitar sobrescribir: si existe, agregar sufijo
    count = 1
    while os.path.exists(dest_path):
        name, ext = os.path.splitext(basename)
        dest_path = os.path.join(dest_dir, f"{name}_{count}{ext}")
        count += 1
    shutil.move(src_path, dest_path)
    print(f"Movido: {basename} -> {dest_path}")

def main():
    for entry in os.listdir(BASE_DIR):
        if entry.lower().endswith(".py"):
            full_path = os.path.join(BASE_DIR, entry)
            category = get_category(entry)
            dest_folder = os.path.join(BASE_DIR, category)
            move_file(full_path, dest_folder)

if __name__ == "__main__":
    main()
