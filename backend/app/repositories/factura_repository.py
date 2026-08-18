"""
=============================================================================
📚 MÓDULO REPOSITORIO: INTERACCIÓN CON SUPABASE (FactuSnap AI)
=============================================================================
CAPA DE ARQUITECTURA LIMPIA: REPOSITORY
-----------------------------------------------------------------------------
El Repositorio es la única capa autorizada para comunicarse directamente 
con la fuente de datos externa (en este caso, Supabase).

APRENDIZAJE DIDÁCTICO DE SUPABASE:
1. Cliente Supabase: Se inicializa con 'create_client(url, key)'.
2. Supabase Storage: 'supabase.storage.from_(bucket).upload(path, file_bytes)'
   sube archivos binarios (como un PDF) al bucket de la nube.
3. Supabase DB (PostgreSQL): 'supabase.table("facturas").insert(data)' 
   ejecuta un INSERT en la tabla PostgreSQL y retorna la fila insertada.
=============================================================================
"""

import uuid
from typing import List, Dict, Any
from supabase import create_client, Client
from app.config import settings
from app.models.factura_model import FacturaExtraidaData

class FacturaRepository:
    def __init__(self):
        # 🎓 PASO 1: Inicialización del cliente oficial de Supabase
        # Se requiere la SUPABASE_URL y SUPABASE_KEY desde la configuración.
        self.url: str = settings.SUPABASE_URL
        self.key: str = settings.SUPABASE_KEY
        self.bucket_name: str = settings.SUPABASE_STORAGE_BUCKET
        
        if self.url and self.key:
            self.client: Client = create_client(self.url, self.key)
        else:
            self.client = None

    def subir_pdf_storage(self, pdf_bytes: bytes, file_name: str) -> str:
        """
        🎓 EXPLICACIÓN SUPABASE STORAGE:
        Subes un array de bytes directamente a un Bucket de Almacenamiento en Supabase.
        Retorna la URL pública accesible para descargar o compartir el PDF.
        """
        if not self.client:
            # Fallback didáctico en caso de entorno local sin credenciales aún
            return f"https://placeholder.supabase.co/storage/v1/object/public/{self.bucket_name}/{file_name}"

        # Subir archivo al bucket de Supabase
        res = self.client.storage.from_(self.bucket_name).upload(
            path=file_name,
            file=pdf_bytes,
            file_options={"content-type": "application/pdf"}
        )
        
        # Obtener la URL pública del archivo cargado
        public_url = self.client.storage.from_(self.bucket_name).get_public_url(file_name)
        return public_url

    def guardar_factura_db(self, factura_data: FacturaExtraidaData, pdf_url: str) -> Dict[str, Any]:
        """
        🎓 EXPLICACIÓN SUPABASE POSTGRESQL:
        Insertar un objeto JSON en una tabla PostgreSQL mediante la API sintáctica de Supabase.
        .table("nombre_tabla").insert({...}).execute()
        """
        record = {
            "id": str(uuid.uuid4()),
            "emisor": factura_data.emisor,
            "nit": factura_data.nit,
            "fecha": factura_data.fecha,
            "monto_total": factura_data.monto_total,
            "moneda": factura_data.moneda,
            "categoria": factura_data.categoria,
            "pdf_url": pdf_url
        }

        if not self.client:
            # Mock de respuesta local en modo de prueba pedagógico
            return record

        response = self.client.table("facturas").insert(record).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return record

    def obtener_todas_facturas(self) -> List[Dict[str, Any]]:
        """
        🎓 EXPLICACIÓN SUPABASE SELECT:
        Consulta todas las filas de la tabla 'facturas' ordenadas por fecha descendente.
        """
        if not self.client:
            return []

        response = self.client.table("facturas").select("*").order("created_at", desc=True).execute()
        return response.data or []
