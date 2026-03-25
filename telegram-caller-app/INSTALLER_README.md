# Telegram Caller - Installer

## Описание

Универсальный установщик с выбором между веб-версией и десктопным приложением.

## Использование

### Способ 1: Через Python (с PyQt6)
```bash
pip install PyQt6
python installer.py
```

### Способ 2: Через EXE (скомпилированный)
```
TelegramCallerInstaller.exe
```

### Способ 3: Через BAT скрипт
```cmd
install.bat
```

## Сборка EXE

```cmd
pip install pyinstaller
pyinstaller specs/installer.spec --clean
```

## Файлы

- `installer.py` - Python установщик с GUI
- `installer.html` - HTML установщик для браузера
- `install.bat` - BAT скрипт установщика
- `launcher.bat` - BAT скрипт запуска
- `specs/installer.spec` - Спецификация PyInstaller