from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class FacturaExtraidaData(BaseModel):
    """
    Modelo Pydantic para castear y validar los datos JSON 
    retornados por la IA (Gemini 1.5 Flash).
    
    OWASP MEDIDA 2 (LLM Injection & Data Validation):
    Casteo estricto de tipos para prevenir inyección de caracteres 
    maliciosos o inconsistencia en la base de datos.
    """
    emisor: str = Field(..., description="Nombre o razón social del emisor de la factura")
    nit: Optional[str] = Field(None, description="Número de Identificación Tributaria o RFC/RUT")
    fecha: str = Field(..., description="Fecha de la factura en formato YYYY-MM-DD")
    monto_total: float = Field(..., description="Monto total cobrado en la factura")
    impuestos: float = Field(0.0, description="Monto total de impuestos (IVA, Sales Tax)")
    moneda: str = Field("COP", description="Código de la moneda (ej. COP, USD, EUR)")
    categoria: Optional[str] = Field("General", description="Categoría asignada al gasto (ej. Alimentación, Transporte)")

class FacturaResponse(BaseModel):
    """
    Modelo de respuesta devuelto por la API al cliente frontend.
    """
    id: str
    emisor: str
    nit: Optional[str]
    fecha: str
    monto_total: float
    impuestos: float
    moneda: str
    categoria: Optional[str]
    pdf_url: str
    created_at: Optional[str] = None
