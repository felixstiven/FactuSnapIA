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
from PIL import Image, ImageEnhance, ImageOps

try:
    # pyrefly: ignore [missing-import]
    import numpy as np
except ImportError:
    np = None

class PDFService:
    @staticmethod
    def recortar_y_limpiar_fondo(pil_img: Image.Image) -> Image.Image:
        """
        Detecta la región de papel de la factura (zonas claras) y recorta el fondo (sillas, mesas, etc.).
        Aplica un filtro de contraste y brillo para asegurar un fondo blanco limpio estilo escáner.
        """
        img_rgb = pil_img.convert("RGB")
        try:
            # 1. Convertir a grises
            gray = img_rgb.convert("L")
            # 2. Aislar los pixeles claros (el papel de la factura) con umbral 160
            mask = gray.point(lambda p: 255 if p > 160 else 0)
            # 3. Obtener el cuadro delimitador del papel blanco
            bbox = mask.getbbox()
            
            if bbox:
                x_min, y_min, x_max, y_max = bbox
                w, h = img_rgb.size
                
                # Añadir un pequeño margen de 15px para no cortar el texto
                x_min = max(0, x_min - 15)
                y_min = max(0, y_min - 15)
                x_max = min(w, x_max + 15)
                y_max = min(h, y_max + 15)

                # Solo recortar si el area detectada es al menos el 20% de la imagen
                # (evita recortes erróneos de brillos aislados)
                if (x_max - x_min) > w * 0.2 and (y_max - y_min) > h * 0.2:
                    img_rgb = img_rgb.crop((x_min, y_min, x_max, y_max))
        except Exception as e:
            print(f"Aviso al recortar imagen: {e}")

        # Realce de contraste y nitidez (Efecto Escáner PDF)
        contrast_enhancer = ImageEnhance.Contrast(img_rgb)
        img_rgb = contrast_enhancer.enhance(1.4)

        brightness_enhancer = ImageEnhance.Brightness(img_rgb)
        img_rgb = brightness_enhancer.enhance(1.1)

        return img_rgb

    @staticmethod
    def sanitizar_y_convertir_a_pdf(image_bytes: bytes) -> tuple[bytes, Image.Image]:
        """
        1. Abre e higieniza la imagen original con Pillow.
        2. Recorta el fondo y aplica filtro de blanco escáner.
        3. Convierte a PDF listo para almacenar.
        """
        input_buffer = io.BytesIO(image_bytes)
        pil_image = Image.open(input_buffer)
        
        if pil_image.mode in ("RGBA", "P"):
            pil_image = pil_image.convert("RGB")
        
        # Procesar recorte de fondo y realce escáner para el PDF
        pil_image_limpia = PDFService.recortar_y_limpiar_fondo(pil_image)

        # Generar PDF en memoria con la imagen limpia
        output_buffer = io.BytesIO()
        pil_image_limpia.save(output_buffer, format="PDF", resolution=100.0)
        pdf_bytes = output_buffer.getvalue()
        
        # IMPORTANTE: Retornar la imagen original (pil_image) a la IA, no la limpia.
        # La IA es experta leyendo la foto original, los filtros pueden borrar texto tenue.
        return pdf_bytes, pil_image
