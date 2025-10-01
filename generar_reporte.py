"""
Genera un CSV con la comparación entre nombres originales y generados
"""
import sys
import csv
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from Renombrar_facturas.renombrar import extraer_texto, parsear_factura, generar_nuevo_nombre

def generar_reporte_csv():
    """Genera CSV con comparación de todas las facturas."""
    
    facturas = sorted(Path("data/samples").glob("*.pdf"))
    
    # Nombre del archivo CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = f"reporte_validacion_{timestamp}.csv"
    
    print(f"\nProcesando {len(facturas)} facturas...")
    print(f"Generando: {csv_file}\n")
    
    resultados = []
    
    for i, factura_path in enumerate(facturas, 1):
        print(f"[{i}/{len(facturas)}] {factura_path.name}...", end=" ")
        
        resultado = {
            'nombre_original': factura_path.name,
            'nombre_generado': '',
            'fecha_detectada': '',
            'proveedor_detectado': '',
            'numero_detectado': '',
            'estado': ''
        }
        
        try:
            # Extraer y parsear
            texto = extraer_texto(factura_path)
            
            if not texto:
                resultado['estado'] = 'ERROR: No se pudo extraer texto'
                print("ERROR (sin texto)")
            else:
                info = parsear_factura(texto, factura_path.name, ruta_pdf=factura_path)
                
                if not info:
                    resultado['estado'] = 'ERROR: No se pudo parsear'
                    print("ERROR (parseo)")
                else:
                    # Generar nombre
                    nombre_gen = generar_nuevo_nombre(info)
                    
                    resultado['nombre_generado'] = nombre_gen
                    resultado['fecha_detectada'] = info.get('fecha', '')
                    resultado['proveedor_detectado'] = info.get('proveedor', '')
                    resultado['numero_detectado'] = info.get('numero', '')
                    resultado['estado'] = 'OK'
                    print("OK")
                    
        except Exception as e:
            resultado['estado'] = f'ERROR: {str(e)}'
            print(f"EXCEPCION")
        
        resultados.append(resultado)
    
    # Escribir CSV
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ['nombre_original', 'nombre_generado', 'fecha_detectada', 
                     'proveedor_detectado', 'numero_detectado', 'estado']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(resultados)
    
    print(f"\n[OK] CSV generado: {csv_file}")
    
    # Estadísticas
    total = len(resultados)
    exitosas = sum(1 for r in resultados if r['estado'] == 'OK')
    errores = total - exitosas
    
    print(f"\nESTADISTICAS:")
    print(f"  Total:     {total}")
    print(f"  Exitosas:  {exitosas} ({exitosas/total*100:.1f}%)")
    print(f"  Errores:   {errores} ({errores/total*100:.1f}%)")
    
    # Abrir CSV
    import os
    os.startfile(csv_file)
    
    return csv_file


if __name__ == "__main__":
    generar_reporte_csv()

