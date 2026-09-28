@echo off
chcp 65001 >nul
title Compilar Front-end (Build de Produção)
echo ========================================================
echo   Compilando Front-end Vue 3 / Vite para producao...
echo ========================================================
echo.
cd /d "%~dp0\.."
call npm run build
if %errorlevel% equ 0 (
    echo.
    echo [SUCESSO] Front-end compilado com sucesso na pasta dist!
) else (
    echo.
    echo [ERRO] Ocorreu uma falha na compilacao do front-end.
)
echo.
pause
