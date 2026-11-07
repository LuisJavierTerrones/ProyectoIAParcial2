@echo off
title LogiSmart AI - Interfaz grafica
cd /d "%~dp0"
echo ==========================================
echo          LOGISMART AI - INICIO
echo ==========================================
echo.
python -m streamlit run app.py
if errorlevel 1 (
  echo.
  echo No se pudo iniciar la interfaz.
  echo Verifica Python y ejecuta: python -m pip install -r requirements.txt
  pause
)
