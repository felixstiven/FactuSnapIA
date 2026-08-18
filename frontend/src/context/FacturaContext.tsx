/**
 * 🎓 APRENDIZAJE FRONTEND: CONTEXT API DE REACT
 * 
 * Gestiona el estado global de la aplicación FactuSnap AI:
 *  - Lista de facturas procesadas.
 *  - Estado de carga (escaneando / procesando con IA).
 *  - Manejo de errores de conexión HTTP / servidor.
 */

import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import { uploadFacturaImage, fetchFacturasList, type FacturaItem } from '../services/apiClient';

interface FacturaContextType {
  facturas: FacturaItem[];
  loading: boolean;
  error: string | null;
  scanFactura: (imageBlob: Blob) => Promise<void>;
  cargarFacturas: () => Promise<void>;
  clearError: () => void;
}

const FacturaContext = createContext<FacturaContextType | undefined>(undefined);

export const FacturaProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [facturas, setFacturas] = useState<FacturaItem[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const cargarFacturas = async () => {
    try {
      setLoading(true);
      const data = await fetchFacturasList();
      setFacturas(data);
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'No se pudieron cargar las facturas');
    } finally {
      setLoading(false);
    }
  };

  const scanFactura = async (imageBlob: Blob) => {
    try {
      setLoading(true);
      setError(null);
      const nuevaFactura = await uploadFacturaImage(imageBlob);
      setFacturas((prev) => [nuevaFactura, ...prev]);
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Error al procesar la factura');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const clearError = () => setError(null);

  useEffect(() => {
    cargarFacturas();
  }, []);

  return (
    <FacturaContext.Provider
      value={{
        facturas,
        loading,
        error,
        scanFactura,
        cargarFacturas,
        clearError,
      }}
    >
      {children}
    </FacturaContext.Provider>
  );
};

export const useFacturas = (): FacturaContextType => {
  const context = useContext(FacturaContext);
  if (!context) {
    throw new Error('useFacturas debe ser usado dentro de un FacturaProvider');
  }
  return context;
};
