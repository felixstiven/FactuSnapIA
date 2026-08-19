# 🚀 GUÍA DE EJECUCIÓN DEL BACKEND Y FRONTEND (FactuSnap AI)

Esta guía explica paso a paso cómo crear el entorno virtual (`venv`), activar las dependencias y ejecutar tanto el Backend como el Frontend de **FactuSnap AI**.

---

## 🐍 1. GUÍA DEL BACKEND (FastAPI + Python venv)

### Paso 1: Abrir la terminal y navegar al Backend
```bash
cd backend
```

### Paso 2: Crear el Entorno Virtual (`venv`)
*Ejecutar solo la primera vez para crear la carpeta virtual:*
```bash
python -m venv venv
```

### Paso 3: Activar el Entorno Virtual
Dependiendo de tu sistema operativo / consola en Windows:

#### En Windows (PowerShell - Recomendado):
```powershell
.\venv\Scripts\Activate.ps1
```

#### En Windows (CMD - Símbolo del Sistema):
```cmd
.\venv\Scripts\activate.bat
```

#### En Linux / macOS / Git Bash:
```bash
source venv/bin/activate
```

> **Nota:** Cuando el entorno virtual esté activo, verás el prefijo `(venv)` al inicio de la línea de comandos en tu terminal.

### Paso 4: Instalar las dependencias (solo si es necesario)
```bash
pip install -r requirements.txt
```

### Paso 5: Ejecutar el Servidor FastAPI
```bash
python -m uvicorn app.main:app --reload --port 8000
```
> Servidor disponible en: `http://localhost:8000`

---

## ⚡ 2. GUÍA DEL FRONTEND (React + TypeScript con pnpm)

Abrir una **segunda terminal** independiente:

### Paso 1: Navegar a la carpeta Frontend
```bash
cd frontend
```

### Paso 2: Ejecutar el Servidor de Desarrollo
```bash
pnpm dev
```
> Aplicación disponible en: `http://localhost:5173`

---

## 🛠️ RESOLUCIÓN DE PROBLEMAS COMUNES EN WINDOWS

Si PowerShell te muestra un error como: `la ejecución de scripts está deshabilitada en este sistema` al activar el `venv`, ejecuta una sola vez este comando en PowerShell como Administrador:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Y luego vuelve a activar con `.\venv\Scripts\Activate.ps1`.
