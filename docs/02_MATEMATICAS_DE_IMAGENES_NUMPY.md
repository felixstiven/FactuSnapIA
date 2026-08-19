# 🔬 Módulo 02: Procesamiento de Imágenes con Pillow y NumPy

En este módulo aprenderás cómo funciona el procesamiento de imágenes digitales y la técnica matemática que usamos en **FactuSnap** para eliminar fondos oscuros (como la silla de un auto o una mesa de madera) y lograr un efecto escáner profesional.

---

## 🖼️ 1. ¿Cómo ve una computadora una imagen?

Para los humanos, una foto es un dibujo con colores. Para una computadora, una imagen es simplemente una **tabla gigante de números** (una matriz):

- Una foto a color tiene 3 canales: **Rojo (R), Verde (G) y Azul (B)**.
- Cada píxel tiene valores entre `0` (totalmente negro) y `255` (blanco brillante).
- Si una foto mide `1000 x 800` píxeles, tiene `800,000` píxeles, y en RGB son `2,400,000` números almacenados en memoria.

---

## ⚡ 2. Las Librerías: Pillow vs NumPy

| Librería | ¿Qué es? | ¿Para qué la usamos en FactuSnap? |
| :--- | :--- | :--- |
| **Pillow (`PIL`)** | Librería estándar de Python para abrir, redimensionar, guardar y convertir formatos (JPEG, PNG, PDF). | Cargar la imagen recibida por el usuario, recortar bordes y generar el archivo binario PDF final. |
| **NumPy (`np`)** | Librería de cálculo numérico ultrarrápido en C para trabajar con matrices multidimensionales. | Operaciones matemáticas sobre millones de píxeles en milisegundos para filtrar sombras y fondos. |

---

## 🪄 3. El Algoritmo del "Efecto Escáner" (Línea por Línea)

En `backend/app/services/pdf_service.py`, implementamos un algoritmo llamado **Adaptive Thresholding (Umbral Adaptativo por División Gaussiana)**.

```python
import io
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

class PDFService:
    @staticmethod
    def recortar_y_limpiar_fondo(pil_img: Image.Image) -> Image.Image:
        try:
            if np is not None:
                # 1. Convertir a Escala de Grises (1 solo canal de luz de 0 a 255)
                gray_img = pil_img.convert("L")
                gray_np = np.array(gray_img).astype(float)
                
                # 2. Crear una versión desenfocada (representa la iluminación del entorno)
                blur_img = gray_img.filter(ImageFilter.GaussianBlur(radius=25))
                blur_np = np.array(blur_img).astype(float)
                
                # 3. División Adaptativa:
                # Píxel original dividido por la iluminación de su vecindario
                result_np = (gray_np / (blur_np + 1)) * 255
                result_np = np.clip(result_np, 0, 255).astype(np.uint8)
                
                # Convertir la matriz de vuelta a imagen de Pillow
                img_rgb = Image.fromarray(result_np).convert("RGB")
                
                # 4. Recorte automático de márgenes blancos vacíos
                bbox = img_rgb.convert("L").point(lambda p: 255 if p < 250 else 0).getbbox()
                if bbox:
                    x_min, y_min, x_max, y_max = bbox
                    w, h = img_rgb.size
                    x_min = max(0, x_min - 20)
                    y_min = max(0, y_min - 20)
                    x_max = min(w, x_max + 20)
                    y_max = min(h, y_max + 20)
                    img_rgb = img_rgb.crop((x_min, y_min, x_max, y_max))
            else:
                img_rgb = pil_img.convert("RGB")

        except Exception as e:
            print(f"Aviso al procesar fondo adaptativo: {e}")
            img_rgb = pil_img.convert("RGB")

        # 5. Realce de Contraste y Brillo
        contrast_enhancer = ImageEnhance.Contrast(img_rgb)
        img_rgb = contrast_enhancer.enhance(2.0)
        brightness_enhancer = ImageEnhance.Brightness(img_rgb)
        img_rgb = brightness_enhancer.enhance(1.2)

        return img_rgb
```

---

## 🧠 ¿Por qué funciona la división `gray_np / (blur_np + 1)`?

Imagina dos situaciones en la misma foto:

### Caso 1: La Silla Oscura de Fondo
- Un píxel de la silla tiene un brillo de `80` (marrón oscuro).
- Los píxeles alrededor de él también son de la silla (`80`).
- Al aplicar el desenfoque (`GaussianBlur`), el promedio local es `80`.
- **La fórmula calcula:** `(80 / 80) * 255 = 1.0 * 255 = 255` (**¡Blanco Puro!**).
- **Resultado:** ¡La silla desaparece por completo y se vuelve blanca!

### Caso 2: El Texto Negro sobre el Papel Blanco
- Un píxel de una letra tiene un brillo de `20` (tinta negra).
- El papel alrededor de la letra tiene un brillo de `220` (papel blanco).
- Al aplicar el desenfoque, el promedio local es alto (ej. `200`).
- **La fórmula calcula:** `(20 / 200) * 255 = 0.1 * 255 = 25.5` (**¡Negro Intenso!**).
- **Resultado:** La letra se mantiene nítida, oscura y perfectamente legible.

---

## 🔒 4. Seguridad OWASP: Conversión a PDF

```python
    def sanitizar_y_convertir_a_pdf(self, image_bytes: bytes):
        input_buffer = io.BytesIO(image_bytes)
        pil_image = Image.open(input_buffer)

        # Limpiar y realzar
        imagen_limpia = self.recortar_y_limpiar_fondo(pil_image)

        # Generar PDF en memoria RAM
        pdf_buffer = io.BytesIO()
        imagen_limpia.save(pdf_buffer, format="PDF", resolution=100.0)
        pdf_bytes = pdf_buffer.getvalue()

        return pdf_bytes, imagen_limpia
```

**Medida de Ciberseguridad (OWASP File Upload Security):**
Los hackers a veces incrustan código PHP, JavaScript o virus dentro de los metadatos de las imágenes JPEG/PNG. 
Al decodificar la imagen píxel por píxel con `Image.open` y re-ensamblarla como un nuevo archivo `PDF` limpio en memoria RAM (`io.BytesIO`), **cualquier virus o script malicioso incrustado es completamente destruido**.

---

### ➡️ Siguiente Módulo:
Descubre cómo se conecta la Inteligencia Artificial de Google para entender el texto de la factura:  
👉 [Módulo 03: Integración con IA Google Gemini](file:///c:/Users/Yaorj/Documents/FactuSnap/docs/03_INTELIGENCIA_ARTIFICIAL_GEMINI.md)
