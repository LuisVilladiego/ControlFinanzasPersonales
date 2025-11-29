# 📥 Guía de Instalación - FINANZAS MALU

Esta guía te ayudará a instalar FINANZAS MALU en tu PC de forma permanente.

## 📋 Requisitos Previos

- **Python 3.9 o superior** (recomendado 3.11)
- **pip** (gestor de paquetes de Python)
- **Git** (opcional, para clonar el repositorio)

## 🚀 Instalación Paso a Paso

### Paso 1: Verificar Python

Abre PowerShell o CMD y verifica que Python esté instalado:

```powershell
python --version
```

Si no tienes Python, descárgalo de: https://www.python.org/downloads/

**⚠️ Importante:** Durante la instalación de Python, marca la opción "Add Python to PATH"

### Paso 2: Navegar al Directorio del Proyecto

```powershell
cd C:\xampp\htdocs\Finanzas
```

### Paso 3: Crear Entorno Virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
```

**Windows (CMD):**
```cmd
python -m venv venv
```

### Paso 4: Activar el Entorno Virtual

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

Si obtienes un error de política de ejecución, ejecuta primero:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

Verás `(venv)` al inicio de tu línea de comandos cuando esté activado.

### Paso 5: Instalar Dependencias

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### Paso 6: Configurar Variables de Entorno

1. Crea un archivo `.env` en la raíz del proyecto (copia de `.env.example` si existe)

2. Edita `.env` con un editor de texto (Notepad, VS Code, etc.):

```env
# Clave secreta (genera una nueva y segura)
SECRET_KEY=tu-clave-secreta-muy-segura-aqui-cambiar-en-produccion

# Base de datos (SQLite por defecto)
DATABASE_URL=sqlite:///finanzas.db

# Configuración de Email (opcional, para recordatorios)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-de-aplicacion
MAIL_DEFAULT_SENDER=tu-email@gmail.com

# Entorno
FLASK_ENV=development
```

**Nota sobre Gmail:**
- Necesitas generar una "Contraseña de aplicación" en tu cuenta de Google
- Ve a: Google Account → Seguridad → Verificación en 2 pasos → Contraseñas de aplicaciones

### Paso 7: Inicializar Base de Datos

```powershell
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Base de datos inicializada correctamente')"
```

### Paso 8: Ejecutar la Aplicación

```powershell
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

## 🎯 Crear Acceso Rápido

### Opción 1: Script de Inicio Rápido

Crea un archivo `iniciar.bat` en la raíz del proyecto:

```batch
@echo off
cd /d "C:\xampp\htdocs\Finanzas"
call venv\Scripts\activate.bat
python app.py
pause
```

Haz doble clic en `iniciar.bat` para iniciar la aplicación.

### Opción 2: Crear Acceso Directo en el Escritorio

1. Crea un acceso directo a `iniciar.bat`
2. Colócalo en el escritorio
3. Cambia el icono si lo deseas

## 🔧 Instalación como Servicio de Windows (Opcional)

Para que la aplicación se inicie automáticamente al encender la PC:

### Usando NSSM (Non-Sucking Service Manager)

1. Descarga NSSM: https://nssm.cc/download
2. Extrae y ejecuta desde PowerShell (como Administrador):

```powershell
# Instalar servicio
.\nssm.exe install FinanzasMalu "C:\xampp\htdocs\Finanzas\venv\Scripts\python.exe" "C:\xampp\htdocs\Finanzas\app.py"

# Configurar directorio de trabajo
.\nssm.exe set FinanzasMalu AppDirectory "C:\xampp\htdocs\Finanzas"

# Iniciar servicio
.\nssm.exe start FinanzasMalu
```

## 📝 Verificación de Instalación

1. Abre tu navegador
2. Ve a: `http://localhost:5000`
3. Deberías ver la página de inicio de sesión
4. Crea una cuenta de prueba
5. Verifica que puedas acceder al dashboard

## 🐛 Solución de Problemas

### Error: "python no se reconoce como comando"

**Solución:** Python no está en el PATH. Reinstala Python marcando "Add to PATH" o agrega manualmente Python al PATH del sistema.

### Error: "No module named 'flask'"

**Solución:** Asegúrate de que el entorno virtual esté activado y ejecuta:
```powershell
pip install -r requirements.txt
```

### Error: "Database is locked"

**Solución:** Cierra otras instancias de la aplicación o reinicia tu PC.

### Error al activar entorno virtual en PowerShell

**Solución:** Ejecuta:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### La aplicación no inicia

**Solución:** Verifica que:
1. El entorno virtual esté activado
2. Todas las dependencias estén instaladas
3. El archivo `.env` esté configurado correctamente
4. No haya otro proceso usando el puerto 5000

## 📦 Actualización de la Aplicación

Para actualizar la aplicación:

```powershell
# Activar entorno virtual
.\venv\Scripts\activate.bat

# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Reiniciar aplicación
python app.py
```

## 🔄 Desinstalación

Para desinstalar completamente:

1. Detén la aplicación (Ctrl+C)
2. Elimina el directorio del proyecto
3. Si instalaste como servicio, desinstálalo:
```powershell
.\nssm.exe stop FinanzasMalu
.\nssm.exe remove FinanzasMalu confirm
```

## ✅ Checklist de Instalación

- [ ] Python 3.9+ instalado
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] Archivo `.env` configurado
- [ ] Base de datos inicializada
- [ ] Aplicación ejecutándose
- [ ] Acceso desde navegador funcionando
- [ ] Cuenta de usuario creada

## 🎉 ¡Instalación Completada!

Una vez completados todos los pasos, tu aplicación FINANZAS MALU estará lista para usar.

**Acceso:** http://localhost:5000

---

**¿Necesitas ayuda?** Revisa la sección de solución de problemas o consulta la documentación completa en `README.md`.


