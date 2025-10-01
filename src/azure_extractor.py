"""
Extracción de datos de facturas usando Azure Document Intelligence (Form Recognizer)
"""

import os
from pathlib import Path
from loguru import logger
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


def extraer_con_azure(ruta_pdf):
    """
    Extrae datos de factura usando Azure Document Intelligence.
    
    Args:
        ruta_pdf (Path): Ruta al archivo PDF
        
    Returns:
        dict: Diccionario con fecha, proveedor, numero o None si falla
    """
    
    try:
        from azure.ai.formrecognizer import DocumentAnalysisClient
        from azure.core.credentials import AzureKeyCredential
        from datetime import datetime
        
        # Obtener credenciales desde variables de entorno
        endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
        api_key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
        
        if not endpoint or not api_key:
            logger.warning("   ⚠️ Credenciales de Azure no configuradas")
            logger.info("   💡 Configura AZURE_FORM_RECOGNIZER_ENDPOINT y AZURE_FORM_RECOGNIZER_KEY")
            return None
        
        logger.debug("   🔷 Usando Azure Document Intelligence...")
        
        # Crear cliente
        client = DocumentAnalysisClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key)
        )
        
        # Analizar documento con modelo pre-entrenado para facturas
        with open(ruta_pdf, "rb") as f:
            poller = client.begin_analyze_document(
                model_id="prebuilt-invoice",  # Modelo específico para facturas
                document=f
            )
        
        result = poller.result()
        
        if not result.documents:
            logger.warning("   ⚠️ Azure no detectó facturas en el documento")
            return None
        
        # Obtener primera factura detectada
        invoice = result.documents[0]
        fields = invoice.fields
        
        # Extraer datos
        info = {
            'fecha': None,
            'proveedor': None,
            'numero': None,
            'cif': None,
            'confianza': {}
        }
        
        # Fecha de factura
        if 'InvoiceDate' in fields and fields['InvoiceDate'].value:
            fecha_obj = fields['InvoiceDate'].value
            if isinstance(fecha_obj, datetime):
                info['fecha'] = fecha_obj.strftime('%Y%m%d')
            else:
                # Intentar parsear si es string
                try:
                    fecha_obj = datetime.fromisoformat(str(fecha_obj))
                    info['fecha'] = fecha_obj.strftime('%Y%m%d')
                except:
                    pass
            
            if info['fecha']:
                confianza = fields['InvoiceDate'].confidence
                info['confianza']['fecha'] = confianza
                logger.debug(f"   ✓ Fecha: {info['fecha']} (confianza: {confianza:.1%})")
        
        # Proveedor (VendorName)
        if 'VendorName' in fields and fields['VendorName'].value:
            proveedor = str(fields['VendorName'].value).strip()
            # Limpiar para nombre de archivo
            import re
            proveedor = re.sub(r'\s+', '_', proveedor)
            proveedor = re.sub(r'[^\w\s-]', '', proveedor)
            info['proveedor'] = proveedor[:50]  # Limitar longitud
            
            confianza = fields['VendorName'].confidence
            info['confianza']['proveedor'] = confianza
            logger.debug(f"   ✓ Proveedor: {proveedor} (confianza: {confianza:.1%})")
        
        # Número de factura
        if 'InvoiceId' in fields and fields['InvoiceId'].value:
            numero = str(fields['InvoiceId'].value).strip()
            info['numero'] = numero
            
            confianza = fields['InvoiceId'].confidence
            info['confianza']['numero'] = confianza
            logger.debug(f"   ✓ Número: {numero} (confianza: {confianza:.1%})")
        
        # CIF/NIF del proveedor (opcional)
        if 'VendorTaxId' in fields and fields['VendorTaxId'].value:
            cif = str(fields['VendorTaxId'].value).strip()
            info['cif'] = cif.replace('-', '').replace('.', '').replace(' ', '')
            logger.debug(f"   ✓ CIF: {info['cif']}")
        
        # Validar que tengamos al menos 2 campos
        campos_validos = sum([
            bool(info['fecha']),
            bool(info['proveedor']),
            bool(info['numero'])
        ])
        
        if campos_validos >= 2:
            logger.success(f"   ✓ Azure extrajo {campos_validos}/3 campos")
            return info
        else:
            logger.warning(f"   ⚠️ Azure solo extrajo {campos_validos}/3 campos")
            return None
            
    except ImportError:
        logger.error("   ❌ azure-ai-formrecognizer no instalado")
        logger.info("   💡 Instala con: pip install azure-ai-formrecognizer")
        return None
    except Exception as e:
        logger.error(f"   ❌ Error en Azure Document Intelligence: {e}")
        return None


def esta_azure_disponible():
    """
    Verifica si Azure Document Intelligence está configurado.
    
    Returns:
        bool: True si está disponible
    """
    try:
        endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
        api_key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
        
        if endpoint and api_key:
            # Verificar que la librería esté instalada
            import azure.ai.formrecognizer
            return True
        return False
    except ImportError:
        return False

