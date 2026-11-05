@echo off
setlocal enabledelayedexpansion
title VoxGravity - Instalador de Ambiente e Dependencias
cd /d "%~dp0"

echo ======================================================================
echo           VOXGRAVITY - INSTALADOR AUTOMATIZADO
echo ======================================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERRO] Python nao foi encontrado no PATH do sistema.
    echo Por favor, instale o Python 3.10 ou superior antes de prosseguir.
    pause
    exit /b 1
)

if not exist ".venv" (
    echo [1/3] Criando ambiente virtual isolado (.venv)...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERRO] Falha ao criar o ambiente virtual .venv.
        pause
        exit /b 1
    )
) else (
    echo [1/3] Ambiente virtual .venv ja existe.
)

echo [2/3] Atualizando gerenciador pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet

echo [3/3] Instalando dependencias do projeto...
".venv\Scripts\python.exe" -m pip install -r requirements.txt --quiet
".venv\Scripts\python.exe" -m pip install -e . --quiet

echo.
echo ======================================================================
echo    INSTALACAO CONCLUIDA COM SUCESSO!
echo    - Para abrir a mini-barra flutuante: execute iniciar_mini_barra.bat
echo    - Para usar pelo terminal: execute iniciar_push_to_talk.bat
echo ======================================================================
echo.
pause
