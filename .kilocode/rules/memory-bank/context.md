# Active Context: Telegram Caller App

## Current State

**Project Status**: ✅ Готов к использованию (v2.0.0)

Проект включает:
- Веб-версия на Next.js (localhost:3000)
- Backend API на Python (localhost:8080) с Telethon
- Авторизация через Telegram по номеру телефона и коду

## Recently Completed

- [x] Создан backend сервер на Python (server.py) с Telethon
- [x] Реализована авторизация по номеру телефона через Telegram API
- [x] Создан UI для входа/регистрации с вводом API_ID, API_HASH, номера
- [x] Добавлена верификация кода из Telegram
- [x] Реализовано получение контактов после авторизации
- [x] Добавлен скрипт запуска (start.bat)

## Структура проекта

| Директория/Файл | Назначение | Статус |
|-----------------|------------|--------|
| `telegram-caller-app/server.py` | Backend API (aiohttp + Telethon) | ✅ Готов |
| `telegram-caller-app/requirements.txt` | Зависимости Python | ✅ Обновлено |
| `telegram-caller-app/start.bat` | Скрипт запуска | ✅ Создан |
| `src/app/page.tsx` | UI авторизации и контакты | ✅ Готов |
| `src/app/api/status/route.ts` | Proxy к backend | ✅ Готов |

## Запуск

### Полный запуск (Frontend + Backend):
```cmd
cd telegram-caller-app
start.bat
# Выбрать пункт 1
```

### Или вручную:
```bash
# Терминал 1: Backend
python telegram-caller-app/server.py

# Терминал 2: Frontend  
npm run dev
```

### Использование:
1. Открыть http://localhost:3000
2. Ввести API_ID и API_HASH (получить на my.telegram.org)
3. Ввести номер телефона (+79991234567)
4. Нажать "Получить код" - код придет в Telegram
5. Ввести код из Telegram
6. После входа отобразятся контакты

## Технологический стек

- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS 4
- **Backend**: Python, aiohttp, Telethon
- **Auth**: Telegram API (TD-Lib через Telethon)

## Сессия

| Дата | Изменения |
|------|-----------|
| 2026-03-25 | Исправлены ошибки, созданы веб и десктоп версии |
| 2026-03-25 | Создан релиз v1.0.0 на GitHub |
| 2026-03-25 | Добавлена авторизация по номеру через Telegram (v2.0.0) |