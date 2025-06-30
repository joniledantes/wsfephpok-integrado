import os
import shutil
import re
import json
import logging
from datetime import datetime

# --- Configuración del Logger ---
# Obtiene el directorio actual del script para asegurar que la carpeta 'logs' se cree allí
script_dir = os.path.dirname(os.path.abspath(__file__))

# --- Configuración del Módulo (antes en config_reestructuracion.json) ---
# Esta cadena JSON contiene todas las configuraciones del script.
# Si necesitas cambiar algo, edita esta cadena directamente.
# ¡IMPORTANTE! Las rutas ahora usan barras inclinadas (/) en lugar de barras invertidas (\)
# para evitar problemas de escape en JSON.
# La 'r' al principio de la cadena la convierte en una "raw string" para manejar mejor las barras invertidas
# si se usaran dentro de los patrones regex (aunque ya están doblemente escapadas, es una capa extra de seguridad).
CONFIG_JSON_STRING = r"""
{
    "ORIGEN": "C:/Users/Viaweb/Documents/GitHub/wsfephpok",
    "DESTINO": "C:/Users/Viaweb/Documents/GitHub/wsfephpok-nueva",
    "DRY_RUN": false,
    "INTERACTIVE_MODE": true,
    "LOG_OUTPUT_DIR": "C:/Temp/logs_reorganizador",
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
    "DIRS_TO_IGNORE_COMPLETELY": [
        ".git", ".github", ".vscode", "vendor", "node_modules",
        "admin", "adherents", "accounting", "agenda", "bank", "barcode", "categories",
        "companies", "compta",
        "comm", "donations", "ecm", "expensereport", "externalsite",
        "fourn", "ftp", "google", "gravatar", "hr", "holiday", "ldap", "mail", "margin",
        "mrp", "multicurrency", "oauth", "paypal", "paybox", "paysbox", "pfg", "pos",
        "printing", "product", "propal", "recursoshumanos", "rubrique", "serverinfo",
        "societe", "stock", "takepos", "tax", "temp", "ticket", "transfer", "user",
        "vat", "website",
        "documents", "includes", "scripts_core_dolibarr", "langs", "lib", "xml", "plantillas", "sql", "arca"
    ],
    "DESCARTAR_PATTERNS": [
        "\\\\.zip$",          
        "\\\\.bak$",          
        "\\\\.tmp$",          
        "\\\\.rar$",          
        "\\\\.7z$",           
        "error_log$",      
        "untitled",        
        "\\\\.ps1$",          
        "thumbs\\\\.db$",     
        "\\\\.ds_store$",     
        "desktop\\\\.ini$",   
        "~\\\\$",             
        "\\\\.psd$",          
        " \\\\((\\\\d+)\\\\)\\\\.",    
        "^migrar_.*\\\\.py$", 
        "^reorganizar_.*\\\\.py$", 
        "estructura\\\\.txt$",
        "test_xml_iva_condition\\\\.py$", 
        "^motocenterhtdocsestructura\\\\.txt$", 
        "^CAE-autorizado-AFIP-advertencia\\\\.txt$", 
        "\\\\.log$" 
    ],
    "FILE_CLASSIFICATION_RULES": [
        {"pattern": "\\\\.class\\\\.php$", "destination": "class", "description": "Clases PHP"},
        {"pattern": "\\\\.lib\\\\.php$", "destination": "class", "description": "Librerías PHP"},
        {"pattern": "(setup|config|admin|tools)\\\\.php$", "destination": "admin", "description": "Scripts de administración"},
        {"pattern": "trigger", "destination": "core/triggers", "description": "Triggers PHP"},
        {"pattern": "(mod|module).*\\\\.php$", "destination": "core/modules", "description": "Definiciones de módulo PHP"},
        {"pattern": "\\\\.(xml|pdf|md|csv)$", "destination": "doc", "description": "Archivos de documentación/ejemplo"},
        {"pattern": "^(ejemplo_|manual|diagram|docs|request-|response-)", "destination": "doc", "description": "Documentación y ejemplos específicos"},
        {"pattern": "\\\\.lang$", "destination": "lang", "description": "Archivos de idioma"},
        {"pattern": "^cron.*\\\\.php$", "destination": "scripts", "description": "Scripts de Cron"},
        {"pattern": "(script|import|export).*\\\\.php$", "destination": "scripts", "description": "Scripts de utilidad"},
        {"pattern": "\\\\.sql$", "destination": "scripts/sql", "description": "Scripts SQL (excepto install/uninstall en raíz)"},
        {"pattern": "\\\\.log$", "destination": "temp", "description": "Archivos de log"},
        {"pattern": "(icon|logo|object_).*\\\\.(png|jpg|jpeg|gif|svg|ico)$", "destination": "img", "description": "Iconos y logos del módulo"},
        {"pattern": "\\\\.css$", "destination": "public/css", "description": "Archivos CSS públicos"},
        {"pattern": "\\\\.js$", "destination": "public/js", "description": "Archivos JavaScript públicos"},
        {"pattern": "\\\\.(woff|ttf|eot|json)$", "destination": "public/assets", "description": "Assets públicos (fuentes, JSON)"},
        {"pattern": "\\\\.(png|jpg|jpeg|gif|svg|ico)$", "destination": "public/assets", "description": "Imágenes generales (si no son iconos)"},
        {"pattern": "^(test).*\\\\.(php|py|js)$", "destination": "tests", "description": "Archivos de test"},
        {"pattern": "\\.(crt|key|csr|pfx)$", "destination": "keys", "description": "Archivos de certificado"},
        {"pattern": "^(readme\\\\.md|license|gitignore|changelog\\\\.md|install\\\\.sql|uninstall\\\\.sql|composer\\\\.json|travis\\\\.yml|copying|dockerfile|php_cs.*|phpunit\\\\.xml)$", "destination": "", "description": "Archivos de la raíz"}
    ]
}
"""
# Intenta cargar la configuración desde la cadena JSON.
try:
    CONFIG = json.loads(CONFIG_JSON_STRING)
except json.JSONDecodeError as e:
    print(f"ERROR CRÍTICO: Error al parsear la cadena de configuración JSON interna: {e}")
    print("El script no puede continuar. Revisa la sintaxis de la cadena CONFIG_JSON_STRING.")
    exit(1)

# Determina el directorio de logs. Prioriza la configuración del JSON, sino usa 'logs'
# dentro del directorio del script. Convierte la ruta a absoluta para mayor robustez.
log_directory_from_config = CONFIG.get("LOG_OUTPUT_DIR", os.path.join(script_dir, "logs"))
log_directory = os.path.abspath(log_directory_from_config)

# Asegúrate de que la carpeta de logs exista. Si no, la crea.
# Esta es una de las primeras operaciones, por lo que su éxito es vital.
try:
    os.makedirs(log_directory, exist_ok=True)
except Exception as e:
    # Si la creación de la carpeta de logs falla (ej. por permisos), se imprime un error crítico
    # directamente en la consola y el script se cierra, ya que no puede proceder sin logging.
    print(f"ERROR CRÍTICO: No se pudo crear la carpeta de logs en '{log_directory}'. Error: {e}")
    print("Asegúrate de tener permisos de escritura en este directorio o de que la ruta sea válida.")
    exit(1) # Sale del script si no se puede inicializar el log

# Define el nombre completo del archivo de log, incluyendo la marca de tiempo para unicidad.
log_filename = os.path.join(log_directory, f"reestructuracion_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Configura el sistema de logging. Los mensajes se envían tanto al archivo de log como a la consola.
logging.basicConfig(
    level=logging.INFO, # Nivel mínimo de mensajes a registrar (INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s', # Formato de los mensajes de log
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'), # Handler para escribir en el archivo de log
        logging.StreamHandler()                               # Handler para mostrar en la consola
    ]
)
logger = logging.getLogger(__name__) # Obtiene una instancia del logger para usarla en todo el script


# --- Configuración principal del script (extraída de la cadena JSON) ---
# Las rutas de origen y destino se convierten a absolutas para evitar problemas con el directorio actual de ejecución.
ORIGEN = os.path.abspath(CONFIG.get("ORIGEN", r"C:\Users\Viaweb\Documents\GitHub\wsfephpok"))
DESTINO = os.path.abspath(CONFIG.get("DESTINO", r"C:\Users\Viaweb\Documents\GitHub\wsfephpok-nueva"))

# Modos de ejecución del script, configurables desde el JSON.
DRY_RUN = CONFIG.get("DRY_RUN", False)       # Si es True, el script solo simula operaciones sin modificar archivos.
INTERACTIVE_MODE = CONFIG.get("INTERACTIVE_MODE", True) # Si es True, pide confirmación antes de acciones destructivas.

# Listado de subcarpetas estándar que se crearán dentro del módulo Dolibarr reestructurado.
SUBCARPETAS = CONFIG.get("SUBCARPETAS", [
    "admin",          # Paneles de administración, configuración, logs
    "class",          # Clases principales, auxiliares, modelos de datos
    "core/modules",   # Clase que define el módulo, modelos de PDF/exportación
    "core/triggers",  # Triggers de integración con Dolibarr
    "doc",            # Documentación, manuales, ejemplos (XML, PDF, MD, CSV, genéricos)
    "lang",           # Archivos de idioma
    "scripts",        # Scripts de cron, migración, importación/exportación
    "scripts/sql",    # Scripts SQL adicionales (que no sean install.sql/uninstall.sql)
    "temp",           # Archivos temporales, logs (no versionar, solo para ejecución)
    "img",            # Iconos, logos y otros recursos gráficos (ej. object_nombremodulo.png)
    "public/css",     # Archivos de hojas de estilo CSS para la interfaz pública del módulo
    "public/js",      # Archivos de scripts JavaScript para la interfaz pública del módulo
    "public/assets",  # Otros recursos estáticos públicos (ej. fuentes, imágenes no específicas de 'img')
    "keys",           # Certificados (AFIP, SSL, etc.)
    "tests"           # Tests unitarios o de integración (recomendado)
])

# Lista de directorios del core de Dolibarr o directorios de desarrollo/sistema a ignorar completamente
# en la carpeta de ORIGEN. Esto evita copiar directorios innecesarios o no relacionados con el módulo.
DIRS_TO_IGNORE_COMPLETELY = CONFIG.get("DIRS_TO_IGNORE_COMPLETELY", [
    '.git', '.github', '.vscode', 'vendor', 'node_modules', # Carpetas de desarrollo/sistema
    'admin', 'adherents', 'accounting', 'agenda', 'bank', 'barcode', 'categories', 
    'companies', 'compta', 'comm', 'donations', 'ecm', 'expensereport', 'externalsite',
    'fourn', 'ftp', 'google', 'gravatar', 'hr', 'holiday', 'ldap', 'mail', 'margin', 
    'mrp', 'multicurrency', 'oauth', 'paypal', 'paybox', 'paysbox', 'pfg', 'pos', 
    'printing', 'product', 'propal', 'recursoshumanos', 'rubrique', 'serverinfo', 
    'societe', 'stock', 'takepos', 'tax', 'temp', 'ticket', 'transfer', 'user', 
    'vat', 'website', # Módulos y carpetas estándar de Dolibarr (evitar copiarlos si están en el ORIGEN)
    'documents', # Carpeta genérica de documentos si no es relevante para el módulo
    'includes', # Carpeta común de inclusiones, pero a veces no es parte del módulo
    'scripts_core_dolibarr', # Si tienes una carpeta de scripts del core separada
    'langs', # La carpeta de idiomas del core de Dolibarr, ya tenemos 'lang' para el módulo
    'lib', # La carpeta 'lib' del core de Dolibarr, ya tenemos 'class' para el módulo
    'xml', # La carpeta 'xml' del core de Dolibarr
    'plantillas', # La carpeta 'plantillas' del core de Dolibarr
    'sql', # La carpeta 'sql' del core de Dolibarr
    'arca' # La carpeta 'arca' específica de tu estructura si no es parte del módulo
])

# Patrones de expresiones regulares para identificar archivos que deben ser descartados y no copiados.
DESCARTAR_PATTERNS = CONFIG.get("DESCARTAR_PATTERNS", [
    r'\.zip$',          # Archivos ZIP
    r'\.bak$',          # Backups
    r'\.tmp$',          # Temporales
    r'\.rar$',          # RAR
    r'\.7z$',           # 7z
    r'error_log$',      # Logs de error de PHP/servidor
    r'untitled',        # Archivos con nombres genéricos sin título
    r'\.ps1$',          # Scripts de PowerShell
    r'thumbs\.db$',     # Archivos de miniaturas de Windows
    r'\.ds_store$',     # Archivos de macOS
    r'desktop\.ini$',   # Archivos de configuración de Windows
    r'~\$',             # Archivos temporales de Office (ej. Word, Excel)
    r'\.psd$',          # Archivos de diseño de Photoshop
    r' \((\d+)\)\.',    # Patrón para archivos como "nombre (1).php"
    r'^migrar_.*\.py$', # Scripts de migración (el propio script o versiones anteriores)
    r'^reorganizar_.*\.py$', # Scripts de reorganización
    r'estructura\.txt$',# Archivo de estructura (como el que nos proporcionaste)
    r'test_xml_iva_condition\.py$', # Script de test específico
    r'^motocenterhtdocsestructura\.txt$', # El archivo de estructura grande que analizamos
    r'^CAE-autorizado-AFIP-advertencia\.txt$', # Archivo de advertencia específico
    r'\.log$' # Archivos de log sueltos (ya tenemos una carpeta 'temp' o 'logs' para ellos)
])

# Reglas de clasificación de archivos, definidas como una lista de diccionarios.
# Cada regla tiene un patrón regex, un destino de carpeta y una descripción.
# El orden de las reglas es importante: la primera que coincide con el nombre de archivo se aplica.
FILE_CLASSIFICATION_RULES = CONFIG.get("FILE_CLASSIFICATION_RULES", [
    {"pattern": r"\.class\.php$", "destination": "class", "description": "Clases PHP"},
    {"pattern": r"\.lib\.php$", "destination": "class", "description": "Librerías PHP"},
    {"pattern": r"(setup|config|admin|tools)\.php$", "destination": "admin", "description": "Scripts de administración"},
    {"pattern": r"trigger", "destination": "core/triggers", "description": "Triggers PHP"},
    {"pattern": r"(mod|module).*\.php$", "destination": "core/modules", "description": "Definiciones de módulo PHP"},
    {"pattern": r"\.(xml|pdf|md|csv)$", "destination": "doc", "description": "Archivos de documentación/ejemplo"},
    {"pattern": r"^(ejemplo_|manual|diagram|docs|request-|response-)", "destination": "doc", "description": "Documentación y ejemplos específicos"},
    {"pattern": r"\.lang$", "destination": "lang", "description": "Archivos de idioma"},
    {"pattern": r"^cron.*\.php$", "destination": "scripts", "description": "Scripts de Cron"},
    {"pattern": r"(script|import|export).*\.php$", "destination": "scripts", "description": "Scripts de utilidad"},
    {"pattern": r"\.sql$", "destination": "scripts/sql", "description": "Scripts SQL (excepto install/uninstall en raíz)"},
    {"pattern": r"\.log$", "destination": "temp", "description": "Archivos de log"},
    {"pattern": r"(icon|logo|object_).*\.(png|jpg|jpeg|gif|svg|ico)$", "destination": "img", "description": "Iconos y logos del módulo"},
    {"pattern": r"\.css$", "destination": "public/css", "description": "Archivos CSS públicos"},
    {"pattern": r"\.js$", "destination": "public/js", "description": "Archivos JavaScript públicos"},
    {"pattern": r"\.(woff|ttf|eot|json)$", "destination": "public/assets", "description": "Assets públicos (fuentes, JSON)"},
    {"pattern": r"\.(png|jpg|jpeg|gif|svg|ico)$", "destination": "public/assets", "description": "Imágenes generales (si no son iconos)"},
    {"pattern": "^(test).*\\.(php|py|js)$", "destination": "tests", "description": "Archivos de test"},
    {"pattern": "\\.(crt|key|csr|pfx)$", "destination": "keys", "description": "Archivos de certificado"},
    {"pattern": "^(readme\\.md|license|gitignore|changelog\\.md|install\\.sql|uninstall\\.sql|composer\\.json|travis\\.yml|copying|dockerfile|php_cs.*|phpunit\\.xml)$", "destination": "", "description": "Archivos de la raíz"}
])

def destino_relativo(filename):
    """
    Determina la subcarpeta de destino para un archivo basándose en las reglas de clasificación configuradas.
    Si un archivo es install.sql o uninstall.sql, se fuerza a la raíz si la regla genérica de SQL lo mandaría a scripts/sql.
    """
    f = filename.lower() # Convierte el nombre de archivo a minúsculas para comparaciones insensibles a mayúsculas/minúsculas
    for rule in FILE_CLASSIFICATION_RULES:
        # Busca el patrón regex de la regla en el nombre del archivo.
        if re.search(rule["pattern"], f):
            # Excepción específica: si la regla dirige a 'scripts/sql' pero el archivo es
            # 'install.sql' o 'uninstall.sql', su destino real es la raíz del módulo.
            if rule["destination"] == "scripts/sql" and \
               (f == "install.sql" or f == "uninstall.sql"):
                return "" # Retorna cadena vacía para indicar la raíz
            return rule["destination"] # Retorna la carpeta de destino definida en la regla
    
    # Si el archivo no coincide con ninguna de las reglas definidas, se clasifica como "unclassified_files".
    return "unclassified_files" 

def limpiar_archivos(nombre):
    """
    Define qué archivos deben ser descartados y no copiados al destino.
    Utiliza patrones de expresiones regulares cargados desde la configuración para una limpieza robusta.
    """
    f = nombre.lower() # Convierte el nombre de archivo a minúsculas
    for pattern_str in DESCARTAR_PATTERNS:
        pattern = re.compile(pattern_str) # Compila el patrón regex
        if pattern.search(f): # Busca el patrón en el nombre del archivo
            return True # Si se encuentra el patrón, el archivo debe ser descartado
    return False # Si ningún patrón coincide, el archivo no se descarta

def confirm_action(prompt):
    """
    Pide al usuario que confirme una acción mediante una entrada por consola.
    Solo se activa si el modo interactivo está habilitado.
    """
    if INTERACTIVE_MODE:
        response = input(f"{prompt} (s/n): ").lower().strip()
        return response == 's' # Retorna True si la respuesta es 's' (sí)
    return True # Si no está en modo interactivo, la acción se asume como confirmada

def copiar_reestructura(origen, destino, dry_run=False):
    """
    Función principal que orquesta el proceso de copia y reestructuración de archivos.
    Gestiona la creación de directorios, la copia de archivos, el descarte,
    el modo de prueba (dry_run), el modo interactivo y el registro de eventos.
    """
    if dry_run:
        logger.info("\n--- ✨ MODO DE PRUEBA (DRY RUN) - NO SE REALIZARÁN CAMBIOS REALES EN EL DISCO ---")
    logger.info(f"--- Iniciando reestructuración desde '{os.path.abspath(origen)}' a '{os.path.abspath(destino)}' ---")

    archivos_copiados = 0
    archivos_descartados = 0
    archivos_no_clasificados = []

    # Intenta eliminar la carpeta de destino si ya existe para asegurar una copia limpia.
    # Esta operación se realiza con confirmación en modo interactivo y manejo de errores.
    if os.path.exists(destino):
        if not dry_run: # Solo intenta borrar si no es un dry run
            # Pide confirmación al usuario antes de borrar si el modo interactivo está activado.
            if INTERACTIVE_MODE:
                if not confirm_action(f"La carpeta de destino '{destino}' ya existe y TODO su contenido será ELIMINADO. ¿Deseas continuar?"):
                    logger.info("Operación cancelada por el usuario.")
                    return # Detiene la ejecución si el usuario no confirma

            try:
                logger.info(f"🚀 Eliminando carpeta previa '{destino}' para asegurar una copia limpia...")
                shutil.rmtree(destino) # Elimina el directorio y todo su contenido
            except PermissionError as e:
                # Manejo de error de permisos si la carpeta está en uso o protegida.
                logger.error(f"\n❌ Error de Permiso: No se pudo eliminar completamente la carpeta '{destino}'.")
                logger.error(f"Por favor, asegúrate de que no haya ningún programa utilizando archivos en '{destino}' (ej. explorador de archivos, IDE, terminal abierta).")
                logger.error(f"Error: {e}")
                logger.error("El script no puede continuar en modo real. Borra la carpeta manualmente e inténtalo de nuevo.")
                return # Detiene el script si no se puede borrar
            except Exception as e:
                # Captura cualquier otro error inesperado durante la eliminación.
                logger.error(f"\n❌ Error inesperado al intentar eliminar la carpeta '{destino}': {e}")
                logger.error("El script no puede continuar. Por favor, revisa y resuelve el problema manualmente.")
                return
        else:
            logger.info(f"🚀 [DRY RUN] Se simularía la eliminación de la carpeta previa '{destino}'.")

    # Crea el directorio de destino principal.

    if not dry_run:
        # Asegura que la ruta padre existe antes de crear el destino
        parent_dir = os.path.dirname(destino)
        try:
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
            os.makedirs(destino, exist_ok=True)  # Crea toda la ruta, forzando la creación de padres
            logger.info(f"✅ Carpeta de destino '{destino}' creada (o ya existía si no pudo ser eliminada por completo).")
        except Exception as e:
            logger.error(f"❌ No se pudo crear la carpeta de destino '{destino}'.")
            logger.error(f"   Error: {e}")
            logger.error(f"   Verifica que tienes permisos de escritura en la ruta.")
            return
    else:
        logger.info(f"✅ [DRY RUN] Se simularía la creación de la carpeta de destino '{destino}'.")

    # Crea todas las subcarpetas estándar del módulo, incluyendo la carpeta para archivos no clasificados.
    logger.info("\n--- Creando subcarpetas estándar del módulo ---")
    all_subfolders = list(SUBCARPETAS)
    if "unclassified_files" not in all_subfolders: # Asegura que la carpeta de no clasificados siempre se cree
        all_subfolders.append("unclassified_files")

    for sub in all_subfolders:
        ruta_subcarpeta = os.path.join(destino, sub)
        if not dry_run:
            os.makedirs(ruta_subcarpeta, exist_ok=True)
            logger.info(f"  📂 Creada: '{os.path.join(destino, sub)}'")
        else:
            logger.info(f"  📂 [DRY RUN] Se simularía la creación de: '{os.path.join(destino, sub)}'")

    # Recorre recursivamente todos los archivos y carpetas del origen y los copia al destino.
    logger.info("\n--- Copiando archivos ---")
    for root, dirs, files in os.walk(origen):
        # Filtra los directorios del core de Dolibarr o de desarrollo para no visitarlos ni copiarlos.
        dirs[:] = [d for d in dirs if d.lower() not in [item.lower() for item in DIRS_TO_IGNORE_COMPLETELY]]

        for file in files:
            ruta_origen_completa = os.path.join(root, file)
            # Calcula la ruta relativa del archivo dentro del origen para los mensajes de log.
            rel_path = os.path.relpath(ruta_origen_completa, origen)

            if limpiar_archivos(file): # Verifica si el archivo debe ser descartado
                logger.info(f"  🗑️ Descartando: '{rel_path}' (archivo irrelevante o temporal/backup)")
                archivos_descartados += 1
                continue # Pasa al siguiente archivo

            # Determina la subcarpeta de destino para el archivo usando las reglas.
            subcarpeta_destino = destino_relativo(file)
            ruta_destino_final_dir = os.path.join(destino, subcarpeta_destino)
            ruta_destino_final_file = os.path.join(ruta_destino_final_dir, file)

            # Si el archivo fue clasificado como "unclassified_files", se añade a la lista para el resumen final.
            if subcarpeta_destino == "unclassified_files":
                archivos_no_clasificados.append(rel_path)

            if not dry_run:
                # Asegura que el directorio de destino para este archivo exista.
                os.makedirs(ruta_destino_final_dir, exist_ok=True)
                try:
                    shutil.copy2(ruta_origen_completa, ruta_destino_final_file) # Copia el archivo, preservando metadatos
                    logger.info(f"  ➡️ Copiado: '{rel_path}' -> '{os.path.join(subcarpeta_destino, file) if subcarpeta_destino else file}'")
                    archivos_copiados += 1
                except PermissionError as e:
                    # Manejo de error si no se puede copiar un archivo específico.
                    logger.error(f"  ❌ Error de Permiso copiando '{rel_path}': {e} (Probablemente el archivo está bloqueado o en uso).")
                    logger.warning(f"     Se omitirá este archivo, pero el script continuará. Considera ejecutar con privilegios de administrador.")
                except Exception as e:
                    # Captura cualquier otro error inesperado durante la copia.
                    logger.error(f"  🐛 Error inesperado copiando '{rel_path}': {e}")
                    logger.warning(f"     Se omitirá este archivo, pero el script continuará.")
            else:
                # En modo dry run, solo simula la operación de copia.
                logger.info(f"  ➡️ [DRY RUN] Se simularía la copia de: '{rel_path}' -> '{os.path.join(subcarpeta_destino, file) if subcarpeta_destino else file}'")
                archivos_copiados += 1 # Se cuenta para el resumen de dry run

    # Crea archivos esenciales en la raíz del módulo (ej. README, LICENSE) si no existen ya.
    logger.info("\n--- Verificando y creando archivos esenciales en la raíz del módulo ---")
    archivos_raiz_esenciales = [
        ("README.md", "Guía básica del módulo", "doc"),
        ("LICENSE", "Licencia de uso", "doc"),
        (".gitignore", "Configuración de Git para ignorar archivos", "misc"),
        ("CHANGELOG.md", "Historial de cambios del módulo", "doc"),
        ("install.sql", "Script SQL de instalación (si aplica)", "script"),
        ("uninstall.sql", "Script SQL de desinstalación (si aplica)", "script"),
        ("composer.json", "Configuración de Composer (si aplica)", "misc"),
        (".travis.yml", "Configuración de Travis CI (si aplica)", "misc"),
        (".github/", "Carpeta para CI/CD y plantillas de issues (si aplica)", "misc", True), # El último True indica que es una carpeta
        ("COPYING", "Otra licencia (si aplica)", "doc"),
        ("Dockerfile", "Definición de entorno Docker (si aplica)", "misc")
    ]
    
    for item in archivos_raiz_esenciales:
        filename = item[0]
        description = item[1]
        is_dir = item[3] if len(item) > 3 else False # Determina si el elemento es un directorio

        ruta_completa = os.path.join(destino, filename)
        
        if is_dir: # Si es un directorio esencial (ej. .github/)
            if not dry_run:
                if not os.path.exists(ruta_completa): # Solo lo crea si no existe
                    os.makedirs(ruta_completa, exist_ok=True)
                    logger.info(f"  📂 Creada carpeta de extras: '{filename}' ({description})")
            else:
                logger.info(f"  📂 [DRY RUN] Se simularía la creación de carpeta de extras: '{filename}' ({description})")
            continue # Pasa al siguiente elemento esencial

        # Si es un archivo esencial (ej. README.md) y no existe en el destino
        if not os.path.exists(ruta_completa):
            if not dry_run:
                try:
                    # Crea un archivo vacío en modo 'append', luego lo cierra.
                    open(ruta_completa, "a", encoding='utf-8').close()
                    logger.info(f"  ➕ Creado archivo vacío en la raíz: '{filename}' ({description})")
                except Exception as e:
                    logger.error(f"  ❌ Error creando archivo '{filename}': {e}")
            else:
                logger.info(f"  ➕ [DRY RUN] Se simularía la creación de archivo vacío en la raíz: '{filename}' ({description})")


    # Asegura que el archivo .gitkeep exista en la carpeta 'temp/' para que Git la preserve si está vacía.
    gitkeep_path = os.path.join(destino, "temp", ".gitkeep")
    if not os.path.exists(gitkeep_path):
        if not dry_run:
            open(gitkeep_path, "a", encoding='utf-8').close()
            logger.info(f"  ➕ Creado '.gitkeep' en '{os.path.join(destino, 'temp')}/' para asegurar que la carpeta de temporales no se ignore en Git.")
        else:
            logger.info(f"  ➕ [DRY RUN] Se simularía la creación de '.gitkeep' en '{os.path.join(destino, 'temp')}/'.")
    
    # --- Resumen final de la operación ---
    logger.info(f"\n--- Resumen de la Reestructuración ---")
    logger.info(f"Total de archivos copiados (o simulados): {archivos_copiados}")
    logger.info(f"Total de archivos descartados: {archivos_descartados}")

    # Si se encontraron archivos no clasificados, se listan con una advertencia.
    if archivos_no_clasificados:
        logger.warning(f"\n--- ⚠️  ¡ATENCIÓN: Archivos no clasificados encontrados! ---")
        logger.warning(f"Los siguientes {len(archivos_no_clasificados)} archivos fueron copiados a '{os.path.join(destino, 'unclassified_files')}/':")
        for f in archivos_no_clasificados:
            logger.warning(f"  - {f}")
        logger.warning("Revisa estos archivos y considera añadir nuevas reglas a 'FILE_CLASSIFICATION_RULES' en tu 'config_reestructuracion.json', o confirmarlos como descartables.")

    if dry_run:
        logger.info("\n--- ✨ MODO DE PRUEBA (DRY RUN) FINALIZADO ---")
        logger.info("No se realizaron cambios reales en el disco.")
    else:
        logger.info(f"\n🎉 ¡Reestructuración completada en '{destino}/'!")
        logger.info("⚠️  RECUERDA:")
        logger.info("    1. Es CRUCIAL revisar y ajustar las rutas de 'require', 'include' o 'use' en tus archivos PHP,")
        logger.info("       ya que la ubicación de las clases y otros archivos ha cambiado. Podría ser necesario ajustar los 'namespaces'.")
        logger.info("    2. Revisa y completa los archivos generados como 'README.md', 'LICENSE' y 'CHANGELOG.md'.")
        logger.info("    3. Verifica las carpetas 'public' y 'keys' para asegurar que tus recursos web y certificados están correctamente enlazados.")
        logger.info(f"    4. Revisa el archivo de log '{log_filename}' para un detalle completo de la operación, incluyendo errores o advertencias.")


if __name__ == "__main__":
    # La ejecución principal del script llama a la función de reestructuración.
    # Los argumentos ORIGEN, DESTINO y DRY_RUN se obtienen de la configuración.
    copiar_reestructura(ORIGEN, DESTINO, DRY_RUN)
