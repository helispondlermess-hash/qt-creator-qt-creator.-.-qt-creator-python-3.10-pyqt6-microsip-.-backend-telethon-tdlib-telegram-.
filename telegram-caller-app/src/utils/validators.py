# -*- coding: utf-8 -*-
"""
Валидаторы для проверки входных данных
"""

import re


def validate_phone_number(phone: str) -> bool:
    """
    Проверка валидности номера телефона
    
    Args:
        phone: Номер телефона в любом формате
        
    Returns:
        True если номер валиден, иначе False
    """
    if not phone:
        return False
    
    digits = re.sub(r'\D', '', phone)
    
    if len(digits) < 10 or len(digits) > 15:
        return False
    
    return True


def validate_username(username: str) -> bool:
    """
    Проверка валидности username Telegram
    
    Args:
        username: Username (с @ или без)
        
    Returns:
        True если username валиден, иначе False
    """
    if not username:
        return False
    
    username = username.lstrip('@')
    
    if len(username) < 5 or len(username) > 32:
        return False
    
    pattern = r'^[a-zA-Z][a-zA-Z0-9_]+$'
    if not re.match(pattern, username):
        return False
    
    return True


def format_phone_number(phone: str) -> str:
    """
    Форматирование номера телефона в международный формат
    
    Args:
        phone: Номер телефона
        
    Returns:
        Отформатированный номер
    """
    digits = re.sub(r'\D', '', phone)
    
    if digits.startswith('8'):
        digits = '7' + digits[1:]
    
    if not digits.startswith('+'):
        digits = '+' + digits
    
    return digits