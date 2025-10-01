"""
Configuración del proyecto Renombrar Facturas
"""

import os
from pathlib import Path

# ============================================
# CONFIGURACIÓN DE ENTORNOS
# ============================================

# Detectar entorno
ENVIRONMENT = os.getenv("ENV", "development")  # development | testing | production

# Rutas base del proyecto
BASE_DIR = Path(__file__).parent.parent

# ============================================
# ENTORNO DE DESARROLLO (Local)
# ============================================
if ENVIRONMENT == "development":
    INPUT_FOLDER = BASE_DIR / "data" / "samples"
    OUTPUT_FOLDER = BASE_DIR / "data" / "output"
    ERROR_FOLDER = BASE_DIR / "data" / "errors"
    LOG_FOLDER = BASE_DIR / "logs"
    
    # Modo seguro: NO renombra, solo simula
    DRY_RUN = True
    
    print("[DESARROLLO] Usando facturas de muestra locales")

# ============================================
# ENTORNO DE TESTING (NAS Test)
# ============================================
elif ENVIRONMENT == "testing":
    INPUT_FOLDER = Path(r"\\NAS-HAFESA\Facturas_TEST\input")
    OUTPUT_FOLDER = Path(r"\\NAS-HAFESA\Facturas_TEST\output")
    ERROR_FOLDER = Path(r"\\NAS-HAFESA\Facturas_TEST\errors")
    LOG_FOLDER = BASE_DIR / "logs"
    
    # Modo seguro: NO renombra, solo simula
    DRY_RUN = True
    
    print("[TESTING] Usando NAS de pruebas (DRY RUN)")

# ============================================
# ENTORNO DE PRODUCCIÓN (NAS Real)
# ============================================
elif ENVIRONMENT == "production":
    INPUT_FOLDER = Path(r"\\NAS-HAFESA\Facturas\input")
    OUTPUT_FOLDER = Path(r"\\NAS-HAFESA\Facturas\output")
    ERROR_FOLDER = Path(r"\\NAS-HAFESA\Facturas\errors")
    LOG_FOLDER = Path(r"\\NAS-HAFESA\Facturas\logs")
    
    # ADVERTENCIA: Solo activar cuando esté 100% probado
    DRY_RUN = os.getenv("ALLOW_PRODUCTION", "false").lower() == "true"
    
    if not DRY_RUN:
        print("[PRODUCCION] MODO ACTIVO - RENOMBRARA ARCHIVOS REALES!")
        print("   Para activar, exporta: $env:ALLOW_PRODUCTION='true'")
    else:
        print("[PRODUCCION] Modo DRY RUN - Solo vista previa")

# ============================================
# CONFIGURACIÓN GENERAL
# ============================================

# Formato de nomenclatura
DATE_FORMAT = "%Y%m%d"
FILENAME_SEPARATOR = "_"
FILENAME_TEMPLATE = "{fecha}{sep}{proveedor}{sep}{numero}.pdf"

# Tesseract OCR
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSERACT_LANG = "spa"

# Procesamiento
MAX_WORKERS = 4
PROCESSING_TIMEOUT = 120  # segundos

# Logging
LOG_LEVEL = "INFO"
LOG_ROTATION = "100 MB"
LOG_RETENTION = "30 days"

# Extensiones permitidas
ALLOWED_EXTENSIONS = [".pdf", ".jpg", ".jpeg", ".png"]

# ============================================
# VALIDACIONES
# ============================================

def validate_config():
    """Valida que la configuración sea correcta."""
    
    errors = []
    
    # Verificar carpetas en desarrollo
    if ENVIRONMENT == "development":
        if not INPUT_FOLDER.exists():
            INPUT_FOLDER.mkdir(parents=True, exist_ok=True)
            print(f"[OK] Creada carpeta: {INPUT_FOLDER}")
        
        if not OUTPUT_FOLDER.exists():
            OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
            print(f"[OK] Creada carpeta: {OUTPUT_FOLDER}")
        
        if not ERROR_FOLDER.exists():
            ERROR_FOLDER.mkdir(parents=True, exist_ok=True)
            print(f"[OK] Creada carpeta: {ERROR_FOLDER}")
    
    # Verificar acceso a NAS en testing/production
    elif ENVIRONMENT in ["testing", "production"]:
        if not INPUT_FOLDER.exists():
            errors.append(f"[ERROR] No se puede acceder a: {INPUT_FOLDER}")
    
    # Verificar Tesseract
    if not Path(TESSERACT_PATH).exists():
        print(f"[ADVERTENCIA] Tesseract no encontrado en: {TESSERACT_PATH}")
        print("   El OCR de imagenes/PDFs escaneados no funcionara")
    
    return errors


# ============================================
# MODO SEGURO (Safety switch)
# ============================================

def is_safe_to_run():
    """
    Verifica que sea seguro ejecutar el script.
    Evita accidentes en producción.
    """
    
    if ENVIRONMENT == "production" and not DRY_RUN:
        response = input("\n!!! ADVERTENCIA !!!\n"
                        "Estas a punto de RENOMBRAR archivos en PRODUCCION.\n"
                        "Estas ABSOLUTAMENTE seguro? (escribe 'SI ESTOY SEGURO'): ")
        
        return response == "SI ESTOY SEGURO"
    
    return True


# Validar al importar
if __name__ != "__main__":
    errors = validate_config()
    if errors:
        print("\n".join(errors))
        raise Exception("Configuración inválida")

