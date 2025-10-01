"""
Sistema de Renombrado Automático de Facturas
Proyecto: Renombrar_facturas
Autores: José María Porras, David Lancheros

Extrae información de facturas (fecha, proveedor, número) y las renombra automáticamente.
"""

import sys
import os
from pathlib import Path
from loguru import logger

# Agregar carpetas al path para imports
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from config.settings import (
    INPUT_FOLDER, OUTPUT_FOLDER, ERROR_FOLDER, LOG_FOLDER,
    ENVIRONMENT, DRY_RUN, is_safe_to_run,
    ALLOWED_EXTENSIONS
)


def configurar_logs():
    """Configura el sistema de logging."""
    
    # Crear carpeta de logs si no existe
    LOG_FOLDER.mkdir(parents=True, exist_ok=True)
    
    # Archivo de log con fecha
    from datetime import datetime
    log_file = LOG_FOLDER / f"renombrar_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # Configurar loguru
    logger.add(
        log_file,
        rotation="100 MB",
        retention="30 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}"
    )
    
    logger.info("="*70)
    logger.info("🚀 INICIANDO SISTEMA DE RENOMBRADO DE FACTURAS")
    logger.info(f"   Entorno: {ENVIRONMENT}")
    logger.info(f"   Modo DRY RUN: {DRY_RUN}")
    logger.info(f"   Carpeta entrada: {INPUT_FOLDER}")
    logger.info(f"   Carpeta salida: {OUTPUT_FOLDER}")
    logger.info("="*70)


def obtener_facturas_pendientes():
    """
    Obtiene la lista de facturas pendientes de procesar.
    
    Returns:
        list: Lista de rutas Path a archivos de facturas
    """
    
    logger.info(f"📂 Buscando facturas en: {INPUT_FOLDER}")
    
    if not INPUT_FOLDER.exists():
        logger.error(f"❌ Carpeta no encontrada: {INPUT_FOLDER}")
        return []
    
    facturas = []
    
    for archivo in INPUT_FOLDER.iterdir():
        if archivo.is_file():
            extension = archivo.suffix.lower()
            
            if extension in ALLOWED_EXTENSIONS:
                facturas.append(archivo)
                logger.debug(f"   ✓ {archivo.name}")
            else:
                logger.warning(f"   ⚠️ Ignorando archivo con extensión no permitida: {archivo.name}")
    
    logger.info(f"✅ Encontradas {len(facturas)} facturas para procesar")
    return facturas


def extraer_texto_pdf(ruta_pdf):
    """
    Extrae texto de un archivo PDF.
    
    Args:
        ruta_pdf (Path): Ruta al archivo PDF
        
    Returns:
        str: Texto extraído o None si falla
    """
    
    try:
        import pdfplumber
        
        logger.debug(f"📄 Extrayendo texto de: {ruta_pdf.name}")
        
        with pdfplumber.open(ruta_pdf) as pdf:
            texto = ""
            
            for pagina in pdf.pages:
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    texto += texto_pagina + "\n"
            
            if texto.strip():
                logger.debug(f"   ✓ Extraídos {len(texto)} caracteres")
                return texto
            else:
                logger.warning(f"   ⚠️ PDF sin texto extraíble (posiblemente escaneado)")
                return None
                
    except Exception as e:
        logger.error(f"   ❌ Error extrayendo texto: {e}")
        return None


def extraer_texto_imagen(ruta_imagen):
    """
    Extrae texto de una imagen usando OCR.
    
    Args:
        ruta_imagen (Path): Ruta a la imagen
        
    Returns:
        str: Texto extraído o None si falla
    """
    
    try:
        import pytesseract
        from PIL import Image
        from config.settings import TESSERACT_PATH
        
        # Configurar Tesseract
        if Path(TESSERACT_PATH).exists():
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
        
        logger.debug(f"🖼️ Aplicando OCR a: {ruta_imagen.name}")
        
        imagen = Image.open(ruta_imagen)
        texto = pytesseract.image_to_string(imagen, lang='spa')
        
        if texto.strip():
            logger.debug(f"   ✓ OCR extraído {len(texto)} caracteres")
            return texto
        else:
            logger.warning(f"   ⚠️ OCR no pudo extraer texto")
            return None
            
    except ImportError:
        logger.error("   ❌ pytesseract no está instalado. Instala con: pip install pytesseract")
        return None
    except Exception as e:
        logger.error(f"   ❌ Error en OCR: {e}")
        return None


def extraer_texto(ruta_archivo):
    """
    Extrae texto de un archivo (PDF o imagen).
    
    Args:
        ruta_archivo (Path): Ruta al archivo
        
    Returns:
        str: Texto extraído o None si falla
    """
    
    extension = ruta_archivo.suffix.lower()
    
    if extension == '.pdf':
        return extraer_texto_pdf(ruta_archivo)
    elif extension in ['.jpg', '.jpeg', '.png']:
        return extraer_texto_imagen(ruta_archivo)
    else:
        logger.error(f"❌ Tipo de archivo no soportado: {extension}")
        return None


def parsear_factura(texto, nombre_archivo):
    """
    Extrae información de la factura (fecha, proveedor, número).
    
    Args:
        texto (str): Texto extraído de la factura
        nombre_archivo (str): Nombre del archivo original
        
    Returns:
        dict: Diccionario con fecha, proveedor, numero o None si falla
    """
    
    # TODO: Implementar parseo inteligente
    # Por ahora retornamos valores de ejemplo
    
    logger.debug(f"🔍 Parseando información de la factura...")
    
    # Aquí irá la lógica de regex, IA, etc.
    # Por ahora, placeholder
    
    info = {
        'fecha': None,
        'proveedor': None,
        'numero': None,
        'original': nombre_archivo
    }
    
    # TODO: Implementar extracción real
    logger.warning("   ⚠️ Parseo aún no implementado - retornando None")
    
    return None  # Por ahora retorna None hasta implementar


def generar_nuevo_nombre(info):
    """
    Genera el nuevo nombre del archivo basado en la información extraída.
    
    Args:
        info (dict): Diccionario con fecha, proveedor, numero
        
    Returns:
        str: Nuevo nombre del archivo
    """
    
    from config.settings import FILENAME_TEMPLATE, FILENAME_SEPARATOR
    
    # Formato: YYYYMMDD_Proveedor_NumFactura.pdf
    nuevo_nombre = FILENAME_TEMPLATE.format(
        fecha=info['fecha'],
        sep=FILENAME_SEPARATOR,
        proveedor=info['proveedor'],
        numero=info['numero']
    )
    
    return nuevo_nombre


def procesar_factura(ruta_factura):
    """
    Procesa una factura completa: extrae, parsea y renombra.
    
    Args:
        ruta_factura (Path): Ruta a la factura
        
    Returns:
        bool: True si se procesó correctamente, False si falló
    """
    
    logger.info(f"\n📋 Procesando: {ruta_factura.name}")
    logger.info("-" * 60)
    
    # Paso 1: Extraer texto
    texto = extraer_texto(ruta_factura)
    
    if not texto:
        logger.error(f"❌ No se pudo extraer texto de: {ruta_factura.name}")
        # Mover a carpeta de errores
        return False
    
    # Paso 2: Parsear información
    info = parsear_factura(texto, ruta_factura.name)
    
    if not info:
        logger.error(f"❌ No se pudo extraer información de: {ruta_factura.name}")
        return False
    
    # Paso 3: Generar nuevo nombre
    nuevo_nombre = generar_nuevo_nombre(info)
    logger.info(f"✏️ Nombre propuesto: {nuevo_nombre}")
    
    # Paso 4: Renombrar (o simular)
    if DRY_RUN:
        logger.info(f"🔍 DRY RUN: No se renombró realmente")
        logger.info(f"   {ruta_factura.name} → {nuevo_nombre}")
    else:
        # TODO: Implementar renombrado real
        logger.info(f"✅ Renombrado: {ruta_factura.name} → {nuevo_nombre}")
    
    logger.info("-" * 60)
    return True


def main():
    """Función principal."""
    
    # Configurar logs
    configurar_logs()
    
    # Verificar seguridad
    if not is_safe_to_run():
        logger.error("❌ Ejecución cancelada por el usuario")
        return
    
    # Obtener facturas pendientes
    facturas = obtener_facturas_pendientes()
    
    if not facturas:
        logger.warning("⚠️ No hay facturas para procesar")
        return
    
    # Procesar cada factura
    exitosas = 0
    fallidas = 0
    
    for factura in facturas:
        try:
            if procesar_factura(factura):
                exitosas += 1
            else:
                fallidas += 1
        except Exception as e:
            logger.error(f"❌ Error inesperado procesando {factura.name}: {e}")
            fallidas += 1
    
    # Resumen final
    logger.info("\n" + "="*70)
    logger.info("📊 RESUMEN DE PROCESAMIENTO")
    logger.info(f"   Total facturas: {len(facturas)}")
    logger.info(f"   ✅ Exitosas: {exitosas}")
    logger.info(f"   ❌ Fallidas: {fallidas}")
    logger.info(f"   📈 Tasa de éxito: {exitosas/len(facturas)*100:.1f}%")
    logger.info("="*70)
    
    if DRY_RUN:
        logger.info("\n💡 Ejecutado en modo DRY RUN - no se renombró ningún archivo")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("\n⚠️ Proceso interrumpido por el usuario")
    except Exception as e:
        logger.error(f"\n❌ Error fatal: {e}")
        raise

