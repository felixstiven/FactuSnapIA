"""
=============================================================================
📚 ENTRADA HTTP / RUTAS DE FACTURACIÓN (Factura Router)
=============================================================================
CAPA DE ARQUITECTURA LIMPIA: ROUTER
-----------------------------------------------------------------------------
Expone los endpoints HTTP. Su única responsabilidad es mapear las URL y verbos 
HTTP (POST, GET) hacia los métodos del Controlador correspondiente.
=============================================================================
"""

from fastapi import APIRouter, UploadFile, File, status
from app.controllers.factura_controller import FacturaController

router = APIRouter(prefix="/api/facturas", tags=["Facturas"])
controller = FacturaController()

@router.post("/scan", status_code=status.HTTP_201_CREATED)
async def escanear_factura(file: UploadFile = File(...)):
    """
    Endpoint POST para escanear y procesar una imagen de factura.
    Recibe un Multipart FormData con la imagen capturada.
    """
    return await controller.procesar_subida_factura(file)

@router.get("", status_code=status.HTTP_200_OK)
def listar_facturas():
    """
    Endpoint GET para listar todas las facturas procesadas.
    """
    return controller.obtener_lista_facturas()
