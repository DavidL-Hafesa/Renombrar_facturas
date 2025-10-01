# 🔷 Configurar Azure Document Intelligence

## 📋 Pasos para configurar (15 minutos)

### **Paso 1: Crear recurso en Azure Portal**

1. **Accede al portal de Azure:**
   - https://portal.azure.com
   - Inicia sesión con tu cuenta M365

2. **Crear recurso de Document Intelligence:**
   - Click en "Crear un recurso"
   - Buscar: **"Document Intelligence"** o **"Form Recognizer"**
   - Click en "Crear"

3. **Configuración del recurso:**
   ```
   Suscripción: Tu suscripción M365
   Grupo de recursos: Crear nuevo → "Facturas-RG"
   Región: West Europe (o más cercana)
   Nombre: facturas-hafesa (o el que prefieras)
   Nivel de precios: Free F0 (500 páginas/mes gratis)
   ```

4. **Click en "Revisar y crear"** → **"Crear"**
   - Esperar 1-2 minutos

---

### **Paso 2: Obtener credenciales**

1. **Una vez creado el recurso:**
   - Click en "Ir al recurso"

2. **En el menú izquierdo:**
   - Click en "Claves y punto de conexión" (Keys and Endpoint)

3. **Copiar estos datos:**
   - **Punto de conexión (Endpoint):** 
     ```
     https://facturas-hafesa.cognitiveservices.azure.com/
     ```
   - **Clave (Key 1):** 
     ```
     abc123...xyz (string largo)
     ```

---

### **Paso 3: Configurar en el proyecto**

1. **Crear archivo `.env` en la raíz del proyecto:**
   ```bash
   # Copiar desde ejemplo
   copy env.example.txt .env
   ```

2. **Editar `.env` y pegar tus credenciales:**
   ```
   AZURE_FORM_RECOGNIZER_ENDPOINT=https://facturas-hafesa.cognitiveservices.azure.com/
   AZURE_FORM_RECOGNIZER_KEY=tu-api-key-copiada-del-portal
   ```

3. **Instalar dependencias:**
   ```bash
   pip install azure-ai-formrecognizer python-dotenv
   ```

---

### **Paso 4: Probar que funciona**

```bash
py Renombrar_facturas/renombrar.py
```

El sistema ahora:
1. Intentará usar Azure primero (alta precisión)
2. Si falla o no está configurado, usará regex (fallback)

---

## 🎯 **Niveles de precios de Azure:**

| Tier | Precio | Páginas/mes | Ideal para |
|------|--------|-------------|------------|
| **F0 (Free)** | Gratis | 500 | Testing/Desarrollo |
| **S0 (Standard)** | $1/1000 páginas | Ilimitado | Producción |

**Con 500 facturas/mes → Gratis** ✅  
**Con 1000 facturas/mes → $0.50/mes** 💰

---

## 🔍 **Modelo prebuilt-invoice detecta:**

- ✅ Fecha de factura (InvoiceDate)
- ✅ Número de factura (InvoiceId)
- ✅ Nombre del proveedor (VendorName)
- ✅ CIF del proveedor (VendorTaxId)
- ✅ Cliente (CustomerName)
- ✅ Total (InvoiceTotal)
- ✅ Subtotal, impuestos, etc.
- ✅ Elementos de línea (productos/servicios)

**Precisión esperada: 95-98%** para facturas estándar europeas 🎯

---

## 🆘 **Solución de problemas:**

### Error: "No tengo acceso a Azure"
→ Habla con tu administrador de M365/Azure

### Error: "Subscription not found"
→ Usa la suscripción correcta en el paso de creación

### Error: "Region not available"
→ Cambia a otra región (West Europe, North Europe)

### Error: "Quota exceeded"
→ Has superado las 500 páginas del tier gratuito. Cambia a S0 o espera al próximo mes.

---

## 📧 Contacto

Si tienes problemas configurando Azure, puedes:
- Contactar soporte Microsoft
- Documentación oficial: https://learn.microsoft.com/azure/ai-services/document-intelligence/

---

**Siguiente paso:** Obtén endpoint y API key del portal Azure y configurar .env

