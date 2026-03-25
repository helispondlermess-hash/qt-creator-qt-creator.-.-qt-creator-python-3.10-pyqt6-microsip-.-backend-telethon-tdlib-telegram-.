# -*- coding: utf-8 -*-
"""
Утилита для логирования событий приложения
"""

import logging
import os
from datetime import datetime
from pathlib import Path


class Logger:
    """Класс для управления логированием в приложении"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._setup_logger()
    
    def _setup_logger(self):
        """Настройка логгера"""
        self.logger = logging.getLogger('TelegramCaller')
        self.logger.setLevel(logging.DEBUG)
        
        log_dir = Path.home() / '.telegram_caller' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f'app_{datetime.now().strftime("%Y%m%d")}.log'
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str):
        """Логирование отладочных сообщений"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Логирование информационных сообщений"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Логирование предупреждений"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Логирование ошибок"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Логирование критических ошибок"""
        self.logger.critical(message)
    
    def exception(self, message: str):
        """Логирование исключений с трассировкой"""
        self.logger.exception(message)


logger = Logger()