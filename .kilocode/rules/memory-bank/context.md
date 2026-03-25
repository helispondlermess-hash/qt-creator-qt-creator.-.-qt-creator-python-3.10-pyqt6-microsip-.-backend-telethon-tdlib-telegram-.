# Active Context: Telegram Caller App

## Current State

**Project Status**: ✅ Готов к использованию

Проект включает:
- Веб-версия на Next.js (localhost:3000)
- Десктоп приложение на PyQt6 (требует сборки через PyInstaller)
- Установщик с выбором версии

## Recently Completed

- [x] Исправлена ошибка AA_EnableHighDpiScaling в main.py
- [x] Создана веб-версия интерфейса на Next.js
- [x] Создан API эндпоинт /api/status
- [x] Создан установщик (installer.html, install.bat)
- [x] Создан лаунчер (launcher.bat)
- [x] Обновлена спецификация PyInstaller

## Структура проекта

| Директория/Файл | Назначение | Статус |
|-----------------|------------|--------|
| `telegram-caller-app/main.py` | Десктоп приложение (PyQt6) | ✅ Готов |
| `telegram-caller-app/requirements.txt` | Зависимости Python | ✅ Обновлено |
| `telegram-caller-app/specs/telegram_caller.spec` | PyInstaller спецификация | ✅ Готов |
| `telegram-caller-app/install.bat` | Установщик Windows | ✅ Создан |
| `telegram-caller-app/launcher.bat` | Лаунчер | ✅ Создан |
| `telegram-caller-app/installer.html` | HTML установщик | ✅ Создан |
| `src/app/page.tsx` | Веб-интерфейс | ✅ Готов |
| `src/app/api/status/route.ts` | API статус | ✅ Готов |

## Запуск

### Веб-версия:
```bash
npm run dev
# Открыть http://localhost:3000
```

### Десктоп приложение (на Windows):
```cmd
cd telegram-caller-app
pip install -r requirements.txt
pyinstaller specs\telegram_caller.spec --clean
dist\TelegramCaller.exe
```

### Установщик:
```cmd
cd telegram-caller-app
install.bat
```

## Технологический стек

- **Веб**: Next.js 16, React 19, TypeScript, Tailwind CSS 4
- **Десктоп**: PyQt6, Telethon, sounddevice, opencv-python
- **Сборка**: PyInstaller, npm build

## Сессия

| Дата | Изменения |
|------|-----------|
| 2026-03-25 | Исправлены ошибки, созданы веб и десктоп версии, установщик |
| 2026-03-25 | Создан релиз v1.0.0 на GitHub |