@echo off
title GearGuard - Backend Server
color 0A
cls

echo.
echo ╔════════════════════════════════════════════════╗
echo ║     GEARGUARD - BACKEND SERVER LAUNCHER       ║
echo ╚════════════════════════════════════════════════╝
echo.
echo [INFO] Starting Flask Backend...
echo.

cd /d "%~dp0backend"
python run.py

echo.
echo [ERROR] Backend server stopped or failed to start.
echo.
pause
