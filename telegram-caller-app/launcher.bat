@echo off
chcp 65001 >nul
title Telegram Caller - Загрузка
echo.
echo ======================================
echo       Telegram Caller v1.0.0
echo ======================================
echo.
echo Выберите режим запуска:
echo.
echo  [1] Веб-версия (браузер)
echo  [2] Десктоп приложение (.exe)
echo  [0] Выход
echo.
set /p choice=Ваш выбор: 

if "%choice%"=="1" goto web
if "%choice%"=="2" goto desktop
if "%choice%"=="0" exit

:web
echo.
echo Запуск веб-версии...
echo Откройте http://localhost:3000 в браузере
echo.
cd /d "%~dp0"
start "" "http://localhost:3000"
npm run dev
goto end

:desktop
echo.
echo Запуск десктоп приложения...
if exist "dist\TelegramCaller.exe" (
    start "" "dist\TelegramCaller.exe"
) else (
    echo Ошибка: TelegramCaller.exe не найден!
    echo Сначала выполните сборку: pyinstaller telegram_caller.spec
    pause
)
goto end

:end
pause