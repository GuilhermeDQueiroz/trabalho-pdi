@echo off
chcp 65001 >nul
title Modo de Desenvolvimento PDI (Vite + FastAPI)
echo ========================================================
echo   Iniciando Modo de Desenvolvimento
echo   Backend: http://localhost:8000
echo   Front-end (Vite Hot-Reload): http://localhost:5173
echo ========================================================
echo.
cd /d "%~dp0\.."
start "Backend FastAPI" cmd /k "python run.py"
timeout /t 2 /nobreak >nul
start http://localhost:5173
call npm run dev
