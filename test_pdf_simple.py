"""
Script de prueba simple - Extracción de texto de PDF
Primer paso del proyecto Renombrar Facturas
"""

import pdfplumber
from loguru import logger

def extraer_texto_pdf(ruta_pdf):
    """
    Extrae todo el texto de un PDF.
    
    Args:
        ruta_pdf (str): Ruta al archivo PDF
        
    Returns:
        str: Texto extraído del PDF
    """
    logger.info(f"Procesando PDF: {ruta_pdf}")
    
    try:
        with pdfplumber.open(ruta_pdf) as pdf:
            texto_completo = ""
            
            # Iterar sobre cada página
            for i, pagina in enumerate(pdf.pages, 1):
                logger.debug(f"Extrayendo página {i}/{len(pdf.pages)}")
                texto_pagina = pagina.extract_text()
                
                if texto_pagina:
                    texto_completo += f"\n--- PÁGINA {i} ---\n"
                    texto_completo += texto_pagina
                else:
                    logger.warning(f"Página {i} no tiene texto extraíble (puede ser escaneada)")
            
            logger.success(f"✅ Extracción completada: {len(texto_completo)} caracteres")
            return texto_completo
            
    except FileNotFoundError:
        logger.error(f"❌ No se encontró el archivo: {ruta_pdf}")
        return None
    except Exception as e:
        logger.error(f"❌ Error al procesar PDF: {e}")
        return None


def main():
    """Función principal para pruebas."""
    
    logger.info("🚀 Iniciando prueba de extracción de PDF")
    
    # Aquí pon la ruta de tu PDF de prueba
    # Ejemplo: ruta_pdf = "data/samples/factura_ejemplo.pdf"
    ruta_pdf = input("Ingresa la ruta de un PDF para probar: ")
    
    if ruta_pdf.strip():
        texto = extraer_texto_pdf(ruta_pdf)
        
        if texto:
            print("\n" + "="*60)
            print("TEXTO EXTRAÍDO:")
            print("="*60)
            print(texto)
            print("\n" + "="*60)
            
            # Mostrar algunas estadísticas
            lineas = texto.split('\n')
            palabras = texto.split()
            print(f"\n📊 Estadísticas:")
            print(f"   - Caracteres: {len(texto)}")
            print(f"   - Palabras: {len(palabras)}")
            print(f"   - Líneas: {len(lineas)}")
    else:
        logger.warning("No se proporcionó ninguna ruta")
        print("\n💡 Consejo: Coloca un PDF de prueba en data/samples/ y prueba de nuevo")


if __name__ == "__main__":
    main()

