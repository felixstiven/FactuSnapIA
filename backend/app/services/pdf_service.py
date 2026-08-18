"""
=============================================================================
📚 SERVICIO DE PROCESAMIENTO DE IMAGEN Y CONVERSIÓN A PDF (Pillow)
=============================================================================
CAPA DE ARQUITECTURA LIMPIA: SERVICE (PDF & Image Processing)
-----------------------------------------------------------------------------
PROTECCIÓN OWASP MEDIDA 1 (Unrestricted File Upload & Malicious Injection):
La imagen cargada por el usuario es re-procesada y decodificada utilizando 
Pillow. Esto destruye metadatos EXIF, payloads binarios incrustados o scripts 
maliciosos ocultos en los bytes del archivo original antes de convertirla a PDF.
=============================================================================
"""

import io
from PIL import Image

class PDFService:
    @staticmethod
    def sanitizar_y_convertir_a_pdf(image_bytes: bytes) -> tuple[bytes, Image.Image]:
        """
        1. Abre los bytes de la imagen con Pillow (destruye cargas maliciosas binarias).
        2. Convierte la imagen a modo RGB.
        3. Guarda la imagen saneada en un buffer de memoria en formato PDF.
        Retorna (pdf_bytes, pil_image_saneada).
        """
        # OWASP: Decodificación y sanitización de imagen
        input_buffer = io.BytesIO(image_bytes)
        pil_image = Image.open(input_buffer)
        
        # Forzar conversión a RGB (requerido para guardar como PDF)
        if pil_image.mode in ("RGBA", "P"):
            pil_image = pil_image.convert("RGB")
        
        # Generar PDF en memoria
        output_buffer = io.BytesIO()
        pil_image.save(output_buffer, format="PDF", resolution=100.0)
        pdf_bytes = output_buffer.getvalue()
        
        return pdf_bytes, pil_image
