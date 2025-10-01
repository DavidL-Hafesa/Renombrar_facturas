# 📄 Propuesta Técnica: Automatización de Renombrado de Facturas

**Proyecto:** Renombrar_facturas  
**Fecha:** 1 de octubre de 2025  
**Solución:** Microsoft 365 (Híbrida con Python)

---

## 🎯 Objetivo del Proyecto

Automatizar el proceso de renombrado y organización de facturas recibidas en diversos formatos (PDF e imágenes), extrayendo información clave como:

- **Fecha de la factura**
- **Nombre del proveedor**
- **Número de factura**

Las facturas serán renombradas automáticamente con estos datos y organizadas en carpetas específicas.

---

## 📋 Contexto del Problema

### Situación Actual

- **Volumen:** Pueden llegar hasta **50 tipos de facturas diferentes**
- **Formatos:** PDF (nativos y escaneados) e imágenes (JPG/PNG)
- **Proceso manual:** Actualmente requiere tiempo y es propenso a errores
- **Necesidad:** Automatización completa del proceso

### Desafíos

1. Múltiples proveedores con formatos distintos
2. PDFs nativos vs escaneados requieren tratamiento diferente
3. Calidad variable de las imágenes escaneadas
4. Variabilidad en la ubicación de datos dentro de las facturas
5. Necesidad de alta precisión (>95%)

---

## 🔷 Solución Recomendada: Microsoft 365

### Herramientas Clave

#### 1. **Power Automate** (Principal)
- Automatiza todo el flujo de trabajo
- Detecta nuevos archivos en carpetas
- Orquesta todo el proceso

#### 2. **AI Builder - Document Processing**
- OCR integrado (extrae texto de PDFs e imágenes)
- Modelos pre-entrenados para facturas
- Reconocimiento inteligente de fechas, proveedores, números

#### 3. **SharePoint o OneDrive**
- Carpeta de entrada: Facturas sin procesar
- Carpeta de salida: Facturas renombradas
- Control de versiones automático

#### 4. **Azure Form Recognizer** (Opcional, más potente)
- OCR de nivel empresarial
- Específico para facturas
- Mayor precisión

---

### ✅ Ventajas de Microsoft 365

- **Sin código** o low-code
- **Ya licenciado** (si tienen M365 E3/E5)
- **Integración nativa** con todo el ecosistema Microsoft
- **OCR incluido** en AI Builder
- **Mantenimiento mínimo**
- **Auditoría automática** de todos los procesos
- **Escalable** según las necesidades

---

## 🔄 Flujo del Proceso Automatizado

```
1. Nuevo archivo detectado en carpeta SharePoint/OneDrive
   ↓
2. Power Automate se activa automáticamente
   ↓
3. AI Builder procesa el documento:
   • Extrae texto (OCR)
   • Identifica campos: fecha, proveedor, número de factura
   ↓
4. Valida que los datos extraídos sean correctos
   ↓
5. Renombra archivo: "YYYYMMDD_Proveedor_NumFactura.pdf"
   ↓
6. Mueve archivo a carpeta de salida
   ↓
7. (Opcional) Envía notificación o registra en Excel/SharePoint List
```

---

## 🐍 Alternativa: Solución Python (Implementación Actual)

### Stack Tecnológico

**Librerías Principales:**
- `pdfplumber` / `PyMuPDF` - Extracción de texto de PDFs
- `pytesseract` + `Tesseract-OCR` - OCR gratuito
- `pdf2image` - Conversión de PDF a imagen
- `Pillow (PIL)` - Procesamiento de imágenes
- `OpenAI/Claude API` - Extracción inteligente con IA
- `python-dateutil` - Parseo inteligente de fechas
- `regex` - Búsqueda de patrones

### Arquitectura Python

```
proyecto/
├── input/              # Carpeta con facturas sin procesar
├── output/             # Carpeta con facturas renombradas
├── logs/               # Registro de procesamiento
├── config.py           # Configuración (patrones, proveedores)
├── extractor.py        # Extrae texto de PDF/imágenes
├── parser.py           # Identifica fecha, proveedor, nº factura
├── renamer.py          # Renombra y mueve archivos
└── main.py             # Ejecuta todo el proceso
```

### ✅ Ventajas de Python

- **Control total** del código
- **Gratuito** (excepto APIs de IA opcionales)
- **Muy flexible** - implementa cualquier lógica
- **Personalizable al 100%**
- **Portabilidad** - funciona en cualquier plataforma
- **Escalable** para alto volumen

### ⚠️ Consideraciones de Python

- Requiere **desarrollo** (2-4 semanas)
- Necesita **conocimientos técnicos**
- **Mantenimiento continuo**
- Requiere **infraestructura** (servidor/PC)
- Configuración inicial más compleja

---

## 💼 Comparación Directa

| Criterio | Microsoft 365 | Python | Ganador |
|----------|---------------|--------|---------|
| **Velocidad de implementación** | 3-5 días | 2-4 semanas | Microsoft 365 |
| **Costo inicial** | Licencias M365 | Tiempo de desarrollo | Depende |
| **Facilidad de uso** | Interfaz visual | Requiere código | Microsoft 365 |
| **Flexibilidad** | Limitada | Ilimitada | Python |
| **Escalabilidad** | Buena | Excelente | Python |
| **Mantenimiento** | Muy bajo | Alto | Microsoft 365 |
| **Integración empresarial** | Excelente | Requiere desarrollo | Microsoft 365 |
| **Portabilidad** | Solo Microsoft | Multi-plataforma | Python |
| **Personalización** | Media | Total | Python |

---

## 🎯 Decisión: Enfoque Híbrido

### Estrategia Recomendada

**Combinar lo mejor de ambos mundos:**

#### Fase 1: Prototipo Python (Semanas 1-2)
- Crear MVP funcional con Python
- Probar con 50-100 facturas reales
- Identificar casos difíciles
- **Meta:** Validar viabilidad técnica

#### Fase 2: Evaluación (Semana 3)
- Medir precisión del OCR
- Evaluar tiempo de desarrollo restante
- Comparar con costo de M365
- **Decisión:** Continuar Python o cambiar a M365

#### Fase 3: Implementación (Según decisión)
- Si Python funciona bien → Continuar y mejorar
- Si hay problemas → Evaluar Power Automate
- Opción intermedia: Python + Azure Form Recognizer API

---

## 📝 Formato de Nomenclatura Propuesto

### Formato del nombre de archivo:

```
YYYYMMDD_NombreProveedor_NumeroFactura.pdf
```

### Ejemplo:

```
20251001_Iberdrola_FAC2024-12345.pdf
```

### Ventajas de este formato:

- ✓ Ordenación cronológica automática
- ✓ Fácil búsqueda por proveedor
- ✓ Referencia única por número de factura
- ✓ Compatible con todos los sistemas

---

## 📁 Estructura de Carpetas Propuesta

```
Facturas/
├── 01_Entrada/              # Facturas nuevas sin procesar
├── 02_Procesadas/           # Facturas renombradas y organizadas
│   ├── 2025/
│   │   ├── 01_Enero/
│   │   ├── 02_Febrero/
│   │   └── ...
│   └── 2024/
├── 03_Errores/              # Facturas con problemas
└── 04_Logs/                 # Registros de procesamiento
```

---

## 📋 Requisitos Previos

### Licencias necesarias (Opción M365):

- Microsoft 365 E3 o E5 (recomendado)
- Créditos de AI Builder (incluidos en algunas licencias)
- SharePoint Online o OneDrive for Business

### Permisos necesarios:

- Permisos de administrador para configurar Power Automate
- Acceso a AI Builder
- Permisos de carpetas en SharePoint/OneDrive

### Para Python:

- Python 3.8+ instalado
- Tesseract-OCR (para OCR gratuito)
- Acceso al NAS o carpetas compartidas
- (Opcional) API keys de OpenAI o Claude

---

## 📊 Métricas de Éxito

### Objetivos cuantitativos:

- 📈 **Tasa de precisión:** >95% en extracción de datos
- ⏱️ **Tiempo de procesamiento:** <2 minutos por factura
- 🎯 **Automatización:** 100% sin intervención manual
- ❌ **Tasa de error:** <5% (con manejo automático)
- 💰 **Ahorro de tiempo:** Estimado 80-90% vs proceso manual

### Objetivos cualitativos:

- Reducción de errores humanos
- Mejora en la organización documental
- Facilidad de búsqueda y auditoría
- Escalabilidad para futuro crecimiento

---

## 🚀 Plan de Implementación

### Fase 1: Estructura Básica (1 semana)

- Crear estructura de carpetas en SharePoint/OneDrive o local
- Configurar entorno de desarrollo (Python) o Power Automate
- Probar con 5-10 facturas de ejemplo
- Validar flujo básico de trabajo

### Fase 2: Integración OCR/AI (1-2 semanas)

- Implementar extracción de texto (Python: pdfplumber/tesseract | M365: AI Builder)
- Crear patrones de parsing para proveedores comunes
- Integrar OCR en el flujo
- Pruebas con diferentes tipos de facturas

### Fase 3: Refinamiento (1 semana)

- Añadir validaciones de datos
- Implementar manejo de errores robusto
- Configurar notificaciones
- Crear dashboard de seguimiento
- Documentación completa del proceso

### Fase 4: Producción (Ongoing)

- Pruebas con volumen real en entorno de testing
- Ajustes finales basados en feedback
- Despliegue gradual en producción
- Monitoreo y mejora continua

---

## 💡 Recomendación Final

### Para GRUPO-HAFESA:

**Implementar enfoque híbrido con Python como solución principal:**

#### Justificación:

1. **Mayor control:** Al ser desarrollo interno, tienen control total
2. **Flexibilidad:** Pueden adaptarlo a necesidades específicas
3. **Aprendizaje:** El equipo gana expertise valiosa
4. **Económico:** Sin costos de licencias adicionales (si no tienen M365 E3/E5)
5. **Escalable:** Fácilmente adaptable a futuras necesidades

#### Plan B disponible:

Si Python presenta desafíos inesperados, Microsoft 365 sigue siendo una opción viable con implementación rápida.

---

## ❓ Preguntas a Resolver

### Antes de comenzar desarrollo:

- ¿Tienen acceso a Microsoft 365 E3/E5 con AI Builder?
- ¿Cuál es el volumen mensual aproximado de facturas?
- ¿Hay proveedores con formatos especiales que requieran atención?
- ¿Necesitan integración con algún sistema contable (SAP, Dynamics, etc.)?
- ¿Requieren notificaciones automáticas?
- ¿Necesitan histórico de cambios y auditoría?
- ¿Dónde se almacenarán las facturas? (NAS, SharePoint, OneDrive)

---

## 📧 Contacto

**Equipo del Proyecto:**
- **David Lancheros** - david.lancheros@grupohafesa.com
- **José María Porras** - josemapa92@gmail.com

**Repositorio:** [github.com/DavidL-Hafesa/Renombrar_facturas](https://github.com/DavidL-Hafesa/Renombrar_facturas)

---

**Documento generado:** 1 de octubre de 2025  
**Última actualización:** 1 de octubre de 2025  
**Estado:** En desarrollo - Fase MVP Python

