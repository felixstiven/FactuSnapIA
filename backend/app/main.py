"""
=============================================================================
🚀 FACTUSNAP AI - APLICACIÓN PRINCIPAL (FastAPI)
=============================================================================
PUNTO DE ENTRADA DEL BACKEND
-----------------------------------------------------------------------------
Configura el servidor FastAPI, los middlewares de CORS y las rutas.

PROTECCIÓN OWASP MEDIDA 4 (Seguridad en Red Privada / Tailscale):
FastAPI se ejecuta en la IP privada de Tailscale para asegurar que todo 
el tráfico pase por un túnel cifrado WireGuard.
=============================================================================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import factura_router
from app.config import settings

app = FastAPI(
    title="FactuSnap AI Backend",
    description="API para escaneo, OCR con Gemini 1.5 Flash y almacenamiento de facturas en Supabase.",
    version="1.0.0"
)

# Configuración de CORS para desarrollo y consumo desde el frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción restringir a la IP o dominio del Frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas del módulo de facturas
app.include_router(factura_router.router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "app": "FactuSnap AI API",
        "tailscale_ip": settings.TAILSCALE_IP,
        "environment": settings.ENVIRONMENT
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
