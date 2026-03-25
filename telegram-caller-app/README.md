# Telegram Caller

Десктопное приложение для звонков через Telegram с современным тёмным дизайном.

## Возможности

- **Авторизация**: Вход по номеру телефона с поддержкой 2FA
- **Звонки**: Голосовые звонки на номера и @username
- **Управление аудио**: Выбор микрофона и динамиков, mute
- **Видео**: Заглушка для включения камеры (OpenCV)
- **Контакты**: Загрузка и поиск контактов из Telegram
- **Тёмная тема**: Современный дизайн в сине-фиолетовых тонах

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

## Сборка в EXE (Windows)

```bash
pyinstaller specs/telegram_caller.spec
```

Итоговый EXE будет в папке `dist/TelegramCaller/`

## Зависимости

- PyQt6 >= 6.5.0
- telethon >= 1.28.0
- sounddevice >= 0.4.6
- opencv-python >= 4.8.0
- numpy >= 1.24.0
- pyinstaller >= 6.0.0

## API Telegram

Используются предоставленные учетные данные:
- api_id: 31818704
- api_hash: 2e12474990ebaa58d90323e14a403c8f

## Структура проекта

```
telegram-caller-app/
├── main.py                 # Точка входа
├── requirements.txt        # Зависимости
├── version.txt             # Информация о версии
├── src/
│   ├── config.py           # Конфигурация
│   ├── gui/
│   │   ├── styles.py       # Стили (тёмная тема)
│   │   └── main_window.py  # Главное окно
│   ├── core/
│   │   ├── telegram_client.py  # Telegram API
│   │   ├── call_manager.py     # Управление звонками
│   │   └── audio_manager.py    # Аудио/видео
│   └── utils/
│       ├── logger.py       # Логирование
│       └── validators.py   # Валидаторы
└── specs/
    └── telegram_caller.spec # Спецификация PyInstaller
```

## Требования

- Python 3.10+
- Windows/Linux/Mac
- Для звонков: микрофон и колонки/наушники