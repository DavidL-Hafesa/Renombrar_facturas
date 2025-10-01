# ⚡ Guía Rápida: Configurar Azure en 5 Pasos

## 🎯 Objetivo
Configurar Azure Document Intelligence para mejorar la precisión de **60-85%** a **95-98%**

---

## 📝 **Paso 1: Acceder al Portal Azure** (2 min)

1. Abre: **https://portal.azure.com**
2. Inicia sesión con tu cuenta **Microsoft 365**

---

## 🔷 **Paso 2: Crear Recurso Document Intelligence** (5 min)

### En el Portal Azure:

1. **Click en "Crear un recurso"** (botón azul arriba a la izquierda)

2. **Buscar:** "Document Intelligence" o "Form Recognizer"

3. **Click en "Crear"**

4. **Rellenar formulario:**
   ```
   Suscripción:       [Tu suscripción M365]
   Grupo de recursos: [Crear nuevo] → "Facturas-RG"
   Región:            West Europe
   Nombre:            facturas-hafesa
   Nivel de precios:  Free F0 (500 páginas/mes GRATIS)
   ```

5. **Click "Revisar y crear"** → **"Crear"**

6. Esperar 1-2 minutos...

7. **Click "Ir al recurso"** cuando termine

---

## 🔑 **Paso 3: Obtener Credenciales** (1 min)

1. **En el recurso creado**, menú izquierdo:
   - Click en **"Claves y punto de conexión"**

2. **Copiar estos 2 valores:**

   **a) Punto de conexión (Endpoint):**
   ```
  https://clasificarfacturas.cognitiveservices.azure.com/
   ```

   **b) Clave 1 (Key 1):**
   ```
   abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567abc890def123...
   (String largo alfanumérico de ~64 caracteres)
   ```

---

## 💾 **Paso 4: Configurar en el Proyecto** (2 min)

1. **Abrir el archivo `.env`** en el proyecto

2. **Pegar tus credenciales:**
   ```
   AZURE_FORM_RECOGNIZER_ENDPOINT=https://facturas-hafesa.cognitiveservices.azure.com/
   AZURE_FORM_RECOGNIZER_KEY=abc123def456ghi789...
   ```
   *(Reemplaza con TUS valores del Paso 3)*

3. **Guardar el archivo**

---

## ✅ **Paso 5: Probar que Funciona** (1 min)

```bash
# Ejecutar el sistema
py Renombrar_facturas/renombrar.py
```

**Si ves esto en los logs:**
```
🔷 Datos extraídos con Azure Document Intelligence
```
→ ✅ **¡Funciona!**

**Si ves esto:**
```
⚠️ Credenciales de Azure no configuradas
```
→ ⚠️ Revisa el archivo `.env`

---

## 🎊 **¡Listo!**

Ahora el sistema:
1. **Intenta Azure primero** (95-98% precisión)
2. **Si falla, usa regex** (fallback)
3. **Todo automático**

---

## 💰 **Límites del Tier Gratuito:**

- **500 páginas/mes GRATIS**
- Para 500 facturas de 1 página = GRATIS
- Si superas 500, cuesta **$1 por 1000 páginas** adicionales

---

## 🆘 **Problemas Comunes:**

### "Subscription not found"
→ Asegúrate de seleccionar la suscripción correcta de M365

### "Region not available"  
→ Cambia a otra región: North Europe, France Central

### "Access denied"
→ Puede que necesites permisos de administrador

---

## 📧 **Ayuda:**

- **Documentación oficial:** https://learn.microsoft.com/azure/ai-services/document-intelligence/
- **Soporte Microsoft:** Desde el portal Azure

---

**Tiempo total:** ~10 minutos  
**Dificultad:** Fácil ⭐  
**Beneficio:** +10-35% de precisión 🚀

