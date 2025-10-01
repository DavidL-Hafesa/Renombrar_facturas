# 🎯 Plan Híbrido - Proyecto Renombrar Facturas

## 📋 Estrategia Aprobada

Hemos decidido seguir el **enfoque híbrido** que combina lo mejor de ambos mundos:
- Empezar con **Python** para tener control y flexibilidad
- Evaluar resultados en 2-3 semanas
- Tener **Microsoft 365 como Plan B** si es necesario

---

## 🗓️ Roadmap del Proyecto

### **FASE 1: MVP Python (Semanas 1-2)**

#### Semana 1: Fundamentos
- [x] Crear repositorio y estructura
- [ ] Configurar entorno de desarrollo
- [ ] Instalar dependencias necesarias
- [ ] Implementar extracción básica de texto (PDFs simples)
- [ ] Crear sistema de logs básico
- [ ] Probar con 10 facturas de ejemplo

**Entregable:** Script que extrae texto de PDFs

#### Semana 2: OCR y Parsing
- [ ] Integrar OCR (Tesseract) para PDFs escaneados e imágenes
- [ ] Implementar regex para extraer fecha, proveedor, número
- [ ] Crear lógica de renombrado
- [ ] Manejo básico de errores
- [ ] Probar con 30-50 facturas variadas

**Entregable:** Sistema funcional de renombrado automático

---

### **FASE 2: Evaluación (Semana 3)**

#### Criterios de Éxito
- [ ] **Precisión:** >90% en extracción correcta de datos
- [ ] **Velocidad:** <2 minutos por factura
- [ ] **Robustez:** Maneja errores sin crashear
- [ ] **Cobertura:** Funciona con al menos 40 de 50 tipos de facturas

#### Métricas a Medir
```
📊 Resultados del MVP:
- Total facturas procesadas: ___
- Éxitos automáticos: ___ (___ %)
- Requirieron intervención manual: ___ (___ %)
- Fallaron completamente: ___ (___ %)
- Tiempo promedio por factura: ___ segundos
```

#### Decisión al Final de Fase 2
- ✅ **Si precisión >90%:** Continuar con Python → Pasar a Fase 3
- ⚠️ **Si precisión 70-90%:** Agregar IA (OpenAI/Claude) → Evaluar costo vs M365
- ❌ **Si precisión <70%:** Evaluar seriamente Microsoft 365

---

### **FASE 3: Refinamiento (Semanas 4-5)** 
*Solo si Fase 2 es exitosa*

- [ ] Optimizar precisión (agregar más patrones/IA si necesario)
- [ ] Implementar procesamiento en paralelo
- [ ] Crear dashboard/reportes
- [ ] Sistema de notificaciones
- [ ] Documentación completa
- [ ] Capacitación al equipo

**Entregable:** Sistema en producción

---

### **FASE 4: Producción (Semana 6+)**
- [ ] Desplegar en servidor/PC dedicado
- [ ] Configurar ejecución automática (cron/scheduled task)
- [ ] Monitoreo continuo
- [ ] Mantenimiento y mejoras

---

## 🛠️ Stack Tecnológico (Python MVP)

### Librerías Principales
```python
# Procesamiento de PDFs
pdfplumber==0.10.3        # Extracción de texto de PDFs nativos
PyMuPDF==1.23.8           # Alternativa rápida

# OCR (PDFs escaneados e imágenes)
pytesseract==0.3.10       # Wrapper de Tesseract
pdf2image==1.16.3         # Convierte PDF a imagen
Pillow==10.1.0            # Procesamiento de imágenes

# Parsing y validación
python-dateutil==2.8.2    # Parseo inteligente de fechas
regex==2023.10.3          # Expresiones regulares avanzadas

# IA (Opcional - Fase 2 si es necesario)
openai==1.3.7             # API de OpenAI
anthropic==0.7.1          # API de Claude

# Utilidades
python-dotenv==1.0.0      # Variables de entorno
loguru==0.7.2             # Sistema de logs mejorado
```

### Herramientas Externas
- **Tesseract-OCR:** Instalar desde [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
- **Git:** Para control de versiones
- **VS Code:** IDE recomendado

---

## 📁 Estructura de Proyecto Propuesta

```
Renombrar_facturas/
│
├── config/
│   ├── __init__.py
│   ├── settings.py              # Configuración general
│   └── patterns.py              # Patrones regex por proveedor
│
├── src/
│   ├── __init__.py
│   ├── ocr_extractor.py         # Extrae texto de PDFs e imágenes
│   ├── data_parser.py           # Identifica fecha, proveedor, número
│   ├── file_renamer.py          # Renombra y mueve archivos
│   ├── validator.py             # Valida datos extraídos
│   └── logger.py                # Sistema de logs
│
├── tests/
│   ├── test_ocr.py
│   ├── test_parser.py
│   └── test_renamer.py
│
├── data/
│   ├── input/                   # Facturas a procesar
│   ├── output/                  # Facturas procesadas
│   ├── errors/                  # Facturas con problemas
│   └── samples/                 # Facturas de ejemplo para testing
│
├── logs/                        # Archivos de log
│
├── requirements.txt             # Dependencias Python
├── .env.example                 # Ejemplo de variables de entorno
├── main.py                      # Script principal
└── README.md                    # Documentación
```

---

## 🚀 Pasos Inmediatos (Esta Semana)

### Para el Equipo:

1. **Recopilar facturas de ejemplo** (URGENTE)
   - [ ] 10 facturas de diferentes proveedores
   - [ ] Incluir PDFs nativos y escaneados
   - [ ] Incluir algunas imágenes (JPG/PNG)
   - [ ] Documentar: proveedor, fecha, número de cada una

2. **Definir formato de nomenclatura final**
   - Propuesta: `YYYYMMDD_Proveedor_NumFactura.pdf`
   - [ ] Aprobar o modificar

3. **Responder preguntas clave:**
   - [ ] ¿Volumen mensual aproximado de facturas?
   - [ ] ¿Tienen Microsoft 365 E3/E5? (para Plan B)
   - [ ] ¿Dónde se ejecutará el script? (PC local/servidor)
   - [ ] ¿Necesitan integración con algún sistema? (SAP, etc.)

### Para Desarrolladores (David + José María):

1. **Configurar entorno**
   ```bash
   # Crear entorno virtual
   python -m venv venv
   
   # Activar entorno
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   
   # Instalar dependencias
   pip install -r requirements.txt
   ```

2. **Instalar Tesseract**
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - Agregar al PATH

3. **Crear estructura de carpetas**
   ```bash
   mkdir -p data/{input,output,errors,samples}
   mkdir -p logs
   mkdir -p src config tests
   ```

4. **Primer objetivo:** Script que lea un PDF y extraiga texto
   ```python
   # Objetivo semana 1
   import pdfplumber
   
   with pdfplumber.open("factura.pdf") as pdf:
       text = pdf.pages[0].extract_text()
       print(text)
   ```

---

## 📊 Criterios de Decisión (Fin de Fase 2)

| Métrica | Continuar Python | Agregar IA a Python | Cambiar a M365 |
|---------|------------------|---------------------|----------------|
| Precisión | >90% | 70-90% | <70% |
| Tiempo dev | En plazo | Retraso leve | Retraso grave |
| Complejidad | Manejable | Media | Muy alta |
| Costo estimado | Bajo | Medio | Alto (si no tienen M365) |

---

## 🆘 Plan B: Microsoft 365

Si al final de Fase 2 decidimos que Python es muy complejo o no alcanza la precisión:

1. **No se pierde el trabajo:** El conocimiento ganado ayuda a configurar mejor Power Automate
2. **Transición rápida:** 3-5 días para implementar en M365
3. **Podemos mantener Python:** Para casos especiales o como backup

---

## 📝 Acuerdos del Equipo

- **Reunión semanal:** Lunes 10:00 AM para revisar progreso
- **Repositorio:** Commits diarios con mensajes descriptivos
- **Documentación:** Documentar decisiones importantes en este archivo
- **Testing:** Probar con facturas reales continuamente

---

## 🎯 Objetivo Final

**Sistema que automáticamente:**
1. ✅ Detecta nuevas facturas en carpeta de entrada
2. ✅ Extrae fecha, proveedor y número de factura
3. ✅ Renombra según formato acordado
4. ✅ Mueve a carpeta de salida organizada
5. ✅ Genera logs y reportes
6. ✅ Notifica errores para revisión manual

**Precisión objetivo:** >95%  
**Tiempo objetivo:** <2 min por factura  
**Intervención manual:** <5% de casos

---

## 📞 Contacto

- **Desarrolladores:** David Lancheros, José María Porras
- **Repositorio:** https://github.com/DavidL-Hafesa/Renombrar_facturas
- **Última actualización:** 1 de octubre de 2025

---

**¡Vamos a por ello! 🚀**

