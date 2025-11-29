@echo off
echo ========================================
echo    FINANZAS MALU - Instalador
echo ========================================
echo.

cd /d "%~dp0"

echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH.
    echo Por favor, instala Python 3.9 o superior desde python.org
    pause
    exit /b 1
)
python --version
echo.

echo [2/5] Creando entorno virtual...
if exist "venv" (
    echo El entorno virtual ya existe. Omitiendo creacion...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
    echo Entorno virtual creado correctamente.
)
echo.

echo [3/5] Activando entorno virtual...
call venv\Scripts\activate.bat
echo.

echo [4/5] Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias.
    pause
    exit /b 1
)
echo Dependencias instaladas correctamente.
echo.

echo [5/5] Inicializando base de datos...
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Base de datos inicializada correctamente')"
if errorlevel 1 (
    echo ADVERTENCIA: Hubo un problema al inicializar la base de datos.
    echo Puede que ya este inicializada o haya un error.
)
echo.

echo ========================================
echo    Instalacion completada!
echo ========================================
echo.
echo Para iniciar la aplicacion, ejecuta: iniciar.bat
echo O ejecuta manualmente: python app.py
echo.
echo La aplicacion estara disponible en: http://localhost:5000
echo.
pause


