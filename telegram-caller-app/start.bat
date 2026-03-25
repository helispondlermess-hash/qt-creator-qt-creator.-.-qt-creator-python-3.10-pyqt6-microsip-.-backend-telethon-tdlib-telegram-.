@echo off
chcp 65001 >nul
title Telegram Caller - Быстрый старт
echo.
echo ╔══════════════════════════════════════════╗
echo ║        Telegram Caller - Запуск           ║
echo ╚══════════════════════════════════════════╝
echo.
echo [1] Запуск веб-сервера (Frontend + Backend)
echo [2] Только веб-интерфейс (порт 3000)
echo [3] Только backend API (порт 8080)
echo [0] Выход
echo.
set /p choice=Выберите: 

if "%choice%"=="1" goto both
if "%choice%"=="2" goto web
if "%choice%"=="3" goto backend
if "%choice%"=="0" exit

:both
echo.
echo Запуск Frontend (порт 3000) и Backend (порт 8080)...
echo.
echo Запуск backend сервера...
start "Telegram Caller Backend" cmd /c "python telegram-caller-app\server.py"
timeout /t 3 /nobreak >nul
echo.
echo Запуск frontend сервера...
start "Telegram Caller Frontend" cmd /c "npm run dev"
echo.
echo Готово!
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8080
echo.
pause
goto end

:web
echo.
echo Запуск веб-интерфейса...
start "" "npm run dev"
echo Откройте http://localhost:3000
pause
goto end

:backend
echo.
echo Запуск backend сервера...
python telegram-caller-app\server.py
goto end

:end
pause