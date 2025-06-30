import os
import shutil
import re
import json
import logging
from datetime import datetime

# --- CONFIGURACIÓN EDITABLE ---
CONFIG = {
    "ORIGEN": "motocenterhtdocs",
    "DESTINO": "wsfephp_migrado",
    "DRY_RUN": False,
    "INTERACTIVE_MODE": True,
    "LOG_OUTPUT_DIR": "logs_migracion",
    "SUBCARPETAS": [
        "admin",
        "class",
        "core/modules",
        "core/triggers",
        "doc",
        "lang",
        "scripts",
        "scripts/sql",
        "temp",
        "img",
        "public/css",
        "public/js",
        "public/assets",
        "keys",
        "tests"
    ],
    "DIRS_TO_IGNORE": [
        ".git", ".github", ".vscode", "vendor", "node_modules"
    ],
    "DESCARTAR_PATTERNS": [
        r"\.zip$", r"\.bak$", r"\.tmp$", r"\.rar$", r"\.7z$", r"error_log$", r"untitled", r"\.ps1$",
        r"^estructura\.txt$", r"\.log$", r"\.db$", r"\.ini$", r"\.psd$", r"~$"
    ],
    "FILE_CLASSIFICATION_RULES": [
        {"pattern": r"\.class\.php$", "destination": "class"},
        {"pattern": r"\.lib\.php$", "destination": "class"},
        {"pattern": r"(setup|config|admin|tools)\.php$", "destination": "admin"},
        {"pattern": r"trigger", "destination": "core/triggers"},
        {"pattern": r"(mod|module).*\.php$", "destination": "core/modules"},
        {"pattern": r"\.(xml|pdf|md|csv)$", "destination": "doc"},
        {"pattern": r"\.lang$", "destination": "lang"},
        {"pattern": r"^cron.*\.php$", "destination": "scripts"},
        {"pattern": r"(script|import|export).*\.php$", "destination": "scripts"},
        {"pattern": r"\.sql$", "destination": "scripts/sql"},
        {"pattern": r"\.log$", "destination": "temp"},
        {"pattern": r"(icon|logo|object_).*\.(png|jpg|jpeg|gif|svg|ico)$", "destination": "img"},
        {"pattern": r"\.css$", "destination": "public/css"},
        {"pattern": r"\.js$", "destination": "public/js"},
        {"pattern": r"\.(woff|ttf|eot|json)$", "destination": "public/assets"},
        {"pattern": r"\.(png|jpg|jpeg|gif|svg|ico)$", "destination": "public/assets"},
        {"pattern": r"^(test).*\\.(php|py|js)$", "destination": "tests"},
        {"pattern": r"\.(crt|key|csr|pfx)$", "destination": "keys"},
        {"pattern": r"^(readme\.md|license|gitignore|changelog\.md|install\.sql|uninstall\.sql|composer\.json|travis\.yml|copying|dockerfile|php_cs.*|phpunit\.xml)$", "destination": ""},
    ]
}

# --- LOGGING ---
if not os.path.isdir(CONFIG["LOG_OUTPUT_DIR"]):
    os.makedirs(CONFIG["LOG_OUTPUT_DIR"], exist_ok=True)
logfile = os.path.join(CONFIG["LOG_OUTPUT_DIR"], f"migracion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(logfile, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def limpiar_archivos(nombre):
    for pattern in CONFIG["DESCARTAR_PATTERNS"]:
        if re.search(pattern, nombre.lower()):
            return True
    return False

def destino_relativo(filename):
    f = filename.lower()
    for rule in CONFIG["FILE_CLASSIFICATION_RULES"]:
        if re.search(rule["pattern"], f):
            return rule["destination"]
    return "unclassified_files"

def confirm_action(prompt):
    if CONFIG["INTERACTIVE_MODE"]:
        respuesta = input(f"{prompt} (s/n): ").lower().strip()
        return respuesta == "s"
    return True

def copiar_reestructura(origen, destino, dry_run=False):
    archivos_copiados, archivos_descartados = 0, 0
    archivos_no_clasificados = []

    # Eliminar destino si existe
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

    # Crear subcarpetas
    todas_subs = list(CONFIG["SUBCARPETAS"])
    if "unclassified_files" not in todas_subs:
        todas_subs.append("unclassified_files")
    for sub in todas_subs:
        ruta = os.path.join(destino, sub)
        if not dry_run:
            os.makedirs(ruta, exist_ok=True)

    # Copiar archivos
    for root, dirs, files in os.walk(origen):
        dirs[:] = [d for d in dirs if d.lower() not in [x.lower() for x in CONFIG["DIRS_TO_IGNORE"]]]
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

    # Archivos esenciales
    esenciales = ["README.md", "LICENSE", ".gitignore", "CHANGELOG.md"]
    for fname in esenciales:
        fpath = os.path.join(destino, fname)
        if not os.path.exists(fpath) and not dry_run:
            open(fpath, "a", encoding='utf-8').close()
            logging.info(f"Creado archivo esencial: {fname}")
    gitkeep = os.path.join(destino, "temp", ".gitkeep")
    if not os.path.exists(gitkeep) and not dry_run:
        open(gitkeep, "a", encoding='utf-8').close()

    # Resumen
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
    copiar_reestructura(CONFIG["ORIGEN"], CONFIG["DESTINO"], CONFIG["DRY_RUN"])