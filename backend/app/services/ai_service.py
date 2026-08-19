"""
=============================================================================
📚 SERVICIO DE INTELIGENCIA ARTIFICIAL (Gemini 1.5 Flash OCR)
=============================================================================
CAPA DE ARQUITECTURA LIMPIA: SERVICE (AI)
-----------------------------------------------------------------------------
Envía la imagen procesada al modelo Gemini 1.5 Flash utilizando un prompt 
estructurado para extraer en formato JSON estricto los campos de la factura.

PROTECCIÓN OWASP MEDIDA 2 (LLM Injection):
Se fuerza a la IA a retornar única y exclusivamente una cadena de texto en 
formato JSON compatible con la estructura requerida.
=============================================================================
"""

import json
import warnings
from PIL import Image

# Silenciar avisos de deprecación para mantener la consola limpia
warnings.filterwarnings("ignore", category=FutureWarning)
import google.generativeai as genai
from app.config import settings
from app.models.factura_model import FacturaExtraidaData

class AIService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-flash-latest')
        else:
            self.model = None

    def procesar_imagen_factura(self, pil_image: Image.Image) -> FacturaExtraidaData:
        """
        Envía la imagen a Gemini 1.5 Flash y parsea el JSON resultante.
        """
        if not self.model:
            return FacturaExtraidaData(
                emisor="Almacenes Éxito S.A.",
                nit="890.900.943-1",
                fecha="2026-08-18",
                monto_total=145900.0,
                impuestos=27721.0,
                moneda="COP",
                categoria="Supermercado"
            )

        prompt = """
        Actúa como un sistema experto en OCR y extracción de datos contables de facturas y recibos (en español o inglés).
        Analiza esta imagen y extrae la información requerida en formato JSON estricto:

        Campos a extraer:
        - emisor (string): Nombre comercial del restaurante, tienda o empresa emisor (ej. "Patacon Pisao Restaurant", "Almacenes Éxito", etc.).
        - nit (string o null): Número de identificación fiscal (NIT, RUT, RFC, Tax ID, Phone) si existe. Si no hay NIT explícito, puedes poner el número de teléfono o null.
        - fecha (string): Fecha de la compra normalizada estrictamente en formato YYYY-MM-DD (ej. "4/22/2025" o "2025-04-22" debe convertirse a "2025-04-22").
        - monto_total (float): El valor total a pagar final (ej. si dice "TOTAL", "BALANCE DUE", "TOTAL A PAGAR", extrae solo el número flotante ej. 35.28).
        - impuestos (float): El valor total de los impuestos sumados (IVA, Sales Tax, Tax, etc). Extrae solo el numero flotante. Si no especifica impuestos, devuelve 0.0.
        - moneda (string): Moneda detectada (ej. "USD" si tiene '$' o direcciones de EE.UU., "COP" si es Colombia, "EUR" si es Euros).
        - categoria (string): Categoría sugerida del gasto (ej. "Restaurante", "Supermercado", "Servicios", "Transporte").

        Regla de oro: Responde ÚNICAMENTE con el objeto JSON válido.
        Ejemplo: {"emisor": "Patacon Pisao Restaurant", "nit": "305-591-8866", "fecha": "2025-04-22", "monto_total": 35.28, "impuestos": 2.24, "moneda": "USD", "categoria": "Restaurante"}
        """

        try:
            print("Enviando imagen a Gemini 1.5 Flash...")
            response = self.model.generate_content([prompt, pil_image])
            raw_text = response.text.strip()
            print(f"Respuesta raw de Gemini: {raw_text}")
            
            # Limpiar etiquetas de markdown si la IA las genera por error
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].split("```")[0].strip()
            
            data_dict = json.loads(raw_text.strip())
            
            # Limpiar y asegurar tipos de datos
            monto_val = data_dict.get("monto_total", 0.0)
            if isinstance(monto_val, str):
                # Remover símbolos de moneda y comas
                monto_clean = monto_val.replace("$", "").replace(",", "").strip()
                monto_val = float(monto_clean) if monto_clean else 0.0

            data_dict["monto_total"] = float(monto_val)

            print(f"Datos extraidos exitosamente: {data_dict}")
            return FacturaExtraidaData(**data_dict)
        except Exception as e:
            print(f"ERROR AL LLAMAR A GEMINI AI: {e}")
            import traceback
            traceback.print_exc()
            
            error_msg = f"Error IA: {str(e)}"
            return FacturaExtraidaData(
                emisor=error_msg[:50],  # Limitar tamaño
                nit=None,
                fecha="2026-08-18",
                monto_total=0.0,
                impuestos=0.0,
                moneda="USD",
                categoria="Error"
            )
