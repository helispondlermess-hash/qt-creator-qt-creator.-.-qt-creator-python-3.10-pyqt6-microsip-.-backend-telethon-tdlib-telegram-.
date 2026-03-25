# -*- coding: utf-8 -*-
"""
Точка входа в приложение Telegram Caller
"""

import sys
import os

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt

from src.gui.main_window import MainWindow
from src.utils.logger import logger


def check_dll_dependencies() -> bool:
    """
    Проверка наличия необходимых DLL и библиотек
    
    Returns:
        True если все зависимости найдены
    """
    required_files = []
    
    if sys.platform == "win32":
        required_files = [
            "python3.dll",
            "vcruntime140.dll",
        ]
    
    missing = []
    for f in required_files:
        if not any(os.path.exists(os.path.join(p, f)) for p in sys.path):
            missing.append(f)
    
    if missing:
        logger.warning(f"Отсутствуют файлы: {missing}")
    
    return True


def main():
    """Запуск приложения"""
    logger.info("Запуск Telegram Caller...")
    
    if not check_dll_dependencies():
        QMessageBox.critical(
            None,
            "Ошибка",
            "Отсутствуют необходимые системные библиотеки. "
            "Пожалуйста, установите Visual C++ Redistributable."
        )
        return 1
    
    app = QApplication(sys.argv)
    app.setApplicationName("Telegram Caller")
    app.setApplicationVersion("1.0.0")
    app.setDesktopFileName("telegram-caller")
    
    window = MainWindow()
    window.show()
    
    logger.info("Приложение запущено")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())