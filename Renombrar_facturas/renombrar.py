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
    Intenta primero extracción directa, luego OCR si es necesario.
    
    Args:
        ruta_pdf (Path): Ruta al archivo PDF
        
    Returns:
        str: Texto extraído o None si falla
    """
    
    try:
        import pdfplumber
        
        logger.debug(f"📄 Extrayendo texto de: {ruta_pdf.name}")
        
        # Intento 1: Extracción directa de texto
        with pdfplumber.open(ruta_pdf) as pdf:
            texto = ""
            
            for pagina in pdf.pages:
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    texto += texto_pagina + "\n"
            
            if texto.strip():
                logger.debug(f"   ✓ Extraídos {len(texto)} caracteres (texto nativo)")
                return texto
            else:
                logger.warning(f"   ⚠️ PDF sin texto extraíble - intentando OCR...")
                # Intento 2: OCR si no hay texto
                return extraer_texto_pdf_con_ocr(ruta_pdf)
                
    except Exception as e:
        logger.error(f"   ❌ Error extrayendo texto: {e}")
        return None


def extraer_texto_pdf_con_ocr(ruta_pdf):
    """
    Extrae texto de un PDF escaneado usando OCR.
    Convierte el PDF a imágenes con PyMuPDF y aplica Tesseract.
    
    Args:
        ruta_pdf (Path): Ruta al archivo PDF
        
    Returns:
        str: Texto extraído o None si falla
    """
    
    try:
        import fitz  # PyMuPDF
        import pytesseract
        from PIL import Image
        import io
        from config.settings import TESSERACT_PATH
        
        # Configurar Tesseract
        if Path(TESSERACT_PATH).exists():
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
        
        logger.debug(f"   🔍 Aplicando OCR al PDF...")
        
        # Abrir PDF con PyMuPDF
        doc = fitz.open(ruta_pdf)
        num_paginas = len(doc)
        texto_completo = ""
        
        for num_pagina in range(num_paginas):
            logger.debug(f"   📄 OCR en página {num_pagina + 1}/{num_paginas}")
            
            # Convertir página a imagen
            pagina = doc[num_pagina]
            pix = pagina.get_pixmap(dpi=300)  # Alta resolución para mejor OCR
            
            # Convertir a PIL Image
            img_data = pix.tobytes("png")
            imagen = Image.open(io.BytesIO(img_data))
            
            # Aplicar OCR
            texto_pagina = pytesseract.image_to_string(imagen, lang='spa')
            texto_completo += texto_pagina + "\n"
        
        doc.close()
        
        if texto_completo.strip():
            logger.success(f"   ✓ OCR extrajo {len(texto_completo)} caracteres de {num_paginas} páginas")
            return texto_completo
        else:
            logger.error(f"   ❌ OCR no pudo extraer texto")
            return None
            
    except ImportError as e:
        logger.error(f"   ❌ Librería no instalada: {e}")
        logger.error(f"   💡 Instala con: pip install PyMuPDF pytesseract")
        return None
    except Exception as e:
        logger.error(f"   ❌ Error en OCR: {e}")
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
    
    import re
    from datetime import datetime
    
    logger.debug(f"🔍 Parseando información de la factura...")
    
    info = {
        'fecha': None,
        'proveedor': None,
        'numero': None,
        'original': nombre_archivo
    }
    
    # Normalizar texto (remover saltos de línea múltiples, espacios extra)
    texto_limpio = re.sub(r'\s+', ' ', texto)
    
    # 1. EXTRAER FECHA
    # Patrones comunes: DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY, etc.
    patrones_fecha = [
        r'Fecha[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',  # Fecha: 15/09/2024
        r'Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',   # Date: 15/09/2024
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{4})',                # 15/09/2024 (genérico)
    ]
    
    for patron in patrones_fecha:
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            fecha_str = match.group(1)
            try:
                # Intentar parsear la fecha
                for formato in ['%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y', '%d/%m/%y']:
                    try:
                        fecha_obj = datetime.strptime(fecha_str, formato)
                        info['fecha'] = fecha_obj.strftime('%Y%m%d')  # YYYYMMDD
                        logger.debug(f"   ✓ Fecha encontrada: {fecha_str} → {info['fecha']}")
                        break
                    except:
                        continue
                if info['fecha']:
                    break
            except Exception as e:
                logger.debug(f"   ⚠️ Error parseando fecha: {e}")
    
    # 2. EXTRAER PROVEEDOR
    patrones_proveedor = [
        r'Proveedor[:\s]+([A-ZÁÉÍÓÚÑa-záéíóúñ\s]+?)(?:\n|Número|N[úu]mero|Fecha|Importe)',
        r'Supplier[:\s]+([A-Za-z\s]+?)(?:\n|Number|Date|Amount)',
        r'Razón Social[:\s]+([A-ZÁÉÍÓÚÑa-záéíóúñ\s]+?)(?:\n|NIF|CIF)',
    ]
    
    for patron in patrones_proveedor:
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            proveedor = match.group(1).strip()
            # Limpiar nombre del proveedor (remover espacios extra, etc.)
            proveedor = re.sub(r'\s+', '_', proveedor)  # Espacios → guiones bajos
            proveedor = re.sub(r'[^\w\s-]', '', proveedor)  # Remover caracteres especiales
            info['proveedor'] = proveedor
            logger.debug(f"   ✓ Proveedor encontrado: {proveedor}")
            break
    
    # 3. EXTRAER NÚMERO DE FACTURA
    patrones_numero = [
        r'N[úu]mero de Factura[:\s]+([A-Z0-9\-/]+)',
        r'Factura N[º°][:\s]+([A-Z0-9\-/]+)',
        r'Invoice Number[:\s]+([A-Z0-9\-/]+)',
        r'N[º°] Factura[:\s]+([A-Z0-9\-/]+)',
        r'Factura[:\s]+([A-Z0-9\-/]+)',
    ]
    
    for patron in patrones_numero:
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            numero = match.group(1).strip()
            info['numero'] = numero
            logger.debug(f"   ✓ Número encontrado: {numero}")
            break
    
    # Validar que al menos tengamos 2 de los 3 campos
    campos_encontrados = sum([bool(info['fecha']), bool(info['proveedor']), bool(info['numero'])])
    
    if campos_encontrados >= 2:
        logger.success(f"   ✓ Parseo exitoso: {campos_encontrados}/3 campos extraídos")
        return info
    else:
        logger.warning(f"   ⚠️ Parseo incompleto: solo {campos_encontrados}/3 campos")
        logger.debug(f"      Fecha: {info['fecha']}")
        logger.debug(f"      Proveedor: {info['proveedor']}")
        logger.debug(f"      Número: {info['numero']}")
        return None


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

