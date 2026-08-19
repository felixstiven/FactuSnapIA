# 🗄️ Módulo 04: Base de Datos y Storage con Supabase

En este módulo aprenderás cómo gestionamos el almacenamiento de archivos binarios (PDFs) y los datos relacionales en la nube usando **Supabase (PostgreSQL)**.

---

## ☁️ 1. ¿Qué es Supabase?

**Supabase** es una plataforma en la nube construida sobre **PostgreSQL**, la base de datos relacional de código abierto más potente del mundo. Nos proporciona dos servicios principales:

1. **Database (PostgreSQL Relacional)**: Tablas organizadas en filas y columnas para guardar textos, fechas y números.
2. **Storage (Almacenamiento de Objetos / S3 Compatible)**: Espacio en disco en la nube para guardar archivos pesados (imágenes, PDFs, audios).

---

## 🚫 Regla de Oro: ¿Por qué NO guardar PDFs dentro de la Base de Datos?

Un error muy común de principiantes es intentar guardar el archivo PDF completo en una columna de texto o tipo BLOB en la base de datos.
- **Razón técnica:** Las bases de datos SQL están optimizadas para buscar y filtrar datos pequeños (números, strings). Si guardas archivos de 2 MB en cada fila, la base de datos se vuelve extremadamente pesada, lenta y costosa de respaldar.
- **La Solución Profesional:**
  1. El archivo PDF se sube a **Supabase Storage**.
  2. Supabase nos entrega un enlace público URL (ej: `https://.../facturas-pdf/recibo.pdf`).
  3. En la tabla SQL **solo guardamos ese enlace de texto**, junto a los datos de emisor, fecha y total.

---

## 🧹 2. Sanitización de Nombres de Archivo (ASCII & Unicode)

Al subir un archivo a un Storage en la nube, caracteres con tildes (ej: `Baterías_Bogotá.pdf`) o símbolos raros generan errores HTTP `400 InvalidKey`.

### Cómo lo solucionamos en `factura_service.py`:
```python
import unicodedata

# 1. Eliminar acentos: "Baterías" -> "Baterias"
emisor_sin_tildes = unicodedata.normalize('NFKD', factura_data.emisor).encode('ASCII', 'ignore').decode('utf-8')

# 2. Reemplazar espacios y caracteres no alfanuméricos
safe_emisor = "".join(c for c in emisor_sin_tildes if c.isalnum() or c in " _-").strip().replace(" ", "_")

# 3. Construir nombre estándar: Emisor_Fecha_MontoMoneda.pdf
file_name = f"{safe_emisor}_{factura_data.fecha}_{factura_data.monto_total}{factura_data.moneda}.pdf"
```

---

## 🏛️ 3. El Patrón Repository (`factura_repository.py`)

El archivo `backend/app/repositories/factura_repository.py` es el único que conoce las credenciales y la librería de Supabase:

```python
from supabase import create_client, Client
from app.config import settings
from app.models.factura_model import FacturaExtraidaData

class FacturaRepository:
    def __init__(self):
        # Conexión con Supabase usando URL y API KEY del archivo .env
        self.client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.bucket_name = "facturas-pdf"
        self.table_name = "facturas"

    def subir_pdf_storage(self, pdf_bytes: bytes, file_name: str) -> str:
        """Sube el archivo binario PDF a Supabase Storage y retorna su URL pública."""
        self.client.storage.from_(self.bucket_name).upload(
            file_name,
            pdf_bytes,
            file_options={"content-type": "application/pdf"}
        )
        return self.client.storage.from_(self.bucket_name).get_public_url(file_name)

    def guardar_factura_db(self, data: FacturaExtraidaData, pdf_url: str):
        """Inserta una nueva fila en la tabla PostgreSQL."""
        payload = {
            "emisor": data.emisor,
            "nit": data.nit,
            "fecha": data.fecha,
            "monto_total": data.monto_total,
            "impuestos": data.impuestos,
            "moneda": data.moneda,
            "categoria": data.categoria,
            "pdf_url": pdf_url
        }
        response = self.client.table(self.table_name).insert(payload).execute()
        return response.data[0]
```

---

## 🛠️ 4. Modificaciones de Esquema SQL (DDL)

Cuando agregamos una nueva propiedad en la aplicación (como los `impuestos`), la tabla de la base de datos debe actualizarse para conocer esa nueva columna:

```sql
ALTER TABLE facturas ADD COLUMN impuestos float8 DEFAULT 0;
```
- `ALTER TABLE facturas`: Modifica la estructura de la tabla existente.
- `ADD COLUMN impuestos`: Crea una nueva columna llamada `impuestos`.
- `float8`: Tipo de dato numérico de doble precisión (números decimales).
- `DEFAULT 0`: Si hay facturas antiguas que no tenían impuestos, les asigna `0` para no generar errores nulos.

---

### ➡️ Siguiente Módulo:
Descubre cómo el Frontend en React se comunica con esta API y presenta los datos:  
👉 [Módulo 05: Frontend con React, TypeScript y Context API](file:///c:/Users/Yaorj/Documents/FactuSnap/docs/05_FRONTEND_REACT_TS.md)
