# 🚀 PROMPT DE INICIALIZACIÓN: FactuSnap AI (MVP Seguro & Clean Architecture)

Actúa como un **Arquitecto de Software Full Stack Senior & Especialista en Ciberseguridad (FastAPI, React PWA, Supabase, Tailscale)**.

Tu objetivo es inicializar el código base para la aplicación **FactuSnap AI** siguiendo el patrón de arquitectura limpia **Router - Controller - Service - Repository - Model** en el backend, y **Context API + Separación de Componentes Presentacionales** en el frontend. Para el frontend, utiliza **pnpm** como gestor de paquetes e inicializa el proyecto React + TypeScript con Vite (`react-ts`) siguiendo los estándares de la industria.

---

## 📚 1. GUÍA DE APRENDIZAJE Y FLUJO DE COMUNICACIÓN

Para fines pedagógicos y de aprendizaje profundo de **Supabase**, el proyecto debe incluir:

1. **Documentación y Guía Didáctica de Supabase:** Explicaciones claras sobre cómo funciona Supabase (PostgreSQL, Storage Buckets, Row Level Security - RLS, y el cliente SDK de Supabase). Se incluirán scripts SQL explicados paso a paso para la creación de tablas, índices y políticas de seguridad en el Bucket de Storage.
2. **Flujo de Comunicación entre Capas:**
   * **Frontend (React + TypeScript):** La cámara captura la imagen y la limpia en un `<canvas>` $\rightarrow$ Invoca el `FacturaContext` $\rightarrow$ El contexto llama al `apiClient.ts` $\rightarrow$ Se envía un `FormData` por HTTP POST a la **IP de Tailscale**.
   * **Backend (FastAPI):**
     * **Router:** Recibe la petición HTTP POST y la redirige al **Controlador**.
     * **Controlador:** Valida la seguridad del archivo (MIME/tamaño) y llama al **Servicio**.
     * **Servicio:** Contiene la lógica de negocio: envía la imagen a Gemini 1.5 Flash para OCR/JSON, convierte la imagen procesada a PDF con `Pillow`, y llama al **Repositorio**.
     * **Repositorio (Supabase):** Interactúa con **Supabase SDK** (guarda el registro en la base de datos PostgreSQL de Supabase y el archivo PDF en el Bucket de Storage). Incluye comentarios didácticos detallando cada método.
     * **Modelo (Pydantic):** Garantiza que los tipos de datos (fecha, monto float, moneda) sean válidos.

---

## 🛡️ 2. AMENAZAS DE SEGURIDAD Y MEDIDAS DE PROTECCIÓN (OWASP)

Implementa de forma nativa las siguientes protecciones en el código:

1. **Prevención de Inyección de Archivos Maliciosos (Unrestricted File Upload):**
   * Validar que el archivo sea estrictamente `image/jpeg` o `image/png`.
   * Límite de tamaño máximo del payload: 10 MB.
   * La imagen debe re-procesarse con `Pillow` antes de guardarse para destruir metadatos o scripts binarios incrustados.
2. **Prompts e Inyección en IA (LLM Injection):**
   * Usar respuestas estructuradas en Gemini (JSON Schema) y castear explícitamente los tipos con Pydantic.
3. **Fuga de Credenciales (API Keys):**
   * La `GEMINI_API_KEY` vive **exclusivamente** en el servidor backend dentro de variables de entorno (`.env`). Nunca se expone a React.
4. **Seguridad en Red Privada (Tailscale):**
   * El puerto de FastAPI (8000) solo escucha en la interfaz privada expuesta por la IP de Tailscale, utilizando el cifrado de WireGuard.
5. **Políticas de Storage (Supabase):**
   * Aplicar políticas en Supabase para evitar accesos públicos no autorizados.

---

## 🌿 4. ESTRATEGIA Y FLUJO DE TRABAJO CON GIT (GIT FLOW)

El proyecto utilizará la siguiente convención de ramas:
* `main`: Código en producción, estable y desplegable.
* `dev`: Rama de desarrollo principal donde se integran las funcionalidades probadas.
* `feature/<nombre-funcionalidad>`: Ramas de características para el trabajo de nuevos módulos o refactorizaciones.

---

## 🗂️ 5. ESTRUCTURA DE ARCHIVOS (CLEAN ARCHITECTURE)

Genera exactamente esta jerarquía de archivos:

```text
factusnap-ai/
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── .gitignore
├── PROMPT_INICIAL.md
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   └── factura_router.py
│   │   ├── controllers/
│   │   │   ├── __init__.py
│   │   │   └── factura_controller.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── factura_service.py
│   │   │   ├── ai_service.py
│   │   │   └── pdf_service.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   └── factura_repository.py
│   │   └── models/
│   │       ├── __init__.py
│   │       └── factura_model.py
│   └── requirements.txt
└── frontend/
    ├── package.json
    ├── tsconfig.json
    ├── vite.config.ts
    ├── index.html
    └── src/
        ├── App.tsx
        ├── main.tsx
        ├── context/
        │   └── FacturaContext.tsx
        ├── services/
        │   └── apiClient.ts
        ├── components/
        │   ├── Header.tsx
        │   ├── CameraScanner.tsx
        │   ├── FacturaList.tsx
        │   ├── FacturaCard.tsx
        │   └── ShareBar.tsx
        └── utils/
            └── canvasFilter.ts
```

## 🔄 Historial de Mejoras y Cambios Implementados (Agosto 2026)

Durante el desarrollo y pruebas de la aplicación, se realizaron las siguientes integraciones y ajustes sobre las instrucciones originales:

1. **Recorte Inteligente del PDF (`pdf_service.py`)**:
   - Se reemplazó el filtro básico por un algoritmo de conteo de píxeles basado en `numpy` (`np.sum` y `np.argmax`), el cual analiza filas y columnas para detectar con precisión el área de la hoja blanca y eliminar completamente el fondo (ej. la silla del carro), dejando el PDF final perfectamente limpio.
2. **Actualización de IA a `gemini-flash-latest` (`ai_service.py`)**:
   - El modelo originalmente sugerido (`gemini-1.5-flash`) ya no está disponible, por lo que la aplicación ahora se conecta al endpoint dinámico `gemini-flash-latest` para garantizar la conexión.
3. **Nomenclatura del Archivo PDF**:
   - En lugar de usar un UUID aleatorio, los PDFs guardados en Supabase Storage ahora se nombran según la convención de los datos extraídos: `[Emisor]_[Fecha]_[Monto]USD.pdf` (ej. `Patacon_Pisao_Restaurant_2025-04-22_35.28USD.pdf`).
4. **Extracción de Impuestos (IVA/Taxes)**:
   - Se actualizó el modelo de base de datos (`factura_model.py`), la tarjeta del frontend (`FacturaCard.tsx`), y las instrucciones de IA para identificar de manera independiente el renglón de impuestos (ej. Sales Tax, IVA) y mostrarlo de forma desagregada del total de la factura.
5. **Corrección de Errores de Windows**:
   - Se eliminaron los Emojis de los `print()` en el servidor Uvicorn para prevenir bloqueos por `UnicodeEncodeError` en la consola de Windows PowerShell.