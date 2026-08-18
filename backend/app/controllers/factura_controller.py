"""
=============================================================================
📚 CONTROLADOR DE FACTURAS (Factura Controller)
=============================================================================
CAPA DE ARQUITECTURA LIMPIA: CONTROLLER
-----------------------------------------------------------------------------
Valida los aspectos técnicos de la petición HTTP (seguridad MIME y tamaño payload),
y delega la lógica de negocio al Servicio.

PROTECCIÓN OWASP MEDIDA 1 (Unrestricted File Upload):
 1. Valida que el MIME Type sea estrictamente 'image/jpeg' o 'image/png'.
 2. Valida que el tamaño máximo del archivo no exceda los 10 MB (10 * 1024 * 1024 bytes).
=============================================================================
"""

from fastapi import UploadFile, HTTPException, status
from app.services.factura_service import FacturaService

# Constante de seguridad OWASP
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/jpg"]

class FacturaController:
    def __init__(self):
        self.service = FacturaService()

    async def procesar_subida_factura(self, file: UploadFile):
        # 1. Validación OWASP: MIME Type
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de archivo no permitido: {file.content_type}. Solo se admiten imágenes JPG y PNG."
            )

        # Leer contenido de bytes
        contents = await file.read()

        # 2. Validación OWASP: Tamaño Payload Max 10 MB
        if len(contents) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="El archivo excede el tamaño máximo permitido de 10 MB."
            )

        # Delegar al servicio de negocio
        resultado = self.service.procesar_y_guardar_factura(contents)
        return resultado

    def obtener_lista_facturas(self):
        return self.service.listar_facturas()
