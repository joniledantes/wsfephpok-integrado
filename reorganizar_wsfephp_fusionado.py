import os
import shutil

ORIGEN = "wsfephp"      # Carpeta origen relativa a donde se ejecuta el script
DESTINO = "wsfephp_mod" # Nueva carpeta destino (no debe existir)

SUBCARPETAS = [
    "admin",
    "class",
    "core/modules",
    "core/triggers",
    "doc",
    "lang",
    "scripts",
    "temp"
]

def destino_relativo(filename):
    f = filename.lower()
    if f.endswith('.class.php'):
        return "class"
    if f.endswith('.php') and ("setup" in f or "config" in f):
        return "admin"
    if f.endswith('.php') and "trigger" in f:
        return "core/triggers"
    if f.endswith('.php') and ("mod" in f or "module" in f):
        return "core/modules"
    if f.endswith('.xml') or f.startswith("request") or f.startswith("response"):
        return "doc"
    if f.endswith('.lang'):
        return "lang"
    if f.startswith('cron') and f.endswith('.php'):
        return "scripts"
    if f.endswith('.log') or "log" in f:
        return "temp"
    return ""

def limpiar_archivos(nombre):
    descartar = [
        '.zip', '.bak', '.tmp', '.rar', '.7z', 'error_log', 'Untitled', '.ps1'
    ]
    for x in descartar:
        if nombre.lower().endswith(x) or x in nombre:
            return True
    return False

def copiar_reestructura(origen, destino):
    if os.path.exists(destino):
        print(f"Eliminando carpeta previa {destino}...")
        shutil.rmtree(destino)
    os.makedirs(destino)

    for sub in SUBCARPETAS:
        os.makedirs(os.path.join(destino, sub), exist_ok=True)

    for root, dirs, files in os.walk(origen):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), origen)
            if limpiar_archivos(file):
                print(f"Descartando: {rel_path}")
                continue
            subcarpeta = destino_relativo(file)
            destino_final = os.path.join(destino, subcarpeta) if subcarpeta else destino
            os.makedirs(destino_final, exist_ok=True)
            shutil.copy2(os.path.join(root, file), os.path.join(destino_final, file))
            print(f"Copiado: {rel_path} -> {os.path.join(subcarpeta, file) if subcarpeta else file}")

    open(os.path.join(destino, "README.md"), "a").close()
    open(os.path.join(destino, "temp", ".gitkeep"), "a").close()
    print(f"\nEstructura migrada en {destino}/")

if __name__ == "__main__":
    copiar_reestructura(ORIGEN, DESTINO)