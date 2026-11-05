@echo off
title VoxGravity Push-to-Talk Terminal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [VoxGravity] Ambiente virtual .venv nao encontrado!
    echo Execute install.bat primeiro.
    pause
    exit /b 1
)

echo Iniciando VoxGravity Terminal Daemon...
".venv\Scripts\python.exe" push_to_talk.py
pause
