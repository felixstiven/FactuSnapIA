import React, { useRef, useState } from 'react';
import { useFacturas } from '../context/FacturaContext';
import { processImageCanvas } from '../utils/canvasFilter';

export const CameraScanner: React.FC = () => {
  const { scanFactura, loading } = useFacturas();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [capturedBlob, setCapturedBlob] = useState<Blob | null>(null);

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Crear un objeto de imagen para procesarlo en el Canvas
    const img = new Image();
    img.src = URL.createObjectURL(file);
    img.onload = async () => {
      try {
        const result = await processImageCanvas(img);
        setPreview(result.dataUrl);
        setCapturedBlob(result.blob);
      } catch (err) {
        console.error('Error al procesar imagen en canvas:', err);
      }
    };
  };

  const handleProcessScan = async () => {
    if (!capturedBlob) return;
    try {
      await scanFactura(capturedBlob);
      // Limpiar estado tras proceso exitoso
      setPreview(null);
      setCapturedBlob(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
    } catch (err) {
      // El error es manejado en el contexto
    }
  };

  return (
    <section className="scanner-container">
      <h2>1. Capturar Factura</h2>
      <div className="scanner-box">
        {preview ? (
          <div className="preview-container">
            <img src={preview} alt="Vista previa de factura" className="image-preview" />
            <div className="action-buttons">
              <button 
                onClick={() => { setPreview(null); setCapturedBlob(null); }} 
                className="btn btn-secondary"
                disabled={loading}
              >
                🔄 Repetir Foto
              </button>
              <button 
                onClick={handleProcessScan} 
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? '⚡ Procesando IA...' : '🚀 Enviar a Gemini AI'}
              </button>
            </div>
          </div>
        ) : (
          <div className="upload-prompt">
            <p>📷 Captura con la cámara o selecciona una imagen (JPG/PNG max 10MB)</p>
            <input
              type="file"
              accept="image/jpeg,image/png"
              capture="environment"
              onChange={handleFileChange}
              ref={fileInputRef}
              style={{ display: 'none' }}
              id="camera-input"
            />
            <label htmlFor="camera-input" className="btn btn-scan">
              📷 Abrir Cámara / Seleccionar Imagen
            </label>
          </div>
        )}
      </div>
    </section>
  );
};
