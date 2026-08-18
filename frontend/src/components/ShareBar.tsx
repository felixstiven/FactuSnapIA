import React from 'react';
import { useFacturas } from '../context/FacturaContext';

export const ShareBar: React.FC = () => {
  const { facturas } = useFacturas();

  const totalGastado = facturas.reduce((acc, curr) => acc + (curr.monto_total || 0), 0);

  const handleShare = async () => {
    const text = `📊 Resumen FactuSnap AI:\nFacturas procesadas: ${facturas.length}\nTotal acumulado: $${totalGastado.toLocaleString('es-CO')} COP`;

    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Resumen de Facturas - FactuSnap AI',
          text: text,
        });
      } catch (err) {
        console.log('Compartir cancelado');
      }
    } else {
      navigator.clipboard.writeText(text);
      alert('Resumen copiado al portapapeles');
    }
  };

  return (
    <footer className="share-bar">
      <div className="summary-info">
        <span><strong>Total acumulado:</strong> ${totalGastado.toLocaleString('es-CO')} COP</span>
        <span><strong>Procesadas:</strong> {facturas.length}</span>
      </div>
      <button onClick={handleShare} className="btn btn-share">
        📤 Compartir Resumen
      </button>
    </footer>
  );
};
