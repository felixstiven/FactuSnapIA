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
        img_rgb = pil_img.convert("RGB")
        try:
            if np is not None:
                img_np = np.array(img_rgb)
                # Convertir a grises
                gray = np.mean(img_np, axis=2)
                
                # El recibo es muy blanco. Umbral estricto para ignorar fondos claros
                mask = gray > 165
                
                # Contar pixeles blancos por fila y columna
                row_counts = np.sum(mask, axis=1)
                col_counts = np.sum(mask, axis=0)
                
                # Una fila/columna es recibo si tiene >15% de su longitud en blanco
                h, w = gray.shape
                row_mask = row_counts > (w * 0.15)
                col_mask = col_counts > (h * 0.15)
                
                if np.any(row_mask) and np.any(col_mask):
                    y_min = np.argmax(row_mask)
                    y_max = len(row_mask) - np.argmax(row_mask[::-1])
                    
                    x_min = np.argmax(col_mask)
                    x_max = len(col_mask) - np.argmax(col_mask[::-1])
                    
                    # Añadir margen
                    x_min = max(0, x_min - 15)
                    y_min = max(0, y_min - 15)
                    x_max = min(w, x_max + 15)
                    y_max = min(h, y_max + 15)
                    
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
