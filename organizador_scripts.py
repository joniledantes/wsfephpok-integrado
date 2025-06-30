import os
import hashlib
import shutil

# Ruta de origen donde están todos los scripts
ORIGEN = r"C:\Users\Viaweb\Documents\GitHub"
DESTINO = r"C:\temp\scripts_limpios_wsfephpok"

# Categorías
CATEGORIAS = {
    "migrar": "migradores",
    "reorganizar": "reorganizadores",
    "fusionador": "fusionadores",
    "profesionalizar": "utilitarios",
    "verificador": "utilitarios",
    "normalizador": "utilitarios",
    "deduplicador": "utilitarios",
    "estructura": "utilitarios",
    "test": "tests",
    "tree": "utilitarios",
    "imagenes": "utilitarios",
    "wordpress": "utilitarios"
}

# Inicializa estructuras
hashes = {}
reporte = []

def categorizar(nombre):
    for clave, categoria in CATEGORIAS.items():
        if clave.lower() in nombre.lower():
            return categoria
    return "otros"

def hash_archivo(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def procesar_archivos():
    for root, _, files in os.walk(ORIGEN):
        for nombre in files:
            if nombre.endswith(".py"):
                origen_completo = os.path.join(root, nombre)
                hash_val = hash_archivo(origen_completo)

                if hash_val in hashes:
                    destino = os.path.join(DESTINO, "duplicados", nombre)
                else:
                    categoria = categorizar(nombre)
                    destino = os.path.join(DESTINO, categoria, nombre)
                    hashes[hash_val] = origen_completo

                os.makedirs(os.path.dirname(destino), exist_ok=True)
                shutil.copy2(origen_completo, destino)

                reporte.append({
                    "archivo": nombre,
                    "hash": hash_val,
                    "origen": origen_completo,
                    "categoria": categoria if hash_val not in hashes else "duplicados",
                    "duplicado": "Sí" if hash_val in hashes and hashes[hash_val] != origen_completo else "No"
                })

def guardar_reporte():
    csv_path = os.path.join(DESTINO, "informe_scripts.csv")
    md_path = os.path.join(DESTINO, "informe_scripts.md")

    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("Archivo,Hash,Origen,Categoría,Duplicado\n")
        for r in reporte:
            f.write(f"{r['archivo']},{r['hash']},{r['origen']},{r['categoria']},{r['duplicado']}\n")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("| Archivo | Categoría | Duplicado | Origen |\n")
        f.write("|---------|-----------|-----------|--------|\n")
        for r in reporte:
            f.write(f"| {r['archivo']} | {r['categoria']} | {r['duplicado']} | `{r['origen']}` |\n")

if __name__ == "__main__":
    print("[+] Procesando scripts...")
    procesar_archivos()
    guardar_reporte()
    print("[✔] Listo. Archivos organizados en:", DESTINO)
