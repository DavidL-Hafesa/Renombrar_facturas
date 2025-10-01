"""
Sistema de aprendizaje incremental para proveedores
Guarda y reutiliza información validada por el usuario
"""

import json
from pathlib import Path
from datetime import datetime

PROVEEDORES_FILE = Path(__file__).parent.parent / "config" / "proveedores.json"


def cargar_proveedores():
    """Carga el archivo de proveedores aprendidos."""
    if PROVEEDORES_FILE.exists():
        with open(PROVEEDORES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "proveedores_por_cif": {},
        "proveedores_por_patron": {},
        "correcciones_ocr": {}
    }


def guardar_proveedores(data):
    """Guarda el archivo de proveedores."""
    with open(PROVEEDORES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def buscar_proveedor_por_cif(cif):
    """
    Busca un proveedor conocido por su CIF.
    
    Args:
        cif (str): CIF del proveedor
        
    Returns:
        str: Nombre del proveedor o None
    """
    data = cargar_proveedores()
    
    # Limpiar CIF (remover guiones, puntos)
    cif_limpio = cif.replace('-', '').replace('.', '').upper()
    
    if cif_limpio in data['proveedores_por_cif']:
        return data['proveedores_por_cif'][cif_limpio].get('alias') or data['proveedores_por_cif'][cif_limpio]['nombre']
    
    return None


def aprender_proveedor(cif, nombre, nombre_archivo):
    """
    Guarda un nuevo proveedor aprendido.
    
    Args:
        cif (str): CIF del proveedor
        nombre (str): Nombre correcto del proveedor
        nombre_archivo (str): Archivo de donde se aprendió
    """
    data = cargar_proveedores()
    
    # Limpiar CIF
    cif_limpio = cif.replace('-', '').replace('.', '').upper()
    
    # Crear alias (nombre simplificado para archivos)
    alias = nombre.upper().replace(',', '').replace('.', '')
    alias = alias.replace('S.A.U.', '').replace('S.L.U.', '').replace('S.A.', '').replace('S.L.', '')
    alias = alias.strip().replace(' ', '_')[:30]  # Máximo 30 caracteres
    
    data['proveedores_por_cif'][cif_limpio] = {
        "nombre": nombre,
        "alias": alias,
        "aprendido_de": nombre_archivo,
        "fecha_aprendizaje": datetime.now().strftime("%Y-%m-%d")
    }
    
    guardar_proveedores(data)
    print(f"[APRENDIDO] CIF {cif} → {alias}")


def corregir_ocr(texto):
    """
    Aplica correcciones conocidas de errores de OCR.
    
    Args:
        texto (str): Texto con posibles errores de OCR
        
    Returns:
        str: Texto corregido
    """
    data = cargar_proveedores()
    
    texto_corregido = texto
    for error, correcion in data.get('correcciones_ocr', {}).items():
        texto_corregido = texto_corregido.replace(error, correcion)
    
    return texto_corregido


def agregar_correccion_ocr(error, correccion):
    """Agrega una nueva corrección de OCR."""
    data = cargar_proveedores()
    data['correcciones_ocr'][error] = correccion
    guardar_proveedores(data)
    print(f"[APRENDIDO] Corrección OCR: {error} → {correccion}")


