@echo off
REM MountainRiverEchoes WebUI - Windows launcher
REM Double-click this file to start the local web UI.
REM It auto-detects the venv in the repo root; no hardcoded paths.

chcp 65001 >nul
cd /d "%~dp0"

set "PY=python"
if exist "%~dp0venv\Scripts\python.exe" set "PY=%~dp0venv\Scripts\python.exe"

echo.
echo   MountainRiverEchoes (Shanhe Huixiang) WebUI
echo   ------------------------------------------
echo   Interpreter: %PY%
echo   URL:         http://127.0.0.1:8766
echo   Press Ctrl+C in this window to stop the server.
echo.

"%PY%" webui\mountainriverechoes.py

echo.
echo   Server stopped.
pause
