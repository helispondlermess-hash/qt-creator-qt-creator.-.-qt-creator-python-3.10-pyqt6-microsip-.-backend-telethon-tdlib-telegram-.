# -*- coding: utf-8 -*-
"""
Telegram Caller - десктопное приложение для звонков через Telegram
"""

__version__ = "1.0.0"
__author__ = "Telegram Caller Team"

from .core.telegram_client import TelegramClient
from .gui.main_window import MainWindow

__all__ = ['TelegramClient', 'MainWindow']