import os
import shutil
import re
import logging
from datetime import datetime

# === CONFIGURACIÓN INICIAL ===
ORIGEN = r"C:\Users\Viaweb\Desktop\viawebsas\wsfephp\ok"   # Tu carpeta fuente
DESTINO = r"C:\Users\Viaweb\Desktop\viawebsas\wsfephp\ok_migrado"  # Cambia el destino si quieres
DRY_RUN = False                 # True = solo simula, no copia ni borra nada
INTERACTIVE_MODE = True         # True = pide confirmación antes de borrar DESTINO

SUBCARPETAS = [
    "admin", "class", "core/modules", "core/triggers", "doc", "lang", "scripts",
    "scripts/sql", "temp", "img", "public/css", "public/js", "public/assets", "keys", "tests"
]

DIRS_TO_IGNORE = [
    ".git", ".github", ".vscode", "vendor", "node_modules"
    # Puedes agregar más carpetas a ignorar según tu entorno
]

DESCARTAR_PATTERNS = [
    r"\.zip$", r"\.bak$", r"\.tmp$", r"\.rar$", r"\.7z$", r"error_log$", r"untitled",
    r"\.ps1$", r"\.db$", r"\.ini$", r"\.psd$", r"~$", r"estructura\.txt$", r"\.log$"
]

FILE_CLASSIFICATION_RULES = [
    (r"\.class\.php$", "class"),
    (r"\.lib\.php$", "class"),
    (r"(setup|config|admin|tools)\.php$", "admin"),
    (r"trigger", "core/triggers"),
    (r"(mod|module).*\.php$", "core/modules"),
    (r"\.(xml|pdf|md|csv)$", "doc"),
    (r"^(ejemplo_|manual|diagram|docs|request-|response-)", "doc"),
    (r"\.lang$", "lang"),
    (r"^cron.*\.php$", "scripts"),
    (r"(script|import|export).*\.php$", "scripts"),
    (r"\.sql$", "scripts/sql"),
    (r"\.log$", "temp"),
    (r"(icon|logo|object_).*\.(png|jpg|jpeg|gif|svg|ico)$", "img"),
    (r"\.css$", "public/css"),
    (r"\.js$", "public/js"),
    (r"\.(woff|ttf|eot|json)$", "public/assets"),
    (r"\.(png|jpg|jpeg|gif|svg|ico)$", "public/assets"),
    (r"^(test).*\\.(php|py|js)$", "tests"),
    (r"\.(crt|key|csr|pfx)$", "keys"),
    (r"^(readme\.md|license|gitignore|changelog\.md|install\.sql|uninstall\.sql|composer\.json|travis\.yml|copying|dockerfile|php_cs.*|phpunit\.xml)$", ""),
]

logdir = "logs_migracion"
if not os.path.exists(logdir):
    os.makedirs(logdir)
logfile = os.path.join(logdir, f"migracion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(logfile, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def limpiar_archivos(nombre):
    for pattern in DESCARTAR_PATTERNS:
        if re.search(pattern, nombre.lower()):
            return True
    return False

def destino_relativo(filename):
    f = filename.lower()
    for pattern, destino in FILE_CLASSIFICATION_RULES:
        if re.search(pattern, f):
            if destino == "scripts/sql" and f in ("install.sql", "uninstall.sql"):
                return ""
            return destino
    return "unclassified_files"

def confirm_action(prompt):
    if INTERACTIVE_MODE:
        resp = input(f"{prompt} (s/n): ").lower().strip()
        return resp == "s"
    return True

def copiar_reestructura(origen, destino, dry_run=False):
    archivos_copiados, archivos_descartados = 0, 0
    archivos_no_clasificados = []

    if os.path.exists(destino):
        if dry_run:
            logging.info(f"[DRY RUN] Se simularía la eliminación de '{destino}'")
        else:
            if confirm_action(f"La carpeta destino '{destino}' será ELIMINADA. ¿Continuar?"):
                shutil.rmtree(destino)
                logging.info(f"Carpeta '{destino}' eliminada.")
            else:
                logging.info("Operación cancelada por el usuario.")
                return
    if not dry_run:
        os.makedirs(destino, exist_ok=True)

    todas_subs = list(SUBCARPETAS)
    if "unclassified_files" not in todas_subs:
        todas_subs.append("unclassified_files")
    for sub in todas_subs:
        ruta = os.path.join(destino, sub)
        if not dry_run:
            os.makedirs(ruta, exist_ok=True)

    for root, dirs, files in os.walk(origen):
        dirs[:] = [d for d in dirs if d.lower() not in [x.lower() for x in DIRS_TO_IGNORE]]
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), origen)
            if limpiar_archivos(file):
                logging.info(f"🗑️ Descartando: '{rel_path}'")
                archivos_descartados += 1
                continue
            subcarpeta = destino_relativo(file)
            if subcarpeta == "unclassified_files":
                archivos_no_clasificados.append(rel_path)
            destino_final = os.path.join(destino, subcarpeta) if subcarpeta else destino
            if not dry_run:
                os.makedirs(destino_final, exist_ok=True)
                shutil.copy2(os.path.join(root, file), os.path.join(destino_final, file))
                logging.info(f"Copiado: {rel_path} -> {os.path.join(subcarpeta, file) if subcarpeta else file}")
            else:
                logging.info(f"[DRY RUN] Copiado: {rel_path} -> {os.path.join(subcarpeta, file) if subcarpeta else file}")
            archivos_copiados += 1

    esenciales = ["README.md", "LICENSE", ".gitignore", "CHANGELOG.md"]
    for fname in esenciales:
        fpath = os.path.join(destino, fname)
        if not os.path.exists(fpath) and not dry_run:
            open(fpath, "a", encoding='utf-8').close()
            logging.info(f"Creado archivo esencial: {fname}")
    gitkeep = os.path.join(destino, "temp", ".gitkeep")
    if not os.path.exists(gitkeep) and not dry_run:
        open(gitkeep, "a", encoding='utf-8').close()

    logging.info(f"\n--- Resumen ---")
    logging.info(f"Archivos copiados: {archivos_copiados}")
    logging.info(f"Archivos descartados: {archivos_descartados}")
    if archivos_no_clasificados:
        logging.warning(f"Archivos no clasificados ({len(archivos_no_clasificados)}):")
        for f in archivos_no_clasificados:
            logging.warning(f"  - {f}")
        logging.warning("Revisa estos archivos y actualiza las reglas si es necesario.")

    if dry_run:
        logging.info("¡DRY RUN finalizado (no se hicieron cambios en disco)!")
    else:
        logging.info(f"¡Migración finalizada en '{destino}'!")

if __name__ == "__main__":
    copiar_reestructura(ORIGEN, DESTINO, DRY_RUN)