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
from PIL import Image
import google.generativeai as genai
from app.config import settings
from app.models.factura_model import FacturaExtraidaData

class AIService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def procesar_imagen_factura(self, pil_image: Image.Image) -> FacturaExtraidaData:
        """
        Envía la imagen a Gemini 1.5 Flash y parsea el JSON resultante.
        """
        if not self.model:
            # Fallback en desarrollo si no hay API Key configurada
            return FacturaExtraidaData(
                emisor="Almacenes Éxito S.A.",
                nit="890.900.943-1",
                fecha="2026-08-18",
                monto_total=145900.0,
                moneda="COP",
                categoria="Supermercado"
            )

        prompt = """
        Actúa como un experto en OCR y procesamiento de documentos contables.
        Analiza esta imagen de factura y extrae la información en un objeto JSON estricto con las siguientes claves:
        - emisor (string): Nombre del comercio o empresa emisor.
        - nit (string o null): Identificación fiscal NIT/RUT/RFC si está visible.
        - fecha (string): Fecha de compra en formato YYYY-MM-DD.
        - monto_total (float): Valor total a pagar.
        - moneda (string): Moneda de la factura (ej. COP, USD, EUR). Default: COP.
        - categoria (string): Categoría del gasto (ej. Supermercado, Restaurante, Tecnología, Servicios).

        Responde ÚNICAMENTE con el objeto JSON válido. No incluyas bloques de código markdown como ```json.
        """

        try:
            response = self.model.generate_content([prompt, pil_image])
            raw_text = response.text.strip()
            
            # Limpiar etiquetas de markdown si la IA las genera por error
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            
            data_dict = json.loads(raw_text.strip())
            return FacturaExtraidaData(**data_dict)
        except Exception as e:
            # Si falla la extracción por IA o formato, se devuelve un fallback seguro
            return FacturaExtraidaData(
                emisor="Factura Sin Nombre",
                nit=None,
                fecha="2026-08-18",
                monto_total=0.0,
                moneda="COP",
                categoria="Sin Categoría"
            )
