@echo off
chcp 65001 >nul
title Sistema PDI - Processamento Digital de Imagens (Python)
echo ========================================================
echo   Iniciando Sistema de Processamento Digital de Imagens
echo   Backend: Python 3.10+ / 3.14 (Algoritmos Puros de PDI)
echo   Front-end: Tema Monocromatico (Preto, Branco e Cinza)
echo ========================================================
echo.
echo Abrindo o navegador em http://localhost:8000 ...
start http://localhost:8000
echo.
python run.py
pause
