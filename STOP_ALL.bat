@echo off
title GearGuard - Stop All Servers
color 0C
cls

echo.
echo ╔════════════════════════════════════════════════╗
echo ║         STOPPING GEARGUARD SERVERS...         ║
echo ╚════════════════════════════════════════════════╝
echo.

echo [INFO] Stopping Flask Backend (Python)...
taskkill /F /FI "WINDOWTITLE eq GearGuard Backend*" >nul 2>&1
taskkill /F /FI "IMAGENAME eq python.exe" /FI "MEMUSAGE gt 10000" >nul 2>&1

echo [INFO] Stopping React Frontend (Node)...
taskkill /F /FI "WINDOWTITLE eq GearGuard Frontend*" >nul 2>&1
taskkill /F /FI "IMAGENAME eq node.exe" /FI "MEMUSAGE gt 10000" >nul 2>&1

echo.
echo ╔════════════════════════════════════════════════╗
echo ║           ALL SERVERS STOPPED!                 ║
echo ╚════════════════════════════════════════════════╝
echo.
echo   Press any key to exit...
pause >nul
