@echo off
chcp 65001 >nul
title Executar Testes Unitarios PDI (Python)
echo ========================================================
echo   Executando Suíte de Testes Unitários dos Algoritmos PDI
echo ========================================================
echo.
cd /d "%~dp0\.."
python -m unittest backend/tests/test_pdi.py
echo.
pause
