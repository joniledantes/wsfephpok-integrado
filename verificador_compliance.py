"""
verificador_compliance.py
Script para verificar que la estructura final de tu módulo cumple con el checklist de compliance RG 5616 y la integración total, basado en los .md y la estructura sugerida (PHPComparer, Platinum v2.1, etc.).

- Revisa que existan TODOS los archivos/críticos y carpetas requeridas en la carpeta destino (por ejemplo, c:/temp/wsfephp-vw/ordenado).
- Reporta archivos/folders faltantes, archivos extra, y un resumen del estado.
- Lista archivos requeridos por categoría: clases core, admin, paneles, plantillas, scripts, SQL, doc, etc.
- Genera logs: compliance_resultado.txt (resumen y faltantes), compliance_extra.txt (archivos no requeridos).

Uso:
    python verificador_compliance.py [CARPETA]
    Por defecto: CARPETA = c:/temp/wsfephp-vw/ordenado
"""

import os
import sys

DESTINO = r"c:/temp/wsfephp-vw/ordenado"
LOG_RESULT = "compliance_resultado.txt"
LOG_EXTRA = "compliance_extra.txt"

# Checklist mínimo de compliance RG 5616 y Platinum v2.1
# Puedes agregar/quitar archivos si tu entrega los requiere
CHECKLIST = {
    "class": [
        "wsfev1.class.php", "pyafip_compatibility.php", "wsaa.class.php", "wsaa_db.class.php", 
        "wsfe_db.class.php", "wsfe_pos.class.php", "array2xml.class.php", "exceptionhandler.php"
    ],
    "admin": ["admin.php", "panel_admin.php"],  # Ejemplo, ajusta según tus scripts reales
    "core/modules/facture/doc": ["pdf_fe.modules.php", "pdf_fe.modulesA4.php", "pdf_fe.modulesticok.php"],
    "core/modules/facture": ["mod_facture_wsfe.php"],
    "core/vendor/tc-lib-barcode": [],  # Solo carpeta, no archivos
    "plantillas": ["commande.pdf", "factura.pdf", "logo.png"],
    "keys": [],  # Solo carpeta, puede contener .crt y .key
    "langs": ["es_ES.wsfephp-vw.lang", "en_US.wsfephp-vw.lang"],
    "lib": [],  # Helpers extra opcionales
    "sql": ["llx_wsfe_config.sql", "llx_wsfe_invoice.sql", "wsfe_tables.sql"],
    "xml_examples": [],  # Solo carpeta, puede contener .xml
    "scripts": [
        "validate_rg5616.php", "check_rg5616_status.php", "test_pyafip_compatibility.php",
        "test_xml_iva_condition.py", "batch_processor.php", "migration_helper.php",
        "backup_manager.php", "compliance_scheduler.php", "install.sh"
    ],
    "tools": ["fusionador_modulos.py"],
    "docs": [
        "README-INSTALACION.md", "QUICK-START.md", "TECHNICAL-SPEC.md", "DETAILED-MODIFICATIONS.md",
        "CHANGELOG.md", "EXECUTIVE-SUMMARY.md", "FINAL-DELIVERY-SUMMARY.md", "COMPARISON-ANALYSIS.md",
        "README-CAMBIOS-MINIMOS.md", "INFORME-ENTREGA-WSFE.md", "MINIMAL-CHANGES-ANALYSIS.md",
        "dolibarr-comparison-final-report.md", "DELIVERY-CHECKLIST.md", "TROUBLESHOOTING.md", "IMPORT-SQL.md"
    ],
    "img": [],  # Solo carpeta, puede contener cualquier imagen extra
    "": ["wsfephp-vw.module.php", "README.md"]  # raíz del módulo
}

def verificar_compliance(base):
    faltan = []
    extras = []
    encontrados = set()
    # 1. Verifica existencia de cada archivo/carpeta requerido
    for subcarpeta, archivos in CHECKLIST.items():
        carpeta = os.path.join(base, subcarpeta)
        if archivos:
            for archivo in archivos:
                path = os.path.join(carpeta, archivo)
                if not os.path.isfile(path):
                    faltan.append(os.path.relpath(path, base))
                else:
                    encontrados.add(os.path.relpath(path, base))
        else:
            # Si solo se requiere la carpeta (puede estar vacía)
            if not os.path.isdir(carpeta):
                faltan.append(os.path.relpath(carpeta, base))
            else:
                # Marca todos los archivos existentes como encontrados
                for root, dirs, files in os.walk(carpeta):
                    for file in files:
                        encontrados.add(os.path.relpath(os.path.join(root, file), base))
    # 2. Busca archivos extra NO requeridos (no listados en CHECKLIST)
    todos = set()
    for root, dirs, files in os.walk(base):
        for file in files:
            rel = os.path.relpath(os.path.join(root, file), base)
            todos.add(rel)
    extras = list(todos - encontrados)
    return faltan, extras

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else DESTINO
    faltan, extras = verificar_compliance(base)
    with open(LOG_RESULT, "w", encoding="utf-8") as f:
        f.write("# COMPLIANCE RG 5616 Y ENTREGA FINAL\n")
        if not faltan:
            f.write("OK: Todos los archivos requeridos están presentes.\n\n")
        else:
            f.write("FALTAN los siguientes archivos/carpetas críticos:\n")
            for path in faltan:
                f.write(f"- {path}\n")
        f.write("\n# Archivos extra (no requeridos, revisar si deben eliminarse):\n")
        for path in extras:
            f.write(f"- {path}\n")
    with open(LOG_EXTRA, "w", encoding="utf-8") as f:
        f.write("# Archivos extra/no requeridos encontrados en la estructura\n")
        for path in extras:
            f.write(f"{path}\n")
    print(f"VERIFICACION COMPLETA. Revisa '{LOG_RESULT}' para el resumen y '{LOG_EXTRA}' para archivos extra.")

if __name__ == "__main__":
    main()