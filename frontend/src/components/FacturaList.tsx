import React from 'react';
import { useFacturas } from '../context/FacturaContext';
import { FacturaCard } from './FacturaCard';

export const FacturaList: React.FC = () => {
  const { facturas, loading, error } = useFacturas();

  return (
    <section className="factura-list-container">
      <h2>2. Historial de Facturas Escaneadas</h2>
      {error && <div className="error-banner">⚠️ {error}</div>}
      {loading && facturas.length === 0 && <p className="loading-text">Cargando facturas...</p>}
      {!loading && facturas.length === 0 && (
        <p className="empty-text">No hay facturas procesadas aún. Escanea la primera factura arriba.</p>
      )}
      <div className="factura-grid">
        {facturas.map((factura) => (
          <FacturaCard key={factura.id} factura={factura} />
        ))}
      </div>
    </section>
  );
};
