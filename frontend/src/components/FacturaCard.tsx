import React from 'react';
import type { FacturaItem } from '../services/apiClient';

interface FacturaCardProps {
  factura: FacturaItem;
}

export const FacturaCard: React.FC<FacturaCardProps> = ({ factura }) => {
  return (
    <article className="factura-card">
      <div className="card-header">
        <h3>{factura.emisor}</h3>
        <span className="categoria-badge">{factura.categoria || 'General'}</span>
      </div>
      <div className="card-body">
        <p><strong>NIT:</strong> {factura.nit || 'N/A'}</p>
        <p><strong>Fecha:</strong> {factura.fecha}</p>
        <p className="monto">
          <strong>Total:</strong> {factura.monto_total.toLocaleString('es-CO')} {factura.moneda}
        </p>
        <p className="impuestos">
          <strong>Impuestos:</strong> {factura.impuestos ? factura.impuestos.toLocaleString('es-CO') : '0'} {factura.moneda}
        </p>
      </div>
      <div className="card-footer">
        <a 
          href={factura.pdf_url} 
          target="_blank" 
          rel="noopener noreferrer" 
          className="btn btn-pdf"
        >
          📄 Ver / Descargar PDF (Supabase)
        </a>
      </div>
    </article>
  );
};
