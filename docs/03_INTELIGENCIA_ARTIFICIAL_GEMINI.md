# 🤖 Módulo 03: Integración con IA Google Gemini

En este módulo aprenderás cómo integramos modelos de visión multimodal de Inteligencia Artificial (**Google Gemini**) en una aplicación de producción y cómo protegemos el sistema contra errores de red y límites de cuota.

---

## 👁️ 1. ¿Qué es un Modelo Multimodal?

Un modelo multimodal (como **Gemini 1.5 Flash**) es capaz de recibir más de un tipo de dato a la vez:
1. **Un archivo visual** (la fotografía de la factura).
2. **Un texto de instrucciones** (el "System Prompt").

La IA procesa visualmente la imagen como un humano: lee el texto manuscrito o impreso, entiende dónde está el encabezado, ubica la fecha y calcula mentalmente el total y los impuestos.

---

## ⚡ 2. Optimización de Rendimiento (Evitar que se quede colgado)

Una foto moderna de un teléfono inteligente puede medir `4000 x 3000` píxeles y pesar más de `8 MB`.
Si intentas subir un archivo de 8 MB a una API por internet:
- Tardará 15 a 30 segundos en subir.
- Puede fallar por timeout de red.
- Consume ancho de banda innecesario.

### La Solución en `backend/app/services/ai_service.py`:
```python
# Redimensionar la imagen antes de enviarla
max_size = (1600, 1600)
img_optimized = pil_image.copy()
img_optimized.thumbnail(max_size)

response = self.model.generate_content([prompt, img_optimized])
```
Con `.thumbnail((1600, 1600))`, la imagen se reduce a menos de `500 KB` manteniendo una nitidez 100% legible para la IA. La respuesta pasa de tardar 20 segundos a **menos de 3 segundos**.

---

## 📜 3. Prompt Engineering Estructurado para JSON

Los modelos de lenguaje tienden a ser "conversacionales" (ej: *"¡Hola! Aquí tienes los datos de la factura que me pediste..."*).
Para una API, ese texto conversacional rompe el código porque necesitamos un **JSON puro**.

### Nuestro Prompt en `ai_service.py`:
```text
Eres un asistente experto en OCR y extracción de datos financieros de facturas y recibos.
Analiza la imagen adjunta y extrae la información en un formato JSON estructurado EXACTAMENTE con las siguientes claves:

Campos a extraer:
- emisor (string): Nombre comercial del restaurante o empresa.
- nit (string o null): Número de identificación fiscal (NIT, RUT, RFC, Tax ID, Phone).
- fecha (string): Fecha normalizada en formato YYYY-MM-DD.
- monto_total (float): Valor total a pagar. DEBE SER UN NÚMERO (ej. 35.28). NO incluyas letras ni símbolos.
- impuestos (float): Valor total de impuestos (IVA, Sales Tax). DEBE SER UN NÚMERO (ej. 2.50). Si no hay, devuelve 0.0.
- moneda (string): Código de la moneda (USD, COP, EUR).
- categoria (string): Categoría sugerida (Restaurante, Supermercado, Servicios).

Regla de oro: Responde ÚNICAMENTE con el objeto JSON válido. NO uses bloques de texto adicionales.
```

---

## 🛡️ 4. Manejo Defensivo de Errores y Cuotas (HTTP 429)

En aplicaciones reales, las APIs de terceros pueden fallar por:
1. **Límites de cuota (Error 429 Too Many Requests)**: Cuando se sobrepasa el límite gratuito de peticiones diarias.
2. **Caídas de internet o problemas en los servidores de Google**.

### Cómo lo solucionamos en el código:
```python
        except Exception as e:
            print(f"ERROR AL LLAMAR A GEMINI AI: {e}")
            import traceback
            traceback.print_exc()
            
            error_msg = f"Error IA: {str(e)}"
            return FacturaExtraidaData(
                emisor=error_msg[:50],  # Mostramos el error en la tarjeta visual
                nit=None,
                fecha="2026-08-18",
                monto_total=0.0,
                impuestos=0.0,
                moneda="COP",
                categoria="Sin Categoría"
            )
```

**Patrón de Resiliencia (Graceful Degradation):**  
En lugar de que el backend lance un error 500 y "se caiga", capturamos la excepción (`try/except`), devolvemos un objeto `FacturaExtraidaData` con un mensaje amigable y permitimos que el usuario vea exactamente qué ocurrió en su panel de control.

---

### ➡️ Siguiente Módulo:
Aprende cómo guardamos los PDFs y los registros en la nube con PostgreSQL:  
👉 [Módulo 04: Base de Datos y Storage con Supabase](file:///c:/Users/Yaorj/Documents/FactuSnap/docs/04_PERSISTENCIA_SUPABASE.md)
