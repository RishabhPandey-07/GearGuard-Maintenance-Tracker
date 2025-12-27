@echo off
title GearGuard - Frontend Server
color 0B
cls

echo.
echo ╔════════════════════════════════════════════════╗
echo ║    GEARGUARD - FRONTEND SERVER LAUNCHER       ║
echo ╚════════════════════════════════════════════════╝
echo.
echo [INFO] Starting React Frontend...
echo.

cd /d "%~dp0frontend"
npm run dev

echo.
echo [ERROR] Frontend server stopped or failed to start.
echo.
pause
