# ⚛️ Módulo 05: Frontend con React, TypeScript y Context API

En este módulo aprenderás cómo funciona la interfaz de usuario de **FactuSnap**, cómo manejamos la cámara, el envío de imágenes pesadas por HTTP y la sincronización del estado global con React Context.

---

## 🏗️ 1. El Ecosistema Frontend

- **Vite:** Herramienta ultrarrápida de empaquetado y servidor de desarrollo.
- **React 18:** Librería para construir interfaces basadas en componentes reutilizables.
- **TypeScript:** Agrega tipado estático a JavaScript, atrapando errores tipográficos antes de ejecutar el código.
- **pnpm:** Gestor de paquetes rápido y eficiente en disco.

---

## 📑 2. El Contrato de Datos: TypeScript Interfaces

En `frontend/src/services/apiClient.ts`, definimos el contrato de datos que coincide exactamente con el modelo Pydantic de Python:

```typescript
export interface FacturaItem {
  id: string;
  emisor: string;
  nit: string | null;
  fecha: string;
  monto_total: number;
  impuestos: number;
  moneda: string;
  categoria: string;
  pdf_url: string;
  created_at: string;
}
```
**¿Por qué es vital TypeScript?**  
Si escribes por error `factura.monto_totl` en un componente, TypeScript marcará una línea roja antes de compilar avisándote que la propiedad no existe.

---

## 📡 3. Envío de Archivos Binarios (`multipart/form-data`)

Para enviar una imagen desde el navegador al servidor FastAPI, no usamos un JSON normal, sino un objeto especial llamado `FormData`:

```typescript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/facturas';

export const uploadFacturaImage = async (imageBlob: Blob): Promise<FacturaItem> => {
  const formData = new FormData();
  // 'file' coincide con el parámetro en FastAPI: def scan_factura(file: UploadFile = File(...))
  formData.append('file', imageBlob, 'factura_capturada.jpg');

  const response = await axios.post<FacturaItem>(`${API_BASE_URL}/scan`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};
```

---

## 🌐 4. Estado Global con Context API (`FacturaContext.tsx`)

En React, si quieres que la lista de facturas se actualice automáticamente cuando la cámara termine de escanear una nueva, usamos un **Contexto Global**:

```typescript
export const FacturaProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [facturas, setFacturas] = useState<FacturaItem[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Cargar facturas iniciales al abrir la app
  useEffect(() => {
    fetchFacturas();
  }, []);

  const handleScanFactura = async (imageBlob: Blob) => {
    setLoading(true);
    setError(null);
    try {
      const nuevaFactura = await uploadFacturaImage(imageBlob);
      // Añadir la nueva factura al principio de la lista
      setFacturas((prev) => [nuevaFactura, ...prev]);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al procesar la factura.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <FacturaContext.Provider value={{ facturas, loading, error, handleScanFactura }}>
      {children}
    </FacturaContext.Provider>
  );
};
```

**Beneficios del Context:**
- Cualquier componente hijo (el escáner de cámara o la lista de tarjetas) puede llamar a `handleScanFactura` o leer la lista `facturas` sin tener que pasar props de padre a hijo repetidamente.

---

## 🃏 5. Componente Visual (`FacturaCard.tsx`)

```tsx
export const FacturaCard: React.FC<{ factura: FacturaItem }> = ({ factura }) => {
  return (
    <div className="factura-card">
      <div className="header">
        <h3>{factura.emisor}</h3>
        <span className="badge">{factura.categoria}</span>
      </div>
      <p><strong>Fecha:</strong> {factura.fecha}</p>
      <p className="total">
        <strong>Total:</strong> {factura.monto_total.toLocaleString('es-CO')} {factura.moneda}
      </p>
      <p className="impuestos">
        <strong>Impuestos:</strong> {factura.impuestos ? factura.impuestos.toLocaleString('es-CO') : '0'} {factura.moneda}
      </p>
      {factura.pdf_url && (
        <a href={factura.pdf_url} target="_blank" rel="noreferrer" className="btn-pdf">
          📄 Ver / Descargar PDF (Supabase)
        </a>
      )}
    </div>
  );
};
```

---

## 🎉 ¡Has completado la Ruta de Aprendizaje!

Ahora conoces:
1. Cómo estructurar un Backend escalable con **FastAPI y Arquitectura Limpia**.
2. Cómo procesar imágenes píxel a píxel con **Pillow y NumPy**.
3. Cómo extraer información estructurada con **Google Gemini AI**.
4. Cómo almacenar archivos y tablas relacionales con **Supabase**.
5. Cómo conectar todo de forma reactiva y tipada con **React y TypeScript**.

👉 Vuelve al índice en cualquier momento: [00_RUTA_DE_APRENDIZAJE.md](file:///c:/Users/Yaorj/Documents/FactuSnap/docs/00_RUTA_DE_APRENDIZAJE.md)
