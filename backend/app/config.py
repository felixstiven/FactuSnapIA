import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Settings:
    """
    Configuración global de la aplicación.
    Centraliza las llaves de seguridad y URLs.
    OWASP MEDIDA 3: La GEMINI_API_KEY y credenciales críticas viven 
    exclusivamente en el servidor y nunca se envían al cliente frontend.
    """
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_STORAGE_BUCKET: str = os.getenv("SUPABASE_STORAGE_BUCKET", "facturas-pdfs")
    
    TAILSCALE_IP: str = os.getenv("TAILSCALE_IP", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

settings = Settings()
