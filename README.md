# 📄 Renombrar Facturas - Automatización Inteligente

Sistema automatizado para renombrar y organizar facturas en formato PDF e imágenes, extrayendo información clave mediante OCR y procesamiento inteligente.

## 🎯 Objetivo

Automatizar el proceso de renombrado de facturas extrayendo:
- 📅 **Fecha de la factura**
- 🏢 **Nombre del proveedor**
- 🔢 **Número de factura**

**Formato de salida:** `YYYYMMDD_Proveedor_NumFactura.pdf`

## 📊 Estado del Proyecto

🟡 **Fase:** MVP en desarrollo (Semana 1-2)  
📅 **Inicio:** 1 de octubre de 2025  
👥 **Equipo:** David Lancheros, José María Porras  
🔄 **Estrategia:** Enfoque Híbrido (Python → Evaluar → Decisión)

Ver [PLAN_HIBRIDO.md](PLAN_HIBRIDO.md) para el roadmap completo.

## 🚀 Quick Start

### Prerrequisitos

- Python 3.8+
- Tesseract-OCR ([Instalar Windows](https://github.com/UB-Mannheim/tesseract/wiki))
- Git

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/DavidL-Hafesa/Renombrar_facturas.git
cd Renombrar_facturas

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones
```

### Uso Básico

```python
# Procesar una factura
python main.py --input "data/input/factura.pdf"

# Procesar carpeta completa
python main.py --input-dir "data/input"

# Ver logs
python main.py --verbose
```

## 📁 Estructura del Proyecto

```
Renombrar_facturas/
│
├── config/                  # Configuración
│   ├── settings.py         # Configuración general
│   └── patterns.py         # Patrones regex por proveedor
│
├── src/                    # Código fuente
│   ├── ocr_extractor.py   # Extracción de texto
│   ├── data_parser.py     # Parsing de datos
│   ├── file_renamer.py    # Renombrado de archivos
│   └── validator.py       # Validación
│
├── data/                   # Datos
│   ├── input/             # Facturas a procesar
│   ├── output/            # Facturas procesadas
│   ├── errors/            # Facturas con errores
│   └── samples/           # Ejemplos para testing
│
├── logs/                   # Archivos de log
├── tests/                  # Tests unitarios
│
├── main.py                 # Script principal
├── requirements.txt        # Dependencias
└── README.md              # Este archivo
```

## 🛠️ Stack Tecnológico

- **Python 3.8+**
- **pdfplumber / PyMuPDF:** Extracción de texto de PDFs
- **Tesseract-OCR / pytesseract:** OCR para PDFs escaneados
- **Pillow:** Procesamiento de imágenes
- **python-dateutil:** Parsing de fechas
- **regex:** Patrones de búsqueda avanzados

## 📋 Roadmap

- [x] Crear repositorio
- [x] Definir estrategia (Enfoque Híbrido)
- [ ] Configurar entorno de desarrollo
- [ ] Implementar extracción básica de PDFs
- [ ] Integrar OCR para PDFs escaneados
- [ ] Implementar parsing de datos
- [ ] Sistema de renombrado
- [ ] Testing con facturas reales
- [ ] Evaluación de precisión
- [ ] Decisión: Continuar Python o evaluar M365

Ver roadmap completo en [PLAN_HIBRIDO.md](PLAN_HIBRIDO.md)

## 📊 Métricas Objetivo

- ✅ **Precisión:** >95% en extracción correcta
- ⏱️ **Velocidad:** <2 minutos por factura
- 🎯 **Automatización:** >95% sin intervención manual
- 🐛 **Robustez:** Manejo de errores en 100% de casos

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Documentación Adicional

- [Plan Híbrido](PLAN_HIBRIDO.md) - Estrategia completa del proyecto
- [Propuesta Técnica](Propuesta_Renombrar_Facturas.html) - Análisis inicial de soluciones
- [Análisis Comparativo](Analisis_Comparativo.html) - Comparación M365 vs Python

## 📧 Contacto

- **David Lancheros** - david.lancheros@grupohafesa.com
- **José María Porras** - josemapa92@gmail.com

## 📄 Licencia

Proyecto interno de GRUPO-HAFESA

---

**Última actualización:** 1 de octubre de 2025

