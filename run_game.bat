@echo off
echo ==========================================
echo      The Green Guardian - Launcher
echo ==========================================
echo 1. Play Game (Manual)
echo 2. Watch AI Agent
echo 3. Train AI Agent
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    C:\Python311\python.exe src/play.py
) else if "%choice%"=="2" (
    C:\Python311\python.exe src/watch.py
) else if "%choice%"=="3" (
    C:\Python311\python.exe src/train.py
) else (
    echo Invalid choice
)
pause
