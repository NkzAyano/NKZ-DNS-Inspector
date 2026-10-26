
@echo off
title NKZ DNS Inspector - Build
cd /d "%~dp0"

echo ========================================
echo       NKZ DNS INSPECTOR
echo       COMPILADOR EXE
echo ========================================
echo.

where py >nul 2>nul
if errorlevel 1 (
    echo Python nao encontrado.
    echo Instale em https://www.python.org/downloads/
    echo Marque Add Python to PATH.
    pause
    exit /b 1
)

echo Instalando dependencias...
py -m pip install -r requirements.txt

if errorlevel 1 (
    echo Erro ao instalar dependencias.
    pause
    exit /b 1
)

echo.
echo Compilando executavel...

py -m PyInstaller --noconfirm --clean --onefile --windowed --name NKZ_DNS_Inspector --collect-all dns main.py

if errorlevel 1 (
    echo Erro ao compilar.
    pause
    exit /b 1
)

echo.
echo Compilacao concluida!
echo Arquivo: dist\NKZ_DNS_Inspector.exe
echo.

pause
