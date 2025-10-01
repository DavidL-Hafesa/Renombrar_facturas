"""
Script para crear un PDF de prueba simple (sin librerías externas)
"""

from datetime import datetime

# Crear un archivo HTML y abrirlo para convertir a PDF manualmente
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; padding: 40px; }}
        .factura {{ border: 2px solid #333; padding: 20px; }}
        .header {{ background: #0078d4; color: white; padding: 15px; }}
        .datos {{ margin: 20px 0; }}
        .dato {{ margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="factura">
        <div class="header">
            <h1>FACTURA DE PRUEBA</h1>
        </div>
        <div class="datos">
            <div class="dato"><strong>Proveedor:</strong> Iberdrola Energía</div>
            <div class="dato"><strong>Número de Factura:</strong> FAC-2024-12345</div>
            <div class="dato"><strong>Fecha:</strong> 15/09/2024</div>
            <div class="dato"><strong>Importe:</strong> 350.00 €</div>
        </div>
        <div>
            <h3>Descripción:</h3>
            <p>Suministro eléctrico correspondiente al mes de agosto 2024.</p>
            <p>Período de facturación: 01/08/2024 - 31/08/2024</p>
        </div>
    </div>
</body>
</html>
"""

# Guardar HTML
with open("factura_prueba.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("OK - Archivo HTML creado: factura_prueba.html")
print("\nInstrucciones:")
print("1. Abre 'factura_prueba.html' en tu navegador")
print("2. Usa Ctrl+P (Imprimir)")
print("3. Selecciona 'Guardar como PDF'")
print("4. Guardalo como 'factura_prueba.pdf' en la misma carpeta")
print("5. Luego ejecuta: py test_pdf_simple.py")

import webbrowser
webbrowser.open("factura_prueba.html")

