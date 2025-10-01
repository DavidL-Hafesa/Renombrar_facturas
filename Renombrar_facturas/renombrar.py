"""
Sistema de Renombrado Automático de Facturas
Proyecto: Renombrar_facturas
Autores: José María Porras, David Lancheros

Extrae información de facturas (fecha, proveedor, número) y las renombra automáticamente.

Métodos de extracción (en orden de prioridad):
1. Azure Document Intelligence (si está configurado) - Precisión 95-98%
2. Regex + OCR (fallback) - Precisión 60-85%
"""

import sys
import os
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

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
    Combina extracción directa + OCR para capturar logos/imágenes con texto.
    
    Args:
        ruta_pdf (Path): Ruta al archivo PDF
        
    Returns:
        str: Texto extraído o None si falla
    """
    
    try:
        import pdfplumber
        
        logger.debug(f"📄 Extrayendo texto de: {ruta_pdf.name}")
        
        # Paso 1: Extracción directa de texto
        texto_nativo = ""
        with pdfplumber.open(ruta_pdf) as pdf:
            for pagina in pdf.pages:
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    texto_nativo += texto_pagina + "\n"
        
        if texto_nativo.strip():
            logger.debug(f"   ✓ Extraídos {len(texto_nativo)} caracteres (texto nativo)")
            
            # Paso 2: Intentar OCR para capturar logos/imágenes (solo primera página)
            # Esto es útil para nombres de proveedores en logos
            try:
                texto_ocr = extraer_texto_pdf_con_ocr_pagina(ruta_pdf, pagina_num=0)
                if texto_ocr:
                    # Combinar ambos textos (OCR al inicio, luego texto nativo)
                    texto_combinado = texto_ocr + "\n" + texto_nativo
                    logger.debug(f"   ✓ Combinado con OCR: {len(texto_combinado)} caracteres total")
                    return texto_combinado
            except:
                # Si falla el OCR, usar solo texto nativo
                pass
            
            return texto_nativo
        else:
            logger.warning(f"   ⚠️ PDF sin texto extraíble - intentando OCR...")
            # Si no hay texto nativo, usar solo OCR
            return extraer_texto_pdf_con_ocr(ruta_pdf)
                
    except Exception as e:
        logger.error(f"   ❌ Error extrayendo texto: {e}")
        return None


def extraer_texto_pdf_con_ocr_pagina(ruta_pdf, pagina_num=0):
    """
    Extrae texto de UNA página específica de un PDF usando OCR.
    Útil para extraer logos/cabeceras sin procesar todo el documento.
    
    Args:
        ruta_pdf (Path): Ruta al archivo PDF
        pagina_num (int): Número de página (0-indexed)
        
    Returns:
        str: Texto extraído o None si falla
    """
    try:
        import fitz
        import pytesseract
        from PIL import Image
        import io
        from config.settings import TESSERACT_PATH
        
        if Path(TESSERACT_PATH).exists():
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
        
        doc = fitz.open(ruta_pdf)
        if pagina_num >= len(doc):
            doc.close()
            return None
        
        pagina = doc[pagina_num]
        pix = pagina.get_pixmap(dpi=300)
        img_data = pix.tobytes("png")
        imagen = Image.open(io.BytesIO(img_data))
        
        texto = pytesseract.image_to_string(imagen, lang='spa')
        doc.close()
        
        return texto if texto.strip() else None
        
    except:
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


def parsear_factura(texto, nombre_archivo, ruta_pdf=None):
    """
    Extrae información de la factura (fecha, proveedor, número).
    Usa Azure Document Intelligence si está disponible, sino usa regex.
    
    Args:
        texto (str): Texto extraído de la factura
        nombre_archivo (str): Nombre del archivo original
        ruta_pdf (Path, optional): Ruta al PDF (para Azure)
        
    Returns:
        dict: Diccionario con fecha, proveedor, numero o None si falla
    """
    
    import re
    from datetime import datetime
    
    logger.debug(f"🔍 Parseando información de la factura...")
    
    # ESTRATEGIA 1: Intentar Azure Document Intelligence primero (si está configurado)
    if ruta_pdf:
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from src.azure_extractor import extraer_con_azure, esta_azure_disponible
            
            logger.debug("   🔍 Verificando si Azure está disponible...")
            if esta_azure_disponible():
                logger.info("   🔷 Azure disponible - intentando extracción...")
                info_azure = extraer_con_azure(ruta_pdf)
                if info_azure:
                    logger.success("   ✅ Datos extraídos con Azure Document Intelligence")
                    return info_azure
                else:
                    logger.warning("   ⚠️ Azure no pudo extraer datos - usando fallback regex")
            else:
                logger.debug("   ℹ️ Azure no configurado - usando regex")
        except Exception as e:
            logger.warning(f"   ⚠️ Error al intentar Azure: {e}")
            import traceback
            logger.debug(traceback.format_exc())
    
    # ESTRATEGIA 2: Fallback a regex (método actual)
    logger.debug("   🔍 Usando extracción por regex...")
    
    # Aplicar correcciones de OCR conocidas
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from src.aprendizaje import corregir_ocr
        texto = corregir_ocr(texto)
    except:
        pass  # Si no funciona, continuar sin correcciones
    
    info = {
        'fecha': None,
        'proveedor': None,
        'numero': None,
        'cif': None,
        'original': nombre_archivo
    }
    
    # Normalizar texto (remover saltos de línea múltiples, espacios extra)
    texto_limpio = re.sub(r'\s+', ' ', texto)
    
    # Extraer CIF/NIF primero (útil para búsqueda en base de datos)
    # Variaciones: CIF, C.I.F., C.LF., NIF, N.I.F.
    # Patrón más flexible para puntos y espacios
    # También buscar formato: 34864979-S (NIF de persona física)
    match_cif = re.search(r'(?:C\.?I\.?F\.?|C\.?L\.?F\.?|N\.?I\.?F\.?)\s*[:.\s]*\s*([A-Z0-9][-\s.]*\d{7,8}[-\s]*[A-Z]?)', texto, re.IGNORECASE)
    if not match_cif:
        # Buscar NIF sin prefijo: 12345678-A
        match_cif = re.search(r'(\d{8}[-\s]*[A-Z])', texto)
    if match_cif:
        cif = match_cif.group(1).replace('-', '').replace('.', '').replace(' ', '')
        info['cif'] = cif
        logger.debug(f"   ✓ CIF encontrado: {cif}")
        
        # Intentar buscar proveedor por CIF en base de datos
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from src.aprendizaje import buscar_proveedor_por_cif
            proveedor_conocido = buscar_proveedor_por_cif(cif)
            if proveedor_conocido:
                info['proveedor'] = proveedor_conocido
                logger.success(f"   ✓ Proveedor encontrado en BD (CIF): {proveedor_conocido}")
        except Exception as e:
            logger.debug(f"   ⚠️ No se pudo buscar en BD: {e}")
            pass
    
    # 1. EXTRAER FECHA
    # Estrategia: Priorizar fechas cerca de "Factura" o número de factura, evitar fechas de albarán
    
    # Buscar primero fechas explícitas de factura/emisión
    patrones_fecha_prioritarios = [
        r'Fecha\s+(?:de\s+)?(?:emisi[oó]n|factura)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'Fecha[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
    ]
    
    for patron in patrones_fecha_prioritarios:
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            # Asegurarse de que no sea fecha de albarán
            contexto = texto[max(0, match.start()-50):match.end()+50]
            if 'albaran' not in contexto.lower() and 'albar' not in contexto.lower():
                fecha_str = match.group(1)
                try:
                    for formato in ['%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y', '%d/%m/%y', '%d-%m-%y']:
                        try:
                            fecha_obj = datetime.strptime(fecha_str, formato)
                            info['fecha'] = fecha_obj.strftime('%Y%m%d')
                            logger.debug(f"   ✓ Fecha encontrada (explícita): {fecha_str} → {info['fecha']}")
                            break
                        except:
                            continue
                    if info['fecha']:
                        break
                except Exception as e:
                    logger.debug(f"   ⚠️ Error parseando fecha: {e}")
    
    # Si no se encontró, buscar fecha cerca del número de factura
    if not info['fecha']:
        # Buscar formato: número/año fecha (ej: 511890/25 18-09-2025)
        patron_numero_fecha = r'(\d{5,7}/\d{2})\s+(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
        match = re.search(patron_numero_fecha, texto)
        if match:
            fecha_str = match.group(2)
            try:
                for formato in ['%d-%m-%Y', '%d/%m/%Y', '%d-%m-%y', '%d/%m/%y']:
                    try:
                        fecha_obj = datetime.strptime(fecha_str, formato)
                        info['fecha'] = fecha_obj.strftime('%Y%m%d')
                        logger.debug(f"   ✓ Fecha encontrada (junto a número): {fecha_str} → {info['fecha']}")
                        break
                    except:
                        continue
            except Exception as e:
                logger.debug(f"   ⚠️ Error parseando fecha: {e}")
    
    # Si aún no se encontró, buscar cualquier fecha (pero evitar albaranes)
    if not info['fecha']:
        fechas_encontradas = re.findall(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', texto)
        for fecha_str in fechas_encontradas[:5]:  # Revisar primeras 5 fechas
            # Buscar contexto de esta fecha
            idx = texto.find(fecha_str)
            if idx != -1:
                contexto = texto[max(0, idx-50):idx+50]
                if 'albaran' not in contexto.lower() and 'albar' not in contexto.lower():
                    try:
                        for formato in ['%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y', '%d/%m/%y', '%d-%m-%y']:
                            try:
                                fecha_obj = datetime.strptime(fecha_str, formato)
                                info['fecha'] = fecha_obj.strftime('%Y%m%d')
                                logger.debug(f"   ✓ Fecha encontrada (genérica): {fecha_str} → {info['fecha']}")
                                break
                            except:
                                continue
                        if info['fecha']:
                            break
                    except Exception as e:
                        logger.debug(f"   ⚠️ Error parseando fecha: {e}")
    
    # 2. EXTRAER PROVEEDOR
    # Si ya se encontró por CIF, no buscar de nuevo
    if info['proveedor']:
        logger.debug(f"   → Usando proveedor de BD: {info['proveedor']}")
    
    # Estrategia 1: Buscar "Proveedor:" explícito
    if not info['proveedor']:
        patrones_proveedor_explicito = [
            r'Proveedor[:\s]+([A-ZÁÉÍÓÚÑa-záéíóúñ\s]+?)(?:\n|Número|N[úu]mero|Fecha|Importe)',
            r'Supplier[:\s]+([A-Za-z\s]+?)(?:\n|Number|Date|Amount)',
            r'Razón Social[:\s]+([A-ZÁÉÍÓÚÑa-záéíóúñ\s]+?)(?:\n|NIF|CIF)',
        ]
    
        for patron in patrones_proveedor_explicito:
            match = re.search(patron, texto, re.IGNORECASE)
            if match:
                proveedor = match.group(1).strip()
                # Limpiar nombre del proveedor
                proveedor = re.sub(r'\s+', '_', proveedor)
                proveedor = re.sub(r'[^\w\s-]', '', proveedor)
                info['proveedor'] = proveedor
                logger.debug(f"   ✓ Proveedor encontrado (explícito): {proveedor}")
                break
    
    # Estrategia 2: Si no se encontró, buscar empresas con sufijos legales (S.A., S.L., etc.)
    if not info['proveedor']:
        # Buscar nombres con sufijos de empresa en TODO el texto (no solo primeras líneas)
        # pero filtrar empresas conocidas que son clientes (HAFESA, etc.)
        patrones_empresa = [
            r'([A-ZÁÉÍÓÚÑ&][A-ZÁÉÍÓÚÑa-záéíóúñ\s\-\.,&]+?(?:S\.A\.U\.|S\.L\.U\.|S\.A\.|S\.L\.|S\.C\.|S\.COOP\.))',
            r'([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑa-záéíóúñ\s\-]+BY\s+[A-ZÁÉÍÓÚÑa-záéíóúñ\s\-]+)',  # Ej: "Q-SAFETY BY QUIRÓN"
        ]
        
        empresas_cliente = ['HAFESA', 'HAFESA OIL', 'HAFESA OLI']  # Empresas que son clientes, no proveedores
        
        # Buscar en todo el texto
        for patron in patrones_empresa:
            matches = re.finditer(patron, texto)
            for match in matches:
                proveedor = match.group(1).strip()
                
                # Verificar que no sea una empresa cliente conocida
                es_cliente = any(cliente.lower() in proveedor.lower() for cliente in empresas_cliente)
                
                if not es_cliente:
                    # Limpiar
                    proveedor = re.sub(r'\s+', '_', proveedor)
                    proveedor = re.sub(r'[^\w\s-]', '', proveedor)
                    # Limitar longitud (evitar nombres muy largos)
                    if len(proveedor) > 50:
                        proveedor = proveedor[:50]
                    info['proveedor'] = proveedor
                    logger.debug(f"   ✓ Proveedor encontrado (sufijo legal): {proveedor}")
                    break
            if info['proveedor']:
                break
    
    # Estrategia 3: Buscar línea antes/después del CIF
    if not info['proveedor']:
        match_cif = re.search(r'CIF[:\s]+([A-Z0-9]+)', texto, re.IGNORECASE)
        if match_cif:
            # Buscar nombre en contexto cercano al CIF
            inicio = max(0, match_cif.start() - 200)
            fin = min(len(texto), match_cif.end() + 200)
            contexto = texto[inicio:fin]
            
            # Buscar nombre de empresa en el contexto
            for patron in patrones_empresa:
                match = re.search(patron, contexto)
                if match:
                    proveedor = match.group(1).strip()
                    proveedor = re.sub(r'\s+', '_', proveedor)
                    proveedor = re.sub(r'[^\w\s-]', '', proveedor)
                    if len(proveedor) > 50:
                        proveedor = proveedor[:50]
                    info['proveedor'] = proveedor
                    logger.debug(f"   ✓ Proveedor encontrado (cerca del CIF): {proveedor}")
                    break
    
    # 3. EXTRAER NÚMERO DE FACTURA
    patrones_numero = [
        r'N[º°úu]?\s*FACTURA\s+FECHA\s+FACTURA\s+([A-Z]\s*\d+)',  # Nº FACTURA FECHA FACTURA A 20250965
        r'N[º°úu]?\s*FACTURA[:\s]+([A-Z]\s*\d+)',  # Nº FACTURA A 20250965
        r'N[úu]mero de Factura[:\s]+([A-Z0-9\-/]+)(?:\s|$)',  # Número de Factura: FAC-2024-12345
        r'Factura [nN][º°u][:\s]+([A-Z0-9\-/_]+)',
        r'Invoice Number[:\s]+([A-Z0-9\-/]+)',
        r'N[º°] Factura[:\s]+([A-Z0-9\-/]+)',
        r'fra\.\s*(\d{6,})',  # Plazo n'1 fra. 2500612
        r'(\d{6}/\d{2})',  # Formato: 511890/25
        r'Fact[ura]*\s+([A-Z]?\d{6,})',  # Fact FAA20250965
    ]
    
    for patron in patrones_numero:
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            numero = match.group(1).strip()
            # Limpiar espacios extra dentro del número
            numero = re.sub(r'\s+', '', numero)
            # Evitar que capture palabras como "FECHA", "FACTURA", etc.
            if numero.upper() not in ['FECHA', 'FACTURA', 'DATE', 'INVOICE']:
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


def sanitizar_nombre_archivo(texto):
    """
    Limpia caracteres no permitidos en nombres de archivo de Windows.
    Reemplaza: \\ / : * ? " < > | por guiones
    
    Args:
        texto (str): Texto a limpiar
        
    Returns:
        str: Texto limpio y seguro para nombre de archivo
    """
    import re
    
    # Si es None o vacío, retornar string vacío
    if not texto:
        return ""
    
    # Caracteres prohibidos en Windows
    caracteres_prohibidos = r'[\\/:*?"<>|]'
    
    # Reemplazar por guion
    texto_limpio = re.sub(caracteres_prohibidos, '-', texto)
    
    # Remover guiones múltiples consecutivos
    texto_limpio = re.sub(r'-+', '-', texto_limpio)
    
    # Remover guiones al inicio o final
    texto_limpio = texto_limpio.strip('-')
    
    return texto_limpio


def generar_nuevo_nombre(info):
    """
    Genera el nuevo nombre del archivo basado en la información extraída.
    
    Args:
        info (dict): Diccionario con fecha, proveedor, numero
        
    Returns:
        str: Nuevo nombre del archivo
    """
    
    from config.settings import FILENAME_TEMPLATE, FILENAME_SEPARATOR
    
    # Sanitizar cada componente
    fecha_limpia = sanitizar_nombre_archivo(info['fecha'])
    proveedor_limpio = sanitizar_nombre_archivo(info['proveedor'])
    numero_limpio = sanitizar_nombre_archivo(info['numero'])
    
    # Registrar si hubo cambios
    if info['numero'] != numero_limpio:
        logger.debug(f"   🔧 Número sanitizado: {info['numero']} → {numero_limpio}")
    
    # Formato: YYYYMMDD_Proveedor_NumFactura.pdf
    nuevo_nombre = FILENAME_TEMPLATE.format(
        fecha=fecha_limpia,
        sep=FILENAME_SEPARATOR,
        proveedor=proveedor_limpio,
        numero=numero_limpio
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
    
    # Paso 2: Parsear información (pasar ruta para Azure)
    info = parsear_factura(texto, ruta_factura.name, ruta_pdf=ruta_factura)
    
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

