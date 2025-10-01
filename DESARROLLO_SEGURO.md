# 🛡️ Guía de Desarrollo Seguro

## ⚠️ REGLA DE ORO

**NUNCA desarrollar o probar directamente en el NAS de producción.**

---

## 🏗️ Entornos de Trabajo

### 1. **DESARROLLO** (Tu PC / PC de David)

**Ubicación:** `data/samples/` (local)

**Características:**
- ✅ Facturas de ejemplo (20-30 muestras)
- ✅ `DRY_RUN = True` (no renombra realmente)
- ✅ Cambios en Git
- ✅ Testing rápido e iterativo

**Activar:**
```bash
# Por defecto está en desarrollo
# O explícitamente:
$env:ENV = "development"
py Renombrar_facturas/renombrar.py
```

---

### 2. **TESTING** (NAS_TEST - Carpeta separada)

**Ubicación:** `\\NAS-HAFESA\Facturas_TEST\`

**Características:**
- ✅ Copias de facturas reales (100-200)
- ✅ Estructura igual a producción
- ✅ `DRY_RUN = True` por defecto
- ⚠️ Solo David tiene acceso (quien puede copiar del NAS)

**Activar:**
```bash
$env:ENV = "testing"
py Renombrar_facturas/renombrar.py
```

**Preparación (David):**
1. Crear carpeta `\\NAS-HAFESA\Facturas_TEST\`
2. Copiar 100-200 facturas variadas
3. Crear subcarpetas: `input/`, `output/`, `errors/`

---

### 3. **PRODUCCIÓN** (NAS Real)

**Ubicación:** `\\NAS-HAFESA\Facturas\`

**Características:**
- 🚨 Facturas REALES
- 🔒 Requiere confirmación explícita
- 🔒 `DRY_RUN = True` por defecto (seguridad)
- ✅ Solo activar cuando precisión >95%

**Activar (Fase 1 - Solo lectura):**
```bash
$env:ENV = "production"
py Renombrar_facturas/renombrar.py
# Por defecto NO renombrará, solo mostrará vista previa
```

**Activar (Fase 2 - Renombrado REAL):**
```bash
$env:ENV = "production"
$env:ALLOW_PRODUCTION = "true"
py Renombrar_facturas/renombrar.py
# Pedirá confirmación: "SI ESTOY SEGURO"
```

---

## 📋 Workflow de Desarrollo

### **Semana 1-2: Desarrollo Local**

```
1. David copia 20-30 facturas → data/samples/
2. Ambos desarrollan código
3. Prueban localmente
4. Suben a Git
5. Iteran hasta que funcione bien
```

### **Semana 3: Testing en NAS_TEST**

```
1. David crea \\NAS-HAFESA\Facturas_TEST\
2. Copia 100-200 facturas variadas
3. Configuran ENV=testing
4. Ejecutan script
5. Validan precisión
6. Si precisión <90% → volver a desarrollo
7. Si precisión >90% → continuar
```

### **Semana 4: Pre-Producción**

```
1. ENV=production con DRY_RUN=True
2. Ejecutar sobre NAS real (solo lectura)
3. Revisar 100 renombrados propuestos manualmente
4. Si todo OK → activar renombrado real
```

### **Semana 5+: Producción**

```
1. ENV=production
2. ALLOW_PRODUCTION=true
3. Procesar primero 50 facturas
4. Validar manualmente
5. Si OK → procesar resto
6. Monitorear logs
```

---

## 🗂️ Estructura de Carpetas

### **Local (Desarrollo):**
```
GitProject/
├── data/
│   ├── samples/          ← Facturas de ejemplo (Git ignored)
│   │   ├── iberdrola_1.pdf
│   │   ├── endesa_2.pdf
│   │   └── ...
│   ├── output/           ← Resultados de pruebas locales
│   └── errors/           ← Facturas con problemas
```

### **NAS Testing:**
```
\\NAS-HAFESA\Facturas_TEST\
├── input/                ← Copias de facturas reales
├── output/               ← Facturas renombradas (prueba)
├── errors/               ← Facturas con problemas
└── logs/                 ← Logs de ejecución
```

### **NAS Producción:**
```
\\NAS-HAFESA\Facturas\
├── input/                ← Facturas nuevas (REAL)
├── output/               ← Facturas procesadas (REAL)
├── errors/               ← Facturas con problemas (REAL)
└── logs/                 ← Logs de producción
```

---

## 🚨 Medidas de Seguridad

### 1. **DRY RUN por Defecto**
- El script NUNCA renombra por defecto
- Solo genera vista previa
- Requiere flag explícito para renombrar

### 2. **Confirmación en Producción**
- Si intentas renombrar en producción
- Te pregunta: "¿Estás ABSOLUTAMENTE seguro?"
- Debes escribir exactamente: "SI ESTOY SEGURO"

### 3. **Backups Automáticos (Recomendado)**
- Antes de renombrar en producción
- Hacer backup del NAS
- O copiar facturas a carpeta de respaldo

### 4. **Logs Detallados**
- Cada ejecución genera log
- Con timestamp
- Qué facturas se procesaron
- Qué cambios se hicieron

### 5. **Rollback Manual**
- Si algo sale mal
- Los logs tienen el nombre original
- Se puede revertir manualmente

---

## 📊 Checklist Pre-Producción

Antes de ejecutar en producción real, verificar:

- [ ] Precisión >95% en testing
- [ ] Probado con al menos 200 facturas de ejemplo
- [ ] Logs funcionando correctamente
- [ ] Backup del NAS disponible
- [ ] David ha revisado el código
- [ ] Ambos están de acuerdo en proceder
- [ ] Plan de rollback definido
- [ ] Horario fuera de horas pico (por si acaso)

---

## 🆘 Plan de Emergencia

**Si algo sale mal en producción:**

1. **DETENER INMEDIATAMENTE** (Ctrl+C)
2. **Revisar logs:** `logs/renombrar_FECHA.log`
3. **Identificar facturas afectadas**
4. **Restaurar desde backup si es necesario**
5. **Revertir usando el log** (tiene nombres originales)
6. **Analizar qué falló**
7. **Corregir en desarrollo**
8. **Re-probar en testing**

---

## 💡 Mejores Prácticas

1. **Nunca tener prisa** - Mejor lento y seguro
2. **Siempre probar en samples primero**
3. **Luego probar en NAS_TEST**
4. **Solo entonces ir a producción**
5. **Hacer commits frecuentes en Git**
6. **Documentar casos raros**
7. **Comunicarse constantemente**

---

## 👥 Responsabilidades

### **José María (tú):**
- Desarrollo de código
- Testing local
- Documentación
- Subir a Git

### **David:**
- Copiar facturas de ejemplo del NAS
- Crear entorno de testing en NAS
- Validar acceso al NAS
- Ejecutar en producción (cuando esté listo)
- Monitoreo post-producción

### **Ambos:**
- Revisión de código
- Validación de resultados
- Decisión de ir a producción

---

**Última actualización:** 1 de octubre de 2025

