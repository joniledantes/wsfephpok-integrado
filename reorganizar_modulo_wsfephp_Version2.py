import os
import shutil

ORIGEN = "motocenterhtdocs"
DESTINO = "wsfephp"

SUBCARPETAS = [
    "admin",
    "class",
    "core/modules",
    "core/triggers",
    "doc",
    "lang",
    "scripts",
    "temp",
    "img"
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
    if f.endswith('.xml') or f.endswith('.pdf') or f.endswith('.md'):
        return "doc"
    if f.endswith('.lang'):
        return "lang"
    if f.startswith('cron') and f.endswith('.php'):
        return "scripts"
    if f.endswith('.log') or "log" in f:
        return "temp"
    if f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico')):
        return "img"
    return ""

def limpiar_archivos(nombre):
    descartar = ['.zip', '.bak', '.tmp', '.rar', '.7z', 'error_log', 'Untitled', '.ps1']
    for x in descartar:
        if nombre.lower().endswith(x) or x in nombre:
            return True
    return False

def copiar_reestructura(origen, destino):
    # Intenta eliminar la carpeta destino si existe
    if os.path.exists(destino):
        try:
            shutil.rmtree(destino)
            print(f"Eliminando carpeta previa {destino}...")
        except PermissionError as e:
            print(f"No se pudo eliminar completamente {destino}. Algunos archivos podrían quedarse. Error: {e}")
            print("El script continuará y copiará los archivos nuevos.")
    os.makedirs(destino, exist_ok=True)

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
            try:
                shutil.copy2(os.path.join(root, file), os.path.join(destino_final, file))
                print(f"Copiado: {rel_path} -> {os.path.join(subcarpeta, file) if subcarpeta else file}")
            except PermissionError as e:
                print(f"Error copiando {file}: {e} (¿Archivo bloqueado?)")

    open(os.path.join(destino, "README.md"), "a").close()
    open(os.path.join(destino, "temp", ".gitkeep"), "a").close()
    print(f"\n¡Estructura migrada en {destino}/! Revisa rutas en los require/include si es necesario.")

if __name__ == "__main__":
    copiar_reestructura(ORIGEN, DESTINO)