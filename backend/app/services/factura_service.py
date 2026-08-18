"""
=============================================================================
📚 SERVICIO PRINCIPAL DE LÓGICA DE NEGOCIO (Factura Service)
=============================================================================
CAPA DE ARQUITECTURA LIMPIA: SERVICE
-----------------------------------------------------------------------------
Orquesta la lógica de negocio completa:
 1. Llama a PDFService para sanitizar la imagen y convertirla a PDF.
 2. Llama a AIService para procesar la imagen con Gemini 1.5 Flash.
 3. Llama a FacturaRepository para guardar el PDF en Supabase Storage 
    y el registro en la base de datos PostgreSQL de Supabase.
=============================================================================
"""

import uuid
from typing import List, Dict, Any
from app.services.pdf_service import PDFService
from app.services.ai_service import AIService
from app.repositories.factura_repository import FacturaRepository

class FacturaService:
    def __init__(self):
        self.pdf_service = PDFService()
        self.ai_service = AIService()
        self.repository = FacturaRepository()

    def procesar_y_guardar_factura(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Orquestación completa del flujo de negocio.
        """
        # 1. Sanitizar imagen y generar PDF (Pillow)
        pdf_bytes, pil_image = self.pdf_service.sanitizar_y_convertir_a_pdf(image_bytes)

        # 2. Extraer datos estructurados con Gemini 1.5 Flash
        factura_data = self.ai_service.procesar_imagen_factura(pil_image)

        # 3. Guardar PDF en Supabase Storage
        file_name = f"factura_{uuid.uuid4().hex[:8]}.pdf"
        pdf_url = self.repository.subir_pdf_storage(pdf_bytes, file_name)

        # 4. Guardar registro en Supabase PostgreSQL
        registro_guardado = self.repository.guardar_factura_db(factura_data, pdf_url)
        return registro_guardado

    def listar_facturas(self) -> List[Dict[str, Any]]:
        return self.repository.obtener_todas_facturas()
