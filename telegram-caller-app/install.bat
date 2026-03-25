@echo off
chcp 65001 >nul
title Telegram Caller - Установщик
echo.
echo ========================================
echo     Telegram Caller v1.0.0 - Установщик
echo ========================================
echo.
echo Выберите версию для установки:
echo.
echo  [1] Веб-версия (Next.js)
echo      - Требует Node.js
echo      - Запускается в браузере
echo      - http://localhost:3000
echo.
echo  [2] Десктоп приложение (PyQt6)
echo      - Требует Python + зависимости
echo      - Запускается как .exe файл
echo.
echo  [0] Выход
echo.
set /p choice=Ваш выбор: 

if "%choice%"=="1" goto web
if "%choice%"=="2" goto desktop
if "%choice%"=="0" exit
goto start

:web
echo.
echo === Установка веб-версии ===
echo.
echo Проверка Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ОШИБКА: Node.js не установлен!
    echo Скачайте с https://nodejs.org
    pause
    exit /b 1
)
echo Node.js найден
echo.
echo Установка зависимостей...
call npm install
echo.
echo Сборка приложения...
call npm run build
echo.
echo Запуск сервера...
echo.
echo Откройте в браузере: http://localhost:3000
echo.
call npm run start
goto end

:desktop
echo.
echo === Установка десктоп версии ===
echo.
echo Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ОШИБКА: Python не установлен!
    echo Скачайте с https://python.org
    pause
    exit /b 1
)
echo Python найден
echo.
echo Установка зависимостей...
pip install -r requirements.txt
echo.
echo Сборка EXE (PyInstaller)...
pyinstaller specs\telegram_caller.spec --clean
echo.
if exist "dist\TelegramCaller.exe" (
    echo Успешно! EXE создан: dist\TelegramCaller.exe
    start "" "dist\TelegramCaller.exe"
) else (
    echo ОШИБКА при сборке
)
goto end

:end
pause
exit /b 0