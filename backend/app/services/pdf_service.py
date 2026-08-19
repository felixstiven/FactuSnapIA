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
                
                # 1. Convertir a escala de grises para análisis
                gray = np.mean(img_np, axis=2)
                
                # 2. Detectar el papel (es más claro que el fondo oscuro)
                # Un umbral dinámico o fijo (ej. 140) separa el papel de la silla
                threshold = np.mean(gray) * 1.1 # Ligeramente arriba del promedio
                if threshold > 200: threshold = 180
                
                mask = gray > threshold
                
                # 3. Pintar todo lo que NO sea papel de BLANCO PURO
                img_np[~mask] = [255, 255, 255]
                
                # Convertir de vuelta a imagen PIL
                img_rgb = Image.fromarray(np.uint8(img_np))
                
                # 4. Obtener cuadro delimitador para recortar bordes blancos excesivos
                bbox = img_rgb.convert("L").point(lambda p: 255 if p < 250 else 0).getbbox()
                if bbox:
                    x_min, y_min, x_max, y_max = bbox
                    w, h = img_rgb.size
                    x_min = max(0, x_min - 20)
                    y_min = max(0, y_min - 20)
                    x_max = min(w, x_max + 20)
                    y_max = min(h, y_max + 20)
                    img_rgb = img_rgb.crop((x_min, y_min, x_max, y_max))

        except Exception as e:
            print(f"Aviso al procesar fondo: {e}")

        # 5. Efecto Escáner: Convertir a grises y forzar el contraste al máximo
        from PIL import ImageOps
        img_rgb = ImageOps.grayscale(img_rgb).convert("RGB")
        contrast_enhancer = ImageEnhance.Contrast(img_rgb)
        img_rgb = contrast_enhancer.enhance(2.0)
        brightness_enhancer = ImageEnhance.Brightness(img_rgb)
        img_rgb = brightness_enhancer.enhance(1.2)

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
