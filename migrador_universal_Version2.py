import os
import shutil
import re
import logging
from datetime import datetime

# CONFIGURACIÓN PRINCIPAL
ORIGEN = "motocenterhtdocs"
DESTINO = "wsfephp"
DRY_RUN = False            # Si True, solo simula operaciones
INTERACTIVE = True         # Si True, pide confirmación para eliminar destino
LOG_DIR = "logs"
SUBCARPETAS = [
    "admin", "class", "core/modules", "core/triggers", "doc", "lang",
    "scripts", "scripts/sql", "temp", "img", "public/css", "public/js",
    "public/assets", "keys", "tests", "unclassified_files"
]
DESCARTAR = [
    '.zip', '.bak', '.tmp', '.rar', '.7z', 'error_log', 'untitled', '.ps1',
    '.log', '.psd', 'Thumbs.db', '.DS_Store', 'desktop.ini'
]
CLASIFICACION = [
    (r'\.class\.php$', "class"),
    (r'\.lib\.php$', "class"),
    (r'(setup|config|admin|tools)\.php$', "admin"),
    (r'trigger', "core/triggers"),
    (r'(mod|module).*\.php$', "core/modules"),
    (r'\.(xml|pdf|md|csv)$', "doc"),
    (r'^(ejemplo_|manual|diagram|docs|request-|response-)', "doc"),
    (r'\.lang$', "lang"),
    (r'^cron.*\.php$', "scripts"),
    (r'(script|import|export).*\.php$', "scripts"),
    (r'\.sql$', "scripts/sql"),
    (r'(icon|logo|object_).*\.(png|jpg|jpeg|gif|svg|ico)$', "img"),
    (r'\.css$', "public/css"),
    (r'\.js$', "public/js"),
    (r'\.(woff|ttf|eot|json)$', "public/assets"),
    (r'\.(png|jpg|jpeg|gif|svg|ico)$', "public/assets"),
    (r'^(test).*\.php$', "tests"),
    (r'\.(crt|key|csr|pfx)$', "keys"),
]

# LOGGING
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"migrador_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[logging.FileHandler(LOG_FILE, encoding='utf-8'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def destino_relativo(nombre):
    f = nombre.lower()
    for patron, destino in CLASIFICACION:
        if re.search(patron, f):
            if destino == "scripts/sql" and f in ("install.sql", "uninstall.sql"):
                return "" # scripts SQL principales van a raíz
            return destino
    return "unclassified_files"

def limpiar(nombre):
    f = nombre.lower()
    for x in DESCARTAR:
        if f.endswith(x) or x in f:
            return True
    return False

def confirmar(texto):
    if INTERACTIVE:
        return input(f"{texto} (s/n): ").strip().lower() == "s"
    return True

def copiar_reestructura(origen, destino, dry_run=False):
    logger.info(f"Iniciando migración: {origen} → {destino} (dry_run={dry_run})")
    if os.path.exists(destino):
        if dry_run:
            logger.info(f"[DRY RUN] Se simularía eliminación de {destino}")
        else:
            if confirmar(f"La carpeta {destino} será ELIMINADA. ¿Continuar?"):
                shutil.rmtree(destino)
                logger.info(f"Eliminada carpeta previa {destino}")
            else:
                logger.info("Operación cancelada por usuario.")
                return
    if not dry_run:
        os.makedirs(destino, exist_ok=True)
        for sub in SUBCARPETAS:
            os.makedirs(os.path.join(destino, sub), exist_ok=True)
    archivos_copiados, descartados, no_clasificados = 0, 0, []
    for root, dirs, files in os.walk(origen):
        for file in files:
            rel = os.path.relpath(os.path.join(root, file), origen)
            if limpiar(file):
                logger.info(f"Descartando: {rel}")
                descartados += 1
                continue
            subcarpeta = destino_relativo(file)
            if subcarpeta == "unclassified_files":
                no_clasificados.append(rel)
            destino_final = os.path.join(destino, subcarpeta) if subcarpeta else destino
            if not dry_run:
                os.makedirs(destino_final, exist_ok=True)
                shutil.copy2(os.path.join(root, file), os.path.join(destino_final, file))
            logger.info(f"Copiado: {rel} → {os.path.join(subcarpeta, file) if subcarpeta else file}")
            archivos_copiados += 1
    # Archivos raíz y .gitkeep
    if not dry_run:
        open(os.path.join(destino, "README.md"), "a").close()
        open(os.path.join(destino, "temp", ".gitkeep"), "a").close()
    logger.info(f"Total copiados: {archivos_copiados} | descartados: {descartados}")
    if no_clasificados:
        logger.warning("Archivos NO CLASIFICADOS:")
        for f in no_clasificados:
            logger.warning(f"  - {f}")
    logger.info("¡Migración terminada!")

if __name__ == "__main__":
    copiar_reestructura(ORIGEN, DESTINO, DRY_RUN)