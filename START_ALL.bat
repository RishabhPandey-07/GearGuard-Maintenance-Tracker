@echo off
title GearGuard - Application Launcher
color 0E
cls

echo.
echo ╔════════════════════════════════════════════════╗
echo ║         GEARGUARD - FULL STACK LAUNCHER       ║
echo ╚════════════════════════════════════════════════╝
echo.

echo [1/3] Launching Backend Server (Port 5000)...
cd /d "%~dp0backend"
start "GearGuard Backend" "%~dp0START_BACKEND.bat"
timeout /t 2 /nobreak >nul

echo [2/3] Launching Frontend Server (Port 3000)...
cd /d "%~dp0frontend"
start "GearGuard Frontend" "%~dp0START_FRONTEND.bat"
timeout /t 4 /nobreak >nul

echo [3/3] Opening Application in Browser...
timeout /t 2 /nobreak >nul
start http://localhost:3000

echo.
echo ╔════════════════════════════════════════════════╗
echo ║              ALL SYSTEMS STARTED!              ║
echo ╚════════════════════════════════════════════════╝
echo.
echo   Backend:  http://localhost:5000
echo   Frontend: http://localhost:3000
echo.
echo   Both servers are running in separate windows.
echo   Close those windows to stop the servers.
echo.
echo   This launcher window will close in 5 seconds...
timeout /t 5 /nobreak >nul
