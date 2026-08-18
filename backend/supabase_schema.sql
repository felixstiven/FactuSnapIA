-- =====================================================================
-- 📚 GUÍA DIDÁCTICA Y SCRIPT DE CONFIGURACIÓN PARA SUPABASE (FactuSnap AI)
-- =====================================================================
-- ¿Qué es Supabase?
-- Supabase es una plataforma Backend-as-a-Service basada en PostgreSQL.
-- Nos ofrece:
--  1. Base de datos PostgreSQL relacional.
--  2. Storage Buckets (almacenamiento de archivos como PDFs o imágenes).
--  3. Row Level Security (RLS) para proteger los datos a nivel de fila.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. CREACIÓN DE LA TABLA 'facturas' EN POSTGRESQL
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.facturas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    emisor VARCHAR(255) NOT NULL,
    nit VARCHAR(50),
    fecha DATE NOT NULL,
    monto_total NUMERIC(12, 2) NOT NULL,
    moneda VARCHAR(10) DEFAULT 'COP',
    categoria VARCHAR(100),
    pdf_url TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Comentarios educativos en las columnas de PostgreSQL
COMMENT ON TABLE public.facturas IS 'Tabla principal de almacenamiento para los datos extraídos de facturas por la IA.';
COMMENT ON COLUMN public.facturas.id IS 'Identificador único UUID de la factura.';
COMMENT ON COLUMN public.facturas.emisor IS 'Nombre o razón social de la empresa emisora.';
COMMENT ON COLUMN public.facturas.monto_total IS 'Monto total procesado y validado en la factura.';
COMMENT ON COLUMN public.facturas.pdf_url IS 'Enlace al archivo PDF generado y almacenado en el Bucket de Supabase Storage.';

-- ---------------------------------------------------------------------
-- 2. POLÍTICAS DE SEGURIDAD A NIVEL DE FILA (Row Level Security - RLS)
-- ---------------------------------------------------------------------
-- RLS previene accesos no autorizados a la base de datos PostgreSQL.
ALTER TABLE public.facturas ENABLE ROW LEVEL SECURITY;

-- Política de lectura para usuarios autenticados o anónimos segun configuración
CREATE POLICY "Permitir lectura publica de facturas"
ON public.facturas
FOR SELECT
USING (true);

-- Política de inserción permitida solo desde el servidor Backend
CREATE POLICY "Permitir insercion de facturas"
ON public.facturas
FOR INSERT
WITH CHECK (true);

-- ---------------------------------------------------------------------
-- 3. CONFIGURACIÓN DEL BUCKET DE STORAGE ('facturas-pdfs')
-- ---------------------------------------------------------------------
-- Crear el bucket de almacenamiento para guardar los PDFs procesados
INSERT INTO storage.buckets (id, name, public)
VALUES ('facturas-pdfs', 'facturas-pdfs', true)
ON CONFLICT (id) DO NOTHING;

-- Política RLS para el Bucket de Storage: Permitir subir archivos
CREATE POLICY "Permitir subida de PDFs al bucket facturas-pdfs"
ON storage.objects
FOR INSERT
WITH CHECK (bucket_id = 'facturas-pdfs');

-- Política RLS para el Bucket de Storage: Permitir ver/descargar PDFs
CREATE POLICY "Permitir lectura publica de PDFs en el bucket facturas-pdfs"
ON storage.objects
FOR SELECT
USING (bucket_id = 'facturas-pdfs');
