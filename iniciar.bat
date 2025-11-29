@echo off
echo ========================================
echo    FINANZAS MALU - Iniciando...
echo ========================================
echo.

cd /d "%~dp0"

REM Verificar si existe el entorno virtual
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Entorno virtual no encontrado.
    echo Por favor, ejecuta primero: python -m venv venv
    pause
    exit /b 1
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Verificar si existe app.py
if not exist "app.py" (
    echo ERROR: app.py no encontrado.
    echo Asegurate de estar en el directorio correcto.
    pause
    exit /b 1
)

REM Verificar si existe .env
if not exist ".env" (
    echo ADVERTENCIA: Archivo .env no encontrado.
    echo La aplicacion usara valores por defecto.
    echo.
)

echo Iniciando servidor Flask...
echo.
echo La aplicacion estara disponible en: http://localhost:5000
echo.
echo Presiona Ctrl+C para detener el servidor.
echo.

REM Iniciar aplicación
python app.py

pause


