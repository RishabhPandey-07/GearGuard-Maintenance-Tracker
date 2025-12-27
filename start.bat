@echo off
echo ========================================
echo   GearGuard - Starting Servers
echo ========================================
echo.

echo [1/2] Starting Flask Backend (Port 5000)...
cd /d "%~dp0backend"
start "Flask Backend" cmd /k "python run.py"
timeout /t 3 /nobreak >nul

echo [2/2] Starting React Frontend (Port 3000)...
cd /d "%~dp0frontend"
start "React Frontend" cmd /k "npm run dev"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   Servers Started Successfully!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Press any key to open the application...
pause >nul

start http://localhost:3000

echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
pause
