# Dockerfile multi-stage para FastAPI Backend

FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema requeridas para Pillow (imagen a PDF)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar requerimientos de Python
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del backend
COPY backend/ /app/backend/

WORKDIR /app/backend

EXPOSE 8000

# Ejecutar FastAPI escuchando en todas las interfaces del contenedor (o Tailscale)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
