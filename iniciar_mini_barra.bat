@echo off
title VoxGravity Voice Bar
cd /d "%~dp0"

if not exist ".venv\Scripts\pythonw.exe" (
    echo [VoxGravity] Ambiente virtual .venv nao encontrado!
    echo Execute install.bat primeiro.
    pause
    exit /b 1
)

echo Iniciando VoxGravity Voice Bar em segundo plano...
start "" ".venv\Scripts\pythonw.exe" mini_barra.py
exit
