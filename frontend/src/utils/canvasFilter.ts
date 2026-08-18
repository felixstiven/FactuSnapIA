/**
 * 🎓 APRENDIZAJE FRONTEND: PROCESAMIENTO DE IMAGEN EN CANVAS
 * 
 * Limpia y optimiza la imagen capturada por la cámara WebRTC antes de 
 * enviarla al servidor. Mejora el contraste y nitidez para optimizar el 
 * OCR del modelo Gemini 1.5 Flash.
 */

export interface ProcessedCanvasResult {
  blob: Blob;
  dataUrl: string;
}

export const processImageCanvas = (
  imageElement: HTMLImageElement | HTMLVideoElement,
  maxWidth = 1600
): Promise<ProcessedCanvasResult> => {
  return new Promise((resolve, reject) => {
    try {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');

      if (!ctx) {
        throw new Error('No se pudo obtener el contexto 2D del Canvas');
      }

      // Calcular proporciones manteniendo relación de aspecto
      let width = imageElement instanceof HTMLVideoElement ? imageElement.videoWidth : imageElement.width;
      let height = imageElement instanceof HTMLVideoElement ? imageElement.videoHeight : imageElement.height;

      if (width > maxWidth) {
        height = Math.round((height * maxWidth) / width);
        width = maxWidth;
      }

      canvas.width = width;
      canvas.height = height;

      // Dibujar imagen original
      ctx.drawImage(imageElement, 0, 0, width, height);

      // Aplicar filtro de contraste y brillo ligero para mejorar legibilidad de texto
      const imageData = ctx.getImageData(0, 0, width, height);
      const data = imageData.data;

      for (let i = 0; i < data.length; i += 4) {
        // Aumentar ligeramente el contraste
        const factor = 1.15; // 15% más contraste
        data[i] = Math.min(255, (data[i] - 128) * factor + 128);     // Rojo
        data[i + 1] = Math.min(255, (data[i + 1] - 128) * factor + 128); // Verde
        data[i + 2] = Math.min(255, (data[i + 2] - 128) * factor + 128); // Azul
      }

      ctx.putImageData(imageData, 0, 0);

      // Convertir a Blob JPEG de alta calidad
      canvas.toBlob(
        (blob) => {
          if (blob) {
            const dataUrl = canvas.toDataURL('image/jpeg', 0.9);
            resolve({ blob, dataUrl });
          } else {
            reject(new Error('Fallo al generar Blob de la imagen'));
          }
        },
        'image/jpeg',
        0.9
      );
    } catch (error) {
      reject(error);
    }
  });
};
