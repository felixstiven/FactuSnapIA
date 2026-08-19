/**
 * 🎓 APRENDIZAJE FRONTEND: CLIENTE API HTTP
 * 
 * Centraliza las peticiones hacia la IP de Tailscale del backend en FastAPI.
 * Envía la imagen limpia capturada en FormData.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export interface FacturaItem {
  id: string;
  emisor: string;
  nit: string | null;
  fecha: string;
  monto_total: number;
  impuestos: number;
  moneda: string;
  categoria: string | null;
  pdf_url: string;
  created_at?: string;
}

export const uploadFacturaImage = async (imageBlob: Blob): Promise<FacturaItem> => {
  const formData = new FormData();
  formData.append('file', imageBlob, 'factura_scan.jpg');

  const response = await fetch(`${API_BASE_URL}/api/facturas/scan`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Error al procesar la factura en el servidor');
  }

  return await response.json();
};

export const fetchFacturasList = async (): Promise<FacturaItem[]> => {
  const response = await fetch(`${API_BASE_URL}/api/facturas`);
  if (!response.ok) {
    throw new Error('Error al obtener la lista de facturas');
  }
  return await response.json();
};
